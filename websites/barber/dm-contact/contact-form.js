/*!
 * Data Master — contact form helper
 * Sends any <form data-dm-contact> to dm-contact/contact.php without leaving the page.
 * On GitHub Pages / local files it stays in demo mode and sends nothing.
 *
 * Form attributes:
 *   action="dm-contact/contact.php" method="post" data-dm-contact
 *   data-sent-target="#formCard"   (optional) element that gets class "sent" on success
 *   data-dm-contact="demo"         (optional) force demo mode
 */
(function () {
    "use strict";

    var TXT = {
        el: {
            sending: "Αποστολή…",
            network: "Δεν ήταν δυνατή η σύνδεση. Ελέγξτε τη σύνδεσή σας και δοκιμάστε ξανά.",
            ok: "Ευχαριστούμε! Λάβαμε το μήνυμά σας."
        },
        en: {
            sending: "Sending…",
            network: "Could not connect. Please check your connection and try again.",
            ok: "Thank you! We received your message."
        }
    };

    function lang() {
        return (document.documentElement.lang || "el").toLowerCase().indexOf("en") === 0 ? "en" : "el";
    }

    function isDemo(form) {
        var h = location.hostname;
        return form.getAttribute("data-dm-contact") === "demo" ||
            location.protocol === "file:" || /\.github\.io$/.test(h) || !form.getAttribute("action");
    }

    function hidden(form, name, value) {
        var el = form.querySelector('input[name="' + name + '"]');
        if (!el) {
            el = document.createElement("input");
            el.type = "hidden";
            el.name = name;
            form.appendChild(el);
        }
        el.value = value;
    }

    function addHoneypot(form) {
        if (form.querySelector('[name="dm_hp"]')) return;
        var wrap = document.createElement("div");
        wrap.setAttribute("aria-hidden", "true");
        wrap.style.cssText = "position:absolute;left:-9999px;top:auto;width:1px;height:1px;overflow:hidden";
        wrap.innerHTML = '<label>Leave this field empty<input type="text" name="dm_hp" tabindex="-1" autocomplete="off"></label>';
        form.appendChild(wrap);
    }

    function text(el) {
        return el ? el.textContent.replace(/\s+/g, " ").replace(/[*:]\s*$/, "").trim() : "";
    }

    // The label a visitor sees for each field, so the owner's email reads naturally.
    function labelFor(form, field) {
        return labelText(form, field).replace(/\s*\((optional|προαιρετικό|προαιρετικά)\)\s*$/i, "");
    }

    function labelText(form, field) {
        if (field.id) {
            var l = form.querySelector('label[for="' + field.id + '"]');
            if (l) return text(l);
        }
        var fs = field.closest("fieldset");
        if (fs && (field.type === "radio" || field.type === "checkbox") && fs.querySelector("legend")) {
            return text(fs.querySelector("legend"));
        }
        var wrap = field.closest("label");
        return wrap ? text(wrap) : "";
    }

    function statusEl(form) {
        var s = form.querySelector("[data-dm-status]");
        if (!s) {
            s = document.createElement("p");
            s.setAttribute("data-dm-status", "");
            s.setAttribute("role", "alert");
            s.style.cssText = "margin:12px 0 0;font-size:.95em";
            var btn = form.querySelector('[type="submit"]');
            (btn && btn.parentNode === form ? btn : form.lastChild).after(s);
        }
        return s;
    }

    function showSent(form, message) {
        var sel = form.getAttribute("data-sent-target");
        var target = sel ? document.querySelector(sel) : null;
        if (target) {
            target.classList.add("sent");
        } else {
            var s = statusEl(form);
            s.style.color = "";
            s.textContent = message;
        }
        form.reset();
        form.dispatchEvent(new CustomEvent("dm:sent", { bubbles: true }));
    }

    function init(form) {
        addHoneypot(form);
        hidden(form, "_t", String(Date.now()));

        form.addEventListener("submit", function (e) {
            e.preventDefault();
            if (!form.checkValidity()) { form.reportValidity(); return; }

            var L = lang(), T = TXT[L];
            if (isDemo(form)) { showSent(form, T.ok); return; }

            hidden(form, "_lang", L);
            hidden(form, "_page", location.href.split("#")[0]);

            var data = new FormData(form), labels = {};
            Array.prototype.forEach.call(form.elements, function (f) {
                if (!f.name || f.type === "hidden" || f.name === "dm_hp") return;
                if (!labels[f.name]) { var lb = labelFor(form, f); if (lb) labels[f.name] = lb; }
                // Send what the visitor saw ("Αλλαγή λογιστή"), not the code ("switch").
                if (f.tagName === "SELECT") {
                    if (f.value === "" || f.selectedIndex < 0) data.delete(f.name);
                    else data.set(f.name, text(f.options[f.selectedIndex]));
                } else if (f.type === "radio" && f.checked) {
                    var t = text(f.closest("label"));
                    if (t) data.set(f.name, t);
                }
            });
            data.set("_labels", JSON.stringify(labels));

            var btn = form.querySelector('[type="submit"]');
            var s = statusEl(form);
            s.textContent = T.sending;
            s.style.color = "";
            if (btn) btn.disabled = true;

            fetch(form.getAttribute("action"), {
                method: "POST",
                body: data,
                headers: { Accept: "application/json" },
                credentials: "same-origin"
            })
                .then(function (r) { return r.json().catch(function () { return { ok: false, message: T.network }; }); })
                .then(function (res) {
                    if (res.ok) {
                        s.textContent = "";
                        showSent(form, res.message || T.ok);
                        hidden(form, "_t", String(Date.now()));
                    } else {
                        s.style.color = "#b42318";
                        s.textContent = res.message || T.network;
                    }
                })
                .catch(function () {
                    s.style.color = "#b42318";
                    s.textContent = T.network;
                })
                .then(function () { if (btn) btn.disabled = false; });
        });
    }

    function start() {
        Array.prototype.forEach.call(document.querySelectorAll("form[data-dm-contact]"), init);
    }
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
    else start();
})();
