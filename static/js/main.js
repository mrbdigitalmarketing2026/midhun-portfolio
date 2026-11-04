
document.addEventListener("DOMContentLoaded", () => {
  // Mobile navigation
  const toggle = document.querySelector(".menu-toggle");
  const nav = document.querySelector(".main-nav");

  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const isOpen = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(isOpen));
      toggle.setAttribute("aria-label", isOpen ? "Close navigation" : "Open navigation");
    });

    nav.querySelectorAll("a").forEach(link => {
      link.addEventListener("click", () => {
        nav.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  // Back to top button
  const backToTop = document.querySelector(".back-to-top");

  if (backToTop) {
    window.addEventListener("scroll", () => {
      backToTop.classList.toggle("visible", window.scrollY > 400);
    });

    backToTop.addEventListener("click", () => {
      window.scrollTo({
        top: 0,
        behavior: "smooth"
      });
    });
  }
});
