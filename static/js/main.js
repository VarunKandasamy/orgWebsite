/* ============================================================
   DEMOPOLIS COALITION — MAIN JS
   ============================================================ */

(function () {
  'use strict';

  // ---- Logo header + nav scroll behaviour ----
  const logoHeader = document.getElementById('logo-header');
  const nav = document.querySelector('.nav');
  const SCROLL_THRESHOLD = 20;

  function updateNavOnScroll() {
    const scrolled = window.scrollY > SCROLL_THRESHOLD;
    if (scrolled) {
      if (logoHeader) logoHeader.classList.add('is-hidden');
      if (nav) {
        nav.classList.remove('at-top');
        nav.classList.add('is-scrolled');
      }
    } else {
      if (logoHeader) logoHeader.classList.remove('is-hidden');
      if (nav) {
        nav.classList.remove('is-scrolled');
        nav.classList.add('at-top');
      }
    }
  }

  window.addEventListener('scroll', updateNavOnScroll, { passive: true });
  updateNavOnScroll();

  // ---- Mobile hamburger ----
  const hamburger = document.getElementById('nav-hamburger');
  const mobileMenu = document.getElementById('nav-mobile');

  if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', function () {
      const isOpen = mobileMenu.classList.toggle('is-open');
      hamburger.setAttribute('aria-expanded', isOpen);
    });

    document.addEventListener('click', function (e) {
      if (!hamburger.contains(e.target) && !mobileMenu.contains(e.target)) {
        mobileMenu.classList.remove('is-open');
        hamburger.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // ---- About Us dropdown (keyboard/click for accessibility) ----
  const aboutItem = document.querySelector('.nav__item--dropdown');
  const aboutBtn = document.getElementById('about-nav-btn');

  if (aboutItem && aboutBtn) {
    // Click toggles dropdown open/closed
    aboutBtn.addEventListener('click', function (e) {
      // If navigating directly to /about, allow. Otherwise toggle dropdown.
      const isOpen = aboutItem.classList.toggle('is-open');
      aboutBtn.setAttribute('aria-expanded', isOpen);
      if (isOpen) e.preventDefault();
    });

    // Close when clicking outside
    document.addEventListener('click', function (e) {
      if (!aboutItem.contains(e.target)) {
        aboutItem.classList.remove('is-open');
        aboutBtn.setAttribute('aria-expanded', 'false');
      }
    });

    // Close on Escape
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        aboutItem.classList.remove('is-open');
        aboutBtn.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // ---- Set active nav link ----
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav__link').forEach(function (link) {
    const href = link.getAttribute('href');
    if (!href) return;
    if (href === '/' && currentPath === '/') {
      link.classList.add('active');
    } else if (href !== '/' && href !== '/contact?ref=donate' && currentPath.startsWith(href.split('?')[0])) {
      link.classList.add('active');
    }
  });

  // ---- Chapter card accordion ----
  document.querySelectorAll('.chapter-card__summary').forEach(function (summary) {
    summary.addEventListener('click', function () {
      const card = summary.closest('.chapter-card');
      const body = card.querySelector('.chapter-card__body');
      const isOpen = card.classList.toggle('is-open');
      summary.setAttribute('aria-expanded', isOpen);
      if (body) {
        body.style.maxHeight = isOpen ? body.scrollHeight + 'px' : '0';
      }
    });
  });

})();
