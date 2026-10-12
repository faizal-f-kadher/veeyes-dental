/* Veeyes Dental Hospital: site behaviour. No dependencies. */
(function () {
  "use strict";
  var mq = function (q) { return window.matchMedia && window.matchMedia(q).matches; };
  var reduceMotion = mq("(prefers-reduced-motion: reduce)");
  var saveData = navigator.connection && navigator.connection.saveData;

  /* ---------- header border on scroll */
  var header = document.querySelector(".header");
  if (header) {
    var onScroll = function () { header.classList.toggle("is-scrolled", window.scrollY > 4); };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---------- treatments mega menu
     Hover opens it on devices with a mouse; click/Enter toggles it for touch and keyboard.
     A click that lands right after a hover-open keeps it open instead of closing it. */
  var trigger = document.querySelector("[data-mega-trigger]");
  var mega = document.getElementById("mega");
  if (trigger && mega) {
    var item = trigger.parentElement;
    var hoverCapable = mq("(hover: hover) and (pointer: fine)");
    var closeTimer, openedAt = 0;
    var setOpen = function (open) {
      clearTimeout(closeTimer);
      mega.hidden = !open;
      trigger.setAttribute("aria-expanded", open ? "true" : "false");
      header.classList.toggle("has-open", open);
      if (open) openedAt = Date.now();
    };
    trigger.addEventListener("click", function () {
      var isOpen = trigger.getAttribute("aria-expanded") === "true";
      if (isOpen && Date.now() - openedAt < 400) return;
      setOpen(!isOpen);
    });
    if (hoverCapable) {
      var enter = function () { if (mega.hidden) setOpen(true); else clearTimeout(closeTimer); };
      var leave = function () { closeTimer = setTimeout(function () { setOpen(false); }, 180); };
      item.addEventListener("mouseenter", enter);
      item.addEventListener("mouseleave", leave);
      mega.addEventListener("mouseenter", enter);
      mega.addEventListener("mouseleave", leave);
    }
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && !mega.hidden) { setOpen(false); trigger.focus(); }
    });
    document.addEventListener("click", function (e) {
      if (!mega.hidden && !mega.contains(e.target) && !item.contains(e.target)) setOpen(false);
    });
    mega.addEventListener("focusout", function (e) {
      if (e.relatedTarget && !mega.contains(e.relatedTarget) && e.relatedTarget !== trigger) setOpen(false);
    });
  }

  /* ---------- mobile drawer with focus trap */
  var drawer = document.getElementById("drawer");
  var openBtn = document.querySelector("[data-drawer-open]");
  if (drawer && openBtn) {
    var closeBtn = drawer.querySelector("[data-drawer-close]");
    var focusables = function () { return drawer.querySelectorAll('a[href], button, summary'); };
    var open = function () {
      drawer.hidden = false; document.documentElement.style.overflow = "hidden";
      openBtn.setAttribute("aria-expanded", "true"); closeBtn.focus();
    };
    var close = function () {
      drawer.hidden = true; document.documentElement.style.overflow = "";
      openBtn.setAttribute("aria-expanded", "false"); openBtn.focus();
    };
    openBtn.addEventListener("click", open);
    closeBtn.addEventListener("click", close);
    drawer.addEventListener("keydown", function (e) {
      if (e.key === "Escape") return close();
      if (e.key !== "Tab") return;
      var f = focusables(), first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
    window.addEventListener("resize", function () { if (!drawer.hidden && window.innerWidth > 1080) close(); });
  }

  /* ---------- mobile call chooser: close when tapping elsewhere */
  var callPick = document.querySelector(".actionbar details");
  if (callPick) document.addEventListener("click", function (e) { if (callPick.open && !callPick.contains(e.target)) callPick.open = false; });

  /* ---------- videos: load only when near the screen, smaller file on phones,
     poster only for reduced-motion / data-saver users, pause when off screen */
  var vids = document.querySelectorAll("video[data-src]");
  var small = window.innerWidth < 760;
  var load = function (v) {
    if (v.dataset.loaded) return;
    v.dataset.loaded = "1";
    if (reduceMotion || saveData) return;
    v.src = (small && v.dataset.srcSmall) ? v.dataset.srcSmall : v.dataset.src;
    v.muted = true;
    var p = v.play(); if (p && p.catch) p.catch(function () {});
  };
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        var v = en.target;
        if (en.isIntersecting) {
          load(v);
          if (v.src && v.paused) { var p = v.play(); if (p && p.catch) p.catch(function () {}); }
        } else if (v.src && !v.paused) { v.pause(); }
      });
    }, { rootMargin: "200px 0px", threshold: 0.01 });
    vids.forEach(function (v) { io.observe(v); });
  } else { vids.forEach(load); }

  /* ---------- before / after sliders */
  document.querySelectorAll(".ba input[type=range]").forEach(function (input) {
    var ba = input.closest(".ba");
    var set = function () { ba.style.setProperty("--pos", input.value + "%"); };
    input.addEventListener("input", set);
    set();
  });

  /* ---------- smile gallery filter */
  var filters = document.querySelector(".filters");
  if (filters) {
    var items = document.querySelectorAll("[data-cat]");
    var count = document.getElementById("gallery-count");
    filters.addEventListener("click", function (e) {
      var b = e.target.closest("button");
      if (!b) return;
      filters.querySelectorAll("button").forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      var cat = b.getAttribute("data-filter"), n = 0;
      items.forEach(function (it) { var show = cat === "all" || it.getAttribute("data-cat") === cat; it.hidden = !show; if (show) n++; });
      if (count) count.textContent = n + (n === 1 ? " case" : " cases");
    });
  }

  /* ---------- table of contents: highlight the section in view */
  var toc = document.querySelector(".toc");
  if (toc && "IntersectionObserver" in window) {
    var links = {};
    toc.querySelectorAll("a").forEach(function (a) { links[a.getAttribute("href").slice(1)] = a; });
    var tio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          Object.keys(links).forEach(function (k) { links[k].classList.toggle("is-active", k === en.target.id); });
        }
      });
    }, { rootMargin: "-30% 0px -60% 0px" });
    Object.keys(links).forEach(function (id) { var el = document.getElementById(id); if (el) tio.observe(el); });
  }

  /* ---------- appointment form: prefill from the link, then hand off to WhatsApp */
  var form = document.getElementById("appt");
  if (form) {
    var params = new URLSearchParams(window.location.search);
    var treat = form.querySelector("#a-treat"), clinic = form.querySelector("#a-clinic"), date = form.querySelector("#a-date");
    if (params.get("t")) {
      for (var i = 0; i < treat.options.length; i++) if (treat.options[i].getAttribute("data-slug") === params.get("t")) treat.selectedIndex = i;
    }
    if (params.get("c")) {
      for (var j = 0; j < clinic.options.length; j++) if (clinic.options[j].value.toLowerCase() === params.get("c").toLowerCase()) clinic.selectedIndex = j;
    }
    var today = new Date(); today.setMinutes(today.getMinutes() - today.getTimezoneOffset());
    date.min = today.toISOString().slice(0, 10);

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var firstBad = null;
      form.querySelectorAll("[required]").forEach(function (f) {
        var bad = !f.value.trim() || (f.type === "tel" && f.value.replace(/\D/g, "").length < 10);
        var err = document.getElementById(f.id + "-err");
        if (err) err.hidden = !bad;
        f.setAttribute("aria-invalid", bad ? "true" : "false");
        if (bad && !firstBad) firstBad = f;
      });
      if (firstBad) { firstBad.focus(); return; }
      var opt = clinic.options[clinic.selectedIndex];
      var lines = [
        "Hello Veeyes Dental, I would like to book an appointment.",
        "Name: " + form.querySelector("#a-name").value.trim(),
        "Phone: " + form.querySelector("#a-phone").value.trim(),
        "Hospital: " + clinic.value,
      ];
      if (treat.value) lines.push("Treatment: " + treat.value);
      if (date.value) lines.push("Preferred date: " + new Date(date.value + "T00:00").toLocaleDateString("en-IN", { day: "numeric", month: "long", year: "numeric" }));
      var msg = form.querySelector("#a-msg").value.trim();
      if (msg) lines.push("Note: " + msg);
      var url = "https://wa.me/" + opt.getAttribute("data-wa") + "?text=" + encodeURIComponent(lines.join("\n"));
      var status = document.getElementById("appt-status");
      status.querySelector("a").href = url;
      status.querySelector("[data-phone]").textContent = opt.getAttribute("data-phone");
      status.querySelector("[data-phone]").href = "tel:" + opt.getAttribute("data-tel");
      status.hidden = false;
      window.open(url, "_blank", "noopener");
    });
  }

  /* ---------- scroll reveals: blocks rise into place as they enter the screen.
     The matching CSS only hides them while <html> has .motion (set in <head>). */
  var root = document.documentElement;
  if (root.classList.contains("motion")) {
    window.__vyMotion = true;
    var REVEAL = ".sh, .cards > li, .article__main > .block, .aside .book, .tgroup, .facility, .bio, .clinic, .posts > li, .photos > *, .mission > *, .team > li, .lead-card, .team-strip, .rv__intro, .rv__feature, .rv__photo, .rv__more, .tx__side, .tx__group, .wgrid > li, .ba-grid > .ba-card, .band__copy, .band > .media, .photo-pair > *, .facts li, .form, .prose, .post-cover, .stack-lg > *, .lost";
    var finish = function (el) {
      setTimeout(function () { el.classList.add("is-done"); el.style.transitionDelay = ""; }, 1700 + (parseFloat(el.style.transitionDelay) || 0) * 1000);
    };
    var show = function (el, delay) {
      if (delay) el.style.transitionDelay = delay + "s";
      el.classList.add("in-view");
      finish(el);
    };
    var rio = new IntersectionObserver(function (entries) {
      var n = 0;
      entries.filter(function (e) { return e.isIntersecting; })
        .sort(function (a, b) { return a.boundingClientRect.top - b.boundingClientRect.top || a.boundingClientRect.left - b.boundingClientRect.left; })
        .forEach(function (e) { show(e.target, Math.min(n++, 5) * 0.08); rio.unobserve(e.target); });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    document.querySelectorAll(REVEAL).forEach(function (el) {
      if (el.parentElement.closest(REVEAL)) { el.classList.add("in-view", "is-done"); return; }
      rio.observe(el);
    });
    /* anything hidden by a filter (smile gallery) or jumped past by an anchor link still shows */
    window.addEventListener("hashchange", function () {
      document.querySelectorAll(REVEAL).forEach(function (el) { if (!el.classList.contains("in-view") && el.getBoundingClientRect().top < innerHeight) show(el, 0); });
    });

    /* count the hospital facts up once (years stay as they are) */
    var fio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        fio.unobserve(e.target);
        var b = e.target, txt = b.textContent, end = parseInt(txt.replace(/,/g, ""), 10), t0 = null;
        var tick = function (t) {
          t0 = t0 || t;
          var k = Math.min((t - t0) / 1400, 1), v = Math.round(end * (1 - Math.pow(1 - k, 3)));
          b.textContent = k < 1 ? v.toLocaleString("en-IN") : txt;
          if (k < 1) requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
      });
    }, { threshold: 0.6 });
    document.querySelectorAll(".facts b").forEach(function (b) {
      var s = b.textContent.trim();
      if (/^[\d,]+$/.test(s) && !/^(19|20)\d\d$/.test(s) && parseInt(s.replace(/,/g, ""), 10) > 3) fio.observe(b);
    });
  }

  /* ---------- footer year */
  var y = document.getElementById("year");
  if (y) y.textContent = String(new Date().getFullYear());
})();
