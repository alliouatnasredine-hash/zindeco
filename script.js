// =========================
// ZINDECO PEINTURE
// =========================

const header = document.querySelector("header");
const mobileToggle = document.querySelector(".menu-toggle");
const navLinks = document.querySelector(".nav-links");
const topBtn = document.querySelector(".top-btn");

if (header) {
  window.addEventListener("scroll", () => {
    header.classList.toggle("sticky", window.scrollY > 80);

    if (topBtn) {
      topBtn.classList.toggle("show", window.scrollY > 400);
    }
  });
}

if (mobileToggle && navLinks) {
  mobileToggle.addEventListener("click", () => {
    const isOpen = navLinks.classList.toggle("open");
    mobileToggle.classList.toggle("active", isOpen);
    mobileToggle.setAttribute("aria-expanded", String(isOpen));
  });

  document.querySelectorAll(".nav-links a").forEach((link) => {
    link.addEventListener("click", () => {
      navLinks.classList.remove("open");
      mobileToggle.classList.remove("active");
      mobileToggle.setAttribute("aria-expanded", "false");
    });
  });
}
