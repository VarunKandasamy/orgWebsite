/* ============================================================
   DEMOPOLIS COALITION — NEWSLETTER JS
   Intercept form submit, POST to /newsletter/subscribe
   ============================================================ */

(function () {
  'use strict';

  function attachNewsletterForm(formId, confirmId) {
    const form = document.getElementById(formId);
    const confirm = document.getElementById(confirmId);
    if (!form) return;

    form.addEventListener('submit', async function (e) {
      e.preventDefault();
      const emailInput = form.querySelector('input[type="email"]');
      if (!emailInput || !emailInput.value.trim()) return;

      const btn = form.querySelector('button[type="submit"]');
      if (btn) {
        btn.disabled = true;
        btn.textContent = 'Subscribing...';
      }

      try {
        const res = await fetch('/newsletter/subscribe', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: emailInput.value.trim() }),
        });

        const data = await res.json();

        if (data.status === 'subscribed') {
          if (confirm) {
            confirm.textContent = 'Thank you for subscribing!';
            confirm.style.color = '#C5A44E';
          }
          emailInput.value = '';
          if (btn) {
            btn.textContent = 'Subscribed!';
          }
        }
      } catch (err) {
        if (confirm) {
          confirm.textContent = 'Something went wrong. Please try again.';
          confirm.style.color = '#e55';
        }
        if (btn) {
          btn.disabled = false;
          btn.textContent = 'Subscribe';
        }
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      attachNewsletterForm('hero-newsletter-form', 'hero-newsletter-confirm');
      attachNewsletterForm('footer-newsletter-form', 'footer-newsletter-confirm');
    });
  } else {
    attachNewsletterForm('hero-newsletter-form', 'hero-newsletter-confirm');
    attachNewsletterForm('footer-newsletter-form', 'footer-newsletter-confirm');
  }
})();
