/* SIO · Rediseño Home — interacciones (vanilla JS, sin dependencias) */
(() => {
  'use strict';

  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const clamp = (n, a, b) => Math.min(b, Math.max(a, n));

  /* ---------- Anclas internas: scroll propio (más fiable dentro de un visor embebido) ---------- */
  document.addEventListener('click', e => {
    const a = e.target.closest('a[href^="#"]');
    if (!a) return;
    const id = a.getAttribute('href').slice(1);
    const target = id && document.getElementById(id);
    if (!target) return;
    e.preventDefault();
    target.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' });
  });

  /* ---------- Año + barra superior ---------- */
  $$('[data-year]').forEach(el => (el.textContent = new Date().getFullYear()));
  const topbar = $('#topbar');
  $('[data-close-topbar]')?.addEventListener('click', () => topbar.classList.add('is-hidden'));

  /* ---------- Nav: sombra al hacer scroll ---------- */
  const navWrap = $('#nav');
  const onScrollNav = () => navWrap.classList.toggle('is-scrolled', scrollY > 24);
  onScrollNav();
  addEventListener('scroll', onScrollNav, { passive: true });

  /* ---------- Mega menú "Soluciones" ---------- */
  const mega = $('.has-mega');
  if (mega) {
    const trigger = $('.mega-trigger', mega);
    let closeTimer;
    const open = () => { clearTimeout(closeTimer); mega.classList.add('is-open'); trigger.setAttribute('aria-expanded', 'true'); };
    const close = () => { mega.classList.remove('is-open'); trigger.setAttribute('aria-expanded', 'false'); };
    const canHover = matchMedia('(hover: hover)').matches;
    if (canHover) {
      mega.addEventListener('mouseenter', open);
      mega.addEventListener('mouseleave', () => { closeTimer = setTimeout(close, 160); });
    }
    trigger.addEventListener('click', () => (mega.classList.contains('is-open') ? close() : open()));
    mega.addEventListener('focusout', e => { if (!mega.contains(e.relatedTarget)) close(); });
    addEventListener('keydown', e => { if (e.key === 'Escape') { close(); closeDrawer(); } });
    document.addEventListener('click', e => { if (!mega.contains(e.target)) close(); });
    $$('.mega a', mega).forEach(a => a.addEventListener('click', close));
  }

  /* ---------- Drawer móvil ---------- */
  const burger = $('.burger');
  const drawer = $('#drawer');
  function closeDrawer() {
    if (!drawer || drawer.hidden) return;
    drawer.hidden = true;
    burger?.setAttribute('aria-expanded', 'false');
  }
  burger?.addEventListener('click', () => {
    const willOpen = drawer.hidden;
    drawer.hidden = !willOpen;
    burger.setAttribute('aria-expanded', String(willOpen));
  });
  $$('a', drawer || document.createElement('div')).forEach(a => a.addEventListener('click', closeDrawer));

  /* ---------- Reveal on scroll ---------- */
  const revealEls = $$('[data-reveal]');
  if ('IntersectionObserver' in window && !reduceMotion) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(en => { if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
    revealEls.forEach(el => io.observe(el));
  } else {
    revealEls.forEach(el => el.classList.add('is-in'));
  }

  /* ---------- Contadores ---------- */
  const counters = $$('[data-count]');
  const runCounter = (el) => {
    const target = +el.dataset.count;
    if (reduceMotion) { el.textContent = target; return; }
    const dur = 1500; const t0 = performance.now();
    const tick = (t) => {
      const p = clamp((t - t0) / dur, 0, 1);
      el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  if ('IntersectionObserver' in window) {
    const cio = new IntersectionObserver((entries) => {
      entries.forEach(en => { if (en.isIntersecting) { runCounter(en.target); cio.unobserve(en.target); } });
    }, { threshold: 0.6 });
    counters.forEach(c => cio.observe(c));
  } else counters.forEach(runCounter);

  /* ---------- Mockup del producto: escala + inclinación según scroll ---------- */
  const device = $('[data-device]');
  const screen = $('[data-screen]');
  const app = screen && $('.app', screen);
  if (screen && app) {
    const fit = () => app.style.setProperty('--s', screen.clientWidth / 1000);
    fit();
    new ResizeObserver(fit).observe(screen);
  }
  if (device && !reduceMotion) {
    let ticking = false;
    const update = () => {
      const r = device.getBoundingClientRect();
      const p = clamp((innerHeight - r.top) / (innerHeight * 0.62), 0, 1);
      device.style.setProperty('--p', p.toFixed(3));
      ticking = false;
    };
    addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    addEventListener('resize', update);
    update();
  } else if (device) {
    device.style.setProperty('--p', 1);
  }

  /* ---------- Marquee de clientes: duplica el contenido para loop continuo ---------- */
  $$('[data-marquee]').forEach(m => {
    const track = $('.marquee-track', m);
    if (!track || reduceMotion) return;
    [...track.children].forEach(n => {
      const c = n.cloneNode(true);
      c.alt = ''; c.setAttribute('aria-hidden', 'true');
      track.appendChild(c);
    });
  });

  /* ---------- Hub de subsistemas SAMAN SOLUTION ---------- */
  const hubWrap = $('[data-hub]');
  if (hubWrap) {
    const hub = $('.hub', hubWrap);
    const nodes = $$('.node', hub);
    const panes = $$('.pane', hubWrap);
    const lines = $('.hub-lines', hub);
    const progress = $('.detail-progress', hubWrap);
    const R = 39;
    let index = 0;
    let auto = !reduceMotion;
    let hovering = false;
    let inView = false;
    let timer;

    // posiciona nodos (CSS lee --a) y dibuja líneas desde el centro
    const ns = 'http://www.w3.org/2000/svg';
    nodes.forEach((n, i) => {
      const a = +n.dataset.angle;
      n.style.setProperty('--a', a + 'deg');
      const line = document.createElementNS(ns, 'line');
      const rad = a * Math.PI / 180;
      line.setAttribute('x1', 50); line.setAttribute('y1', 50);
      line.setAttribute('x2', (50 + R * Math.cos(rad)).toFixed(2));
      line.setAttribute('y2', (50 + R * Math.sin(rad)).toFixed(2));
      line.style.setProperty('--c', n.style.getPropertyValue('--c'));
      lines.appendChild(line);
    });
    const lineEls = $$('line', lines);

    // "Integrado con": enlaza cada subsistema con los demás (todos se conectan al mismo sistema)
    panes.forEach((pane, pi) => {
      const box = document.createElement('div');
      box.className = 'integrates';
      box.innerHTML = '<span class="mono">Integrado con</span>';
      nodes.forEach((n, ni) => {
        if (ni === pi) return;
        const b = document.createElement('button');
        b.type = 'button';
        b.style.setProperty('--c', n.style.getPropertyValue('--c'));
        b.innerHTML = '<i></i>' + n.textContent.trim();
        b.addEventListener('click', () => { stopAuto(); select(ni); });
        box.appendChild(b);
      });
      pane.appendChild(box);
    });

    const restartProgress = () => {
      progress.classList.remove('run');
      void progress.offsetWidth;
      if (auto && inView && !hovering) progress.classList.add('run');
    };

    const select = (i, { focus = false } = {}) => {
      index = (i + nodes.length) % nodes.length;
      nodes.forEach((n, k) => {
        const on = k === index;
        n.classList.toggle('is-active', on);
        n.setAttribute('aria-selected', String(on));
        n.tabIndex = on ? 0 : -1;
        lineEls[k].classList.toggle('is-active', on);
      });
      panes.forEach((p, k) => { p.hidden = k !== index; });
      if (focus) nodes[index].focus();
      restartProgress();
      schedule();
    };

    const schedule = () => {
      clearTimeout(timer);
      if (!auto || !inView || hovering) return;
      timer = setTimeout(() => select(index + 1), 7000);
    };

    const stopAuto = () => { auto = false; clearTimeout(timer); progress.classList.remove('run'); progress.style.opacity = 0; };

    nodes.forEach((n, i) => {
      n.addEventListener('click', () => { stopAuto(); select(i); });
      n.addEventListener('keydown', e => {
        const next = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key];
        if (next) { e.preventDefault(); stopAuto(); select(index + next, { focus: true }); }
      });
    });
    $('[data-hub-prev]', hubWrap).addEventListener('click', () => { stopAuto(); select(index - 1); });
    $('[data-hub-next]', hubWrap).addEventListener('click', () => { stopAuto(); select(index + 1); });

    hubWrap.addEventListener('mouseenter', () => { hovering = true; clearTimeout(timer); progress.classList.remove('run'); });
    hubWrap.addEventListener('mouseleave', () => { hovering = false; restartProgress(); schedule(); });

    new IntersectionObserver(([en]) => {
      inView = en.isIntersecting;
      restartProgress(); schedule();
    }, { threshold: 0.35 }).observe(hubWrap);

    select(0);
  }

  /* ---------- FAQ (acordeón) ---------- */
  $$('.acc-item').forEach(item => {
    const btn = $('.acc-q', item);
    btn.addEventListener('click', () => {
      const open = !item.classList.contains('is-open');
      $$('.acc-item.is-open').forEach(o => { o.classList.remove('is-open'); $('.acc-q', o).setAttribute('aria-expanded', 'false'); });
      if (open) { item.classList.add('is-open'); btn.setAttribute('aria-expanded', 'true'); }
    });
  });

  /* ---------- Formulario (maqueta: sin backend) ---------- */
  const form = $('[data-form]');
  if (form) {
    form.addEventListener('submit', e => {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      $('.form-ok', form).hidden = false;
      form.reset();
    });
  }
})();
