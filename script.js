/* Rafa García Juanicó — site behavior */
(() => {
  'use strict';

  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  const header = document.querySelector('.site-header');
  const onScroll = () => {
    if (header) header.classList.toggle('is-scrolled', window.scrollY > 8);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  const toggle = document.querySelector('.nav__toggle');
  const mobileMenu = document.getElementById('mobile-menu');
  if (toggle && mobileMenu) {
    toggle.addEventListener('click', () => {
      const open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      mobileMenu.hidden = open;
      mobileMenu.classList.toggle('is-open', !open);
    });
    mobileMenu.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        toggle.setAttribute('aria-expanded', 'false');
        mobileMenu.hidden = true;
        mobileMenu.classList.remove('is-open');
      });
    });
  }

  document.querySelectorAll('a[href^="#"]').forEach((a) => {
    a.addEventListener('click', (e) => {
      const id = a.getAttribute('href');
      if (!id || id === '#') return;
      const target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      const offset = (header?.offsetHeight || 0) + 8;
      const top = target.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: 'smooth' });
    });
  });

  const revealEls = document.querySelectorAll('.section, .hero__inner, .cta-banner, .service-card, .process li, .about-card');
  revealEls.forEach((el) => el.classList.add('reveal'));
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add('is-visible'));
  }

  const form = document.getElementById('contactForm');
  const status = document.getElementById('formStatus');
  const isEmail = (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);

  if (form && status) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      status.className = 'form__status';
      status.textContent = '';

      const data = {
        nombre: form.nombre.value.trim(),
        email: form.email.value.trim(),
        tema: form.tema.value,
        mensaje: form.mensaje.value.trim(),
      };

      let firstError = null;
      [['nombre', !!data.nombre], ['email', isEmail(data.email)], ['tema', !!data.tema], ['mensaje', data.mensaje.length >= 10]].forEach(([name, ok]) => {
        const field = form[name].closest('.field');
        if (!field) return;
        field.classList.toggle('is-error', !ok);
        if (!ok && !firstError) firstError = form[name];
      });

      if (firstError) {
        firstError.focus();
        status.classList.add('is-error');
        status.textContent = 'Revisá los campos marcados.';
        return;
      }

      const submitBtn = form.querySelector('button[type="submit"]');
      const originalText = submitBtn.innerHTML;
      submitBtn.disabled = true;
      submitBtn.innerHTML = 'Enviando…';

      try {
        const fd = new FormData(form);
        const res = await fetch(form.action, {
          method: 'POST',
          body: fd,
          headers: { 'Accept': 'application/json' },
        });
        if (!res.ok) throw new Error('Bad response: ' + res.status);
        form.reset();
        status.classList.add('is-success');
        status.textContent = 'Recibí tu consulta. Te respondo en menos de 24 hs.';
      } catch (err) {
        status.classList.add('is-error');
        status.textContent = 'No pude enviar el mensaje. Escribime a hola@rgj.com.ar';
      } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
      }
    });
  }
})();
