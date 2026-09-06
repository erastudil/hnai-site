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
      { rootMargin: "0px 0px -8% 0px", threshold: 0.08 }
    );
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add("in"));
  }

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
})();
