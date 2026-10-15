// Interactive elements of the learning modules (see scripts/learn.py).
// Everything happens in the browser and nothing is sent anywhere. Only the
// chosen persona and, in exercises, the reader's own written answers are kept
// in localStorage (if the browser allows it).
(function () {
  "use strict";

  function setup(module) {
    var ui = { correct: module.dataset.correct || "Correct!", wrong: module.dataset.wrong || "Not quite." };
    var quizzes = Array.prototype.slice.call(module.querySelectorAll(".quiz"));
    var scorebar = module.querySelector(".scorebar");
    var solved = new Set();
    var touched = false;

    function updateScore() {
      if (!scorebar || !quizzes.length || !touched) return;
      scorebar.hidden = false;
      scorebar.querySelector(".score").textContent = solved.size;
      scorebar.querySelector(".total").textContent = quizzes.length;
    }

    function feedback(box, ok, text) {
      var fb = box.querySelector(".feedback");
      fb.hidden = false;
      fb.className = "feedback " + (ok ? "ok" : "no");
      fb.textContent = text;
    }

    function showExplain(box, show) {
      var explain = box.querySelector(".explain");
      if (explain && explain.textContent.trim()) explain.hidden = !show;
    }

    quizzes.forEach(function (box, index) {
      if (box.dataset.kind === "quiz") {
        var select = box.querySelector("select");
        select.addEventListener("change", function () {
          touched = true;
          if (!select.value) {
            box.querySelector(".feedback").hidden = true;
            showExplain(box, false);
            solved.delete(index);
          } else {
            var ok = select.value === box.dataset.answer;
            feedback(box, ok, ok ? "✓ " + ui.correct : "✗ " + ui.wrong);
            showExplain(box, ok);
            if (ok) solved.add(index); else solved.delete(index);
          }
          updateScore();
        });
        return;
      }
      var rows = Array.prototype.slice.call(box.querySelectorAll("tr[data-answer]"));
      rows.forEach(function (row) {
        row.querySelector("select").addEventListener("change", function () {
          touched = true;
          var done = 0, right = 0;
          rows.forEach(function (r) {
            var value = r.querySelector("select").value;
            var mark = r.querySelector(".mark");
            if (!value) { mark.textContent = ""; r.className = ""; return; }
            done++;
            var ok = value === r.dataset.answer;
            if (ok) right++;
            mark.textContent = ok ? "✓" : "✗";
            r.className = ok ? "ok" : "no";
          });
          if (done === rows.length) {
            var all = right === rows.length;
            feedback(box, all, (all ? "✓ " + ui.correct : "✗ " + ui.wrong) + " (" + right + "/" + rows.length + ")");
            showExplain(box, all);
            if (all) solved.add(index); else solved.delete(index);
          } else {
            box.querySelector(".feedback").hidden = true;
            showExplain(box, false);
            solved.delete(index);
          }
          updateScore();
        });
      });
    });

    if (scorebar) {
      scorebar.querySelector(".reset").addEventListener("click", function () {
        module.querySelectorAll(".quiz select").forEach(function (s) { s.value = ""; });
        module.querySelectorAll(".quiz .feedback, .quiz .explain").forEach(function (e) { e.hidden = true; });
        module.querySelectorAll(".quiz .mark").forEach(function (m) { m.textContent = ""; });
        module.querySelectorAll(".quiz tr").forEach(function (r) { r.className = ""; });
        solved.clear();
        updateScore();
      });
    }

    // Persona picker: show only the "why this matters" boxes for the chosen audience.
    var picker = module.querySelector(".persona-picker");
    var personas = module.querySelectorAll(".persona");
    if (picker && personas.length) {
      picker.hidden = false;
      var choice = picker.querySelector("select");
      var apply = function (value) {
        personas.forEach(function (p) { p.hidden = value !== "" && p.dataset.persona !== value; });
      };
      try { choice.value = localStorage.getItem("tentopics-persona") || ""; } catch (e) { /* storage blocked */ }
      if (!Array.prototype.some.call(choice.options, function (o) { return o.value === choice.value; })) choice.value = "";
      apply(choice.value);
      choice.addEventListener("change", function () {
        apply(choice.value);
        try { localStorage.setItem("tentopics-persona", choice.value); } catch (e) { /* storage blocked */ }
      });
    }
  }

  // Exercises: keep written answers locally, show solution notes only after an
  // own attempt, and let readers download their answers.
  function setupExercise(module) {
    var key = "tentopics-notes-" + module.dataset.module + "-" + module.lang;
    var tasks = Array.prototype.slice.call(module.querySelectorAll(".reflect.task"));
    var bar = module.querySelector(".notes-bar");
    var notes = {};
    try { notes = JSON.parse(localStorage.getItem(key) || "{}") || {}; } catch (e) { notes = {}; }

    function save() {
      try { localStorage.setItem(key, JSON.stringify(notes)); } catch (e) { /* storage blocked */ }
    }

    function gate(task) {
      var written = task.querySelector("textarea").value.trim().length > 0;
      var solution = task.querySelector(".solution");
      solution.hidden = !written;
      if (!written) solution.open = false;
      task.querySelector(".gate").hidden = written;
    }

    tasks.forEach(function (task) {
      var area = task.querySelector("textarea");
      if (notes[area.dataset.key]) area.value = notes[area.dataset.key];
      gate(task);
      area.addEventListener("input", function () {
        if (area.value.trim()) notes[area.dataset.key] = area.value; else delete notes[area.dataset.key];
        save();
        gate(task);
      });
    });

    if (!bar || !tasks.length) return;
    bar.hidden = false;
    bar.querySelector(".download").addEventListener("click", function () {
      var title = module.querySelector("h1").textContent;
      var lines = ["# " + title, "", location.href, ""];
      tasks.forEach(function (task) {
        lines.push("## " + task.querySelector(".q").textContent.replace(/^\S+\s/, "").trim(), "");
        lines.push(task.querySelector("textarea").value.trim() || "–", "");
      });
      var blob = new Blob([lines.join("\n")], { type: "text/markdown;charset=utf-8" });
      var link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = module.dataset.module + "-" + module.lang + ".md";
      document.body.appendChild(link);
      link.click();
      setTimeout(function () { URL.revokeObjectURL(link.href); link.remove(); }, 0);
    });
    bar.querySelector(".clear").addEventListener("click", function () {
      if (!window.confirm(module.dataset.confirm || "Clear?")) return;
      notes = {};
      try { localStorage.removeItem(key); } catch (e) { /* storage blocked */ }
      tasks.forEach(function (task) { task.querySelector("textarea").value = ""; gate(task); });
    });
  }

  document.querySelectorAll(".module").forEach(setup);
  document.querySelectorAll(".module.exercise").forEach(setupExercise);
})();
