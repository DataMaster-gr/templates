/* Nikolaou & Partners multi-page template: menu, reveal, form helpers. */
(function () {
    var btn = document.querySelector(".menu-btn");
    var menu = document.getElementById("mnav");
    if (btn && menu) {
        btn.addEventListener("click", function () {
            var open = btn.getAttribute("aria-expanded") === "true";
            btn.setAttribute("aria-expanded", open ? "false" : "true");
            menu.classList.toggle("open", !open);
        });
    }

    // Remember the language choice so the Data Master gallery and other demos follow it.
    document.querySelectorAll("[data-set-lang]").forEach(function (a) {
        a.addEventListener("click", function () { try { localStorage.setItem("dm-lang", a.getAttribute("data-set-lang")); } catch (e) {} });
    });

    // Contact page: preselect the practice area from ?area=… (links on the area pages).
    var area = new URLSearchParams(location.search).get("area");
    var sel = document.getElementById("f-area");
    if (area && sel && sel.querySelector('option[value="' + area + '"]')) sel.value = area;

    var els = document.querySelectorAll(".reveal");
    if ("IntersectionObserver" in window) {
        var io = new IntersectionObserver(function (entries) {
            entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
        }, { rootMargin: "0px 0px -40px 0px" });
        els.forEach(function (el) { io.observe(el); });
    } else { els.forEach(function (el) { el.classList.add("in"); }); }
})();
