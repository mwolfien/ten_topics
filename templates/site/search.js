// Client-side search over all keyword items and references.
// The index is embedded in the page as JSON (see scripts/site.py), so the search
// works without a server and without network requests.
(function () {
  "use strict";
  var data = JSON.parse(document.getElementById("search-index").textContent);
  var form = document.getElementById("search");
  var input = document.getElementById("q");
  var topicSelect = document.getElementById("topic");
  var newOnly = document.getElementById("new-only");
  var status = document.getElementById("search-status");
  var list = document.getElementById("results");
  var grid = document.getElementById("topics");
  var MAX = 200;

  function fold(text) {
    return text.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
  }

  function escapeHtml(text) {
    return text.replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  data.items.forEach(function (item) {
    item.haystack = fold(item.text + " " + item.topic + " " + item.refs.map(function (r) {
      return [r.label, r.title || "", r.journal || "", r.year || ""].join(" ");
    }).join(" "));
  });

  function render() {
    var terms = fold(input.value).split(/\s+/).filter(Boolean);
    var topic = topicSelect.value;
    var onlyNew = newOnly.checked;
    var active = terms.length > 0 || topic !== "" || onlyNew;
    grid.hidden = active;
    list.innerHTML = "";
    if (!active) {
      status.textContent = "";
      return;
    }
    var hits = data.items.filter(function (item) {
      if (topic && item.topicId !== topic) return false;
      if (onlyNew && !item.refs.some(function (r) { return r.isNew; })) return false;
      return terms.every(function (t) { return item.haystack.indexOf(t) !== -1; });
    });
    status.textContent = hits.length === 1 ? "1 result" : hits.length + " results";
    hits.slice(0, MAX).forEach(function (item) {
      var li = document.createElement("li");
      var refs = item.refs.map(function (r) {
        var label = '<a href="' + escapeHtml(r.url) + '">' + escapeHtml(r.label) + "</a>";
        var extra = r.title ? " – " + escapeHtml(r.title) : "";
        return label + extra + (r.isNew ? ' <span class="badge">new</span>' : "");
      });
      li.innerHTML =
        '<a class="topic" href="' + escapeHtml(item.topicUrl) + '">' + escapeHtml(item.topic) + "</a>" +
        "<div>" + escapeHtml(item.text) + "</div>" +
        (refs.length ? '<ul class="refs">' + refs.map(function (r) { return "<li>" + r + "</li>"; }).join("") + "</ul>" : "");
      list.appendChild(li);
    });
  }

  form.addEventListener("submit", function (event) { event.preventDefault(); render(); });
  input.addEventListener("input", render);
  topicSelect.addEventListener("change", render);
  newOnly.addEventListener("change", render);

  var params = new URLSearchParams(window.location.search);
  if (params.get("q")) input.value = params.get("q");
  render();
})();
