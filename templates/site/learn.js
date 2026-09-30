// Interactive elements of the learning modules (see scripts/learn.py).
// Everything happens in the browser. Only the chosen persona is remembered
// (in localStorage, if the browser allows it); answers are never stored or sent.
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

  document.querySelectorAll(".module").forEach(setup);
})();
