/* RGJ — Estudio profesional integral
   Interacciones y comportamiento del sitio */
(() => {
  'use strict';

  // Año en footer
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // Header con sombra al hacer scroll
  const header = document.querySelector('.site-header');
  const onScroll = () => {
    if (!header) return;
    header.classList.toggle('is-scrolled', window.scrollY > 8);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Toggle del menú móvil
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

  // Smooth scroll con offset por header sticky (fallback si scroll-behavior no aplica)
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

  // Reveal on scroll
  const revealEls = document.querySelectorAll('.section, .hero__content, .cta-banner, .service-card, .process li, .about-card');
  revealEls.forEach((el) => el.classList.add('reveal'));
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.08 });
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add('is-visible'));
  }

  // Parallax suave de los blobs en el hero
  const blobs = document.querySelectorAll('.blob');
  if (blobs.length && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    let raf = null;
    window.addEventListener('mousemove', (e) => {
      if (raf) return;
      raf = requestAnimationFrame(() => {
        const x = (e.clientX / window.innerWidth - 0.5) * 30;
        const y = (e.clientY / window.innerHeight - 0.5) * 30;
        blobs.forEach((b, i) => {
          const f = (i + 1) * 0.6;
          b.style.transform = `translate(${x * f}px, ${y * f}px)`;
        });
        raf = null;
      });
    });
  }

  // Validación y feedback del formulario
  const form = document.getElementById('contactForm');
  const status = document.getElementById('formStatus');

  const isEmail = (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);

  if (form && status) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      status.className = 'form__status';
      status.textContent = '';

      const data = {
        nombre: form.nombre.value.trim(),
        email: form.email.value.trim(),
        tema: form.tema.value,
        mensaje: form.mensaje.value.trim(),
      };

      // Marcar errores
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
        status.textContent = 'Revisá los campos marcados, por favor.';
        return;
      }

      // Simulación de envío (sin backend). Para producción, conectar a un endpoint o servicio (Formspree, Resend, etc.)
      const submitBtn = form.querySelector('button[type="submit"]');
      const originalText = submitBtn.innerHTML;
      submitBtn.disabled = true;
      submitBtn.innerHTML = 'Enviando…';

      setTimeout(() => {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
        form.reset();
        status.classList.add('is-success');
        status.textContent = '¡Gracias! Recibimos tu consulta y te respondemos en menos de 24 hs.';
      }, 900);
    });
  }
})();
