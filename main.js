/* scroll atmosphere + reveal */
(function () {
  const grid = document.getElementById("bg-grid");
  let ticking = false;

  function onScroll() {
    if (!ticking) {
      window.requestAnimationFrame(() => {
        const y = window.scrollY || 0;
        if (grid) {
          grid.style.setProperty("--scroll-y", `${y * -0.12}px`);
        }
        ticking = false;
      });
      ticking = true;
    }
  }

  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  const reveals = document.querySelectorAll(".reveal");

  function revealNearby() {
    const vh = window.innerHeight || 800;
    reveals.forEach((el) => {
      const rect = el.getBoundingClientRect();
      if (rect.top < vh + 300) {
        el.classList.add("in");
      }
    });
  }

  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add("in");
            io.unobserve(e.target);
          }
        });
      },
      { rootMargin: "300px 0px 300px 0px", threshold: 0.01 }
    );
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add("in"));
  }

  revealNearby();
  window.addEventListener("load", revealNearby);
  window.addEventListener("resize", revealNearby, { passive: true });

  const modal = document.getElementById("valor-modal");
  const openBtn = document.getElementById("valor-open");
  const closeBtn = document.getElementById("valor-close");

  function openValor() {
    if (!modal) return;
    modal.hidden = false;
    document.body.style.overflow = "hidden";
    if (closeBtn) closeBtn.focus();
  }

  function closeValor() {
    if (!modal) return;
    modal.hidden = true;
    document.body.style.overflow = "";
    if (openBtn) openBtn.focus();
  }

  if (openBtn) openBtn.addEventListener("click", openValor);
  if (closeBtn) closeBtn.addEventListener("click", closeValor);
  if (modal) {
    modal.addEventListener("click", (e) => {
      if (e.target === modal) closeValor();
    });
  }
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modal && !modal.hidden) closeValor();
  });

  /* copy button feedback */
  document.querySelectorAll(".copy-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const targetId = btn.getAttribute("data-copy-target");
      const targetEl = targetId ? document.getElementById(targetId) : null;
      const textToCopy = targetEl ? (targetEl.value || targetEl.textContent) : btn.getAttribute("data-copy");
      if (textToCopy) {
        navigator.clipboard.writeText(textToCopy.trim()).then(() => {
          const original = btn.textContent;
          btn.textContent = "copied!";
          btn.style.background = "#8b5cf6";
          btn.style.color = "#ffffff";
          setTimeout(() => {
            btn.textContent = original;
            btn.style.background = "";
            btn.style.color = "";
          }, 2000);
        }).catch(() => {
          btn.textContent = "select text";
        });
      }
    });
  });

  /* hydra interactive tab switcher */
  const tabBtns = document.querySelectorAll('.hydra-tab-btn');
  const tabPanels = document.querySelectorAll('.hydra-tab-panel');
  if (tabBtns.length > 0 && tabPanels.length > 0) {
    tabBtns.forEach((btn) => {
      btn.addEventListener('click', () => {
        const targetTab = btn.getAttribute('data-tab');
        tabBtns.forEach((b) => b.classList.remove('active'));
        tabPanels.forEach((p) => p.classList.remove('active'));
        btn.classList.add('active');
        const panel = document.getElementById(targetTab);
        if (panel) panel.classList.add('active');
      });
    });
  }

})();
