/* Data Master showcase — shared ΕΛ/EN switch.
   Each page defines window.DM_T = { en: {...}, el: {...} } before loading this file.
   Elements: data-i18n (text), data-i18n-aria (aria-label), data-i18n-ph (placeholder),
   data-mail (mailto subject), data-set-lang (switch buttons).
   Pages can react to changes with window.DM.onLang(fn); the choice is stored as "dm-lang",
   which the demo ribbons in the templates also read. */
(function () {
    var MAIL = "info@datamaster.gr";
    var SHARED = {
        en: {
            "nav.contact": "Contact us",
            "crumb.home": "All samples",
            "crumb.label": "Breadcrumb",
            "cta.title": "Not sure what fits?",
            "cta.text": "Tell us about your business and we'll recommend the best starting point, or design something tailored to you.",
            "cta.ask": "Ask us",
            "cta.visit": "Visit datamaster.gr",
            "footer.note": "Business names, texts and images in the demos are sample content.",
            "mail.general": "Website enquiry",
            "mail.help": "Help me choose for my website"
        },
        el: {
            "nav.contact": "Επικοινωνία",
            "crumb.home": "Όλα τα δείγματα",
            "crumb.label": "Διαδρομή",
            "cta.title": "Δεν είστε σίγουροι τι ταιριάζει;",
            "cta.text": "Πείτε μας για την επιχείρησή σας και θα σας προτείνουμε την καλύτερη αφετηρία ή θα σχεδιάσουμε κάτι αποκλειστικά για εσάς.",
            "cta.ask": "Ρωτήστε μας",
            "cta.visit": "Επισκεφθείτε το datamaster.gr",
            "footer.note": "Τα ονόματα επιχειρήσεων, τα κείμενα και οι εικόνες στα demos είναι ενδεικτικά.",
            "mail.general": "Ερώτηση για ιστοσελίδα",
            "mail.help": "Βοηθήστε με να διαλέξω για την ιστοσελίδα μου"
        }
    };
    var PAGE = window.DM_T || {};
    var T = {};
    ["en", "el"].forEach(function (l) {
        T[l] = {};
        var k;
        for (k in SHARED[l]) T[l][k] = SHARED[l][k];
        for (k in (PAGE[l] || {})) T[l][k] = PAGE[l][k];
    });
    var listeners = [];
    var current = null;

    function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }

    function apply(lang) {
        var t = T[lang];
        current = lang;
        document.documentElement.lang = lang;
        if (t["meta.title"]) document.title = t["meta.title"];
        var d = document.querySelector('meta[name="description"]');
        if (d && t["meta.desc"]) d.setAttribute("content", t["meta.desc"]);
        document.querySelectorAll("[data-i18n]").forEach(function (el) {
            var v = t[el.getAttribute("data-i18n")];
            if (v != null) el.textContent = v;
        });
        document.querySelectorAll("[data-i18n-aria]").forEach(function (el) {
            var v = t[el.getAttribute("data-i18n-aria")];
            if (v != null) el.setAttribute("aria-label", v);
        });
        document.querySelectorAll("[data-i18n-ph]").forEach(function (el) {
            var v = t[el.getAttribute("data-i18n-ph")];
            if (v != null) el.setAttribute("placeholder", v);
        });
        document.querySelectorAll("[data-mail]").forEach(function (el) {
            var v = t[el.getAttribute("data-mail")];
            if (v != null) el.href = "mailto:" + MAIL + "?subject=" + encodeURIComponent(v);
        });
        document.querySelectorAll("[data-set-lang]").forEach(function (b) {
            b.setAttribute("aria-pressed", b.getAttribute("data-set-lang") === lang ? "true" : "false");
        });
        listeners.forEach(function (fn) { try { fn(lang, t); } catch (e) {} });
    }

    function setLang(lang, remember) {
        if (!T[lang]) return;
        apply(lang);
        if (remember) store("dm-lang", lang);
        try {
            var u = new URL(location.href);
            u.searchParams.set("lang", lang);
            history.replaceState(null, "", u);
        } catch (e) {}
    }

    window.DM = {
        t: function (k) { return (T[current] || {})[k]; },
        lang: function () { return current; },
        onLang: function (fn) { listeners.push(fn); if (current) fn(current, T[current]); }
    };

    var fromUrl = new URLSearchParams(location.search).get("lang");
    var saved = store("dm-lang");
    var initial = T[fromUrl] ? fromUrl
        : (T[saved] ? saved
        : ((navigator.language || "").toLowerCase().indexOf("el") === 0 ? "el" : "en"));
    apply(initial);

    document.querySelectorAll("[data-set-lang]").forEach(function (b) {
        b.addEventListener("click", function () { setLang(b.getAttribute("data-set-lang"), true); });
    });
})();
