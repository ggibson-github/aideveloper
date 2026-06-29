(function () {
  "use strict";

  function rel(path) {
    var base = document.body.getAttribute("data-base") || "";
    return base + path;
  }

  document.addEventListener("DOMContentLoaded", function () {
    if (typeof mermaid !== "undefined") {
      mermaid.initialize({
        startOnLoad: true,
        theme: "neutral",
        securityLevel: "loose",
        flowchart: { curve: "basis", padding: 16 },
      });
    }

    document.querySelectorAll("[data-chart]").forEach(function (el) {
      var spec = el.getAttribute("data-chart");
      if (!spec || typeof Chart === "undefined") return;
      try {
        var cfg = JSON.parse(spec);
        cfg.options = cfg.options || {};
        cfg.options.responsive = true;
        cfg.options.maintainAspectRatio = false;
        cfg.options.plugins = cfg.options.plugins || {};
        cfg.options.plugins.legend = cfg.options.plugins.legend || { position: "bottom", labels: { boxWidth: 12, font: { size: 11 } } };
        new Chart(el.getContext("2d"), cfg);
      } catch (e) {
        console.warn("Chart init failed", e);
      }
    });
  });
})();
