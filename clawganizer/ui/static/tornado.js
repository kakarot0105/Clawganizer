/**
 * Full-viewport tornado takeover animation.
 * Particles + debris funnel that swallows the screen, then calms.
 */
(function () {
  const canvas = document.getElementById("tornado");
  const ctx = canvas.getContext("2d", { alpha: true });

  let running = false;
  let raf = 0;
  let start = 0;
  let width = 0;
  let height = 0;
  let dpr = 1;
  let particles = [];
  let debris = [];
  let flashes = [];
  let resolveDone = null;

  const DURATION = 4200; // ms of storm before calm handoff
  const LABELS = ["pdf", "jpg", "zip", "mp4", "doc", "png", "dmg", "mp3", "txt", "csv"];

  function resize() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = Math.floor(width * dpr);
    canvas.height = Math.floor(height * dpr);
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  function spawnStorm() {
    particles = [];
    debris = [];
    flashes = [];

    const count = Math.floor(Math.min(1400, width * height * 0.00055));
    for (let i = 0; i < count; i++) {
      particles.push({
        a: Math.random() * Math.PI * 2,
        r: 20 + Math.random() * Math.max(width, height) * 0.62,
        y: Math.random() * height,
        speed: 2.2 + Math.random() * 4.2,
        rise: 0.8 + Math.random() * 2.8,
        size: 1.2 + Math.random() * 3.2,
        shade: 170 + Math.random() * 70,
      });
    }

    const debrisCount = Math.floor(55 + Math.min(90, width / 14));
    for (let i = 0; i < debrisCount; i++) {
      debris.push({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 6,
        vy: (Math.random() - 0.5) * 4,
        rot: Math.random() * Math.PI * 2,
        spin: (Math.random() - 0.5) * 0.25,
        w: 28 + Math.random() * 42,
        h: 16 + Math.random() * 24,
        label: LABELS[i % LABELS.length],
        caught: false,
        life: 1,
      });
    }
  }

  function funnelX(y, t) {
    const cx = width * 0.52 + Math.sin(t * 0.0017) * width * 0.04;
    const narrow = 0.08 + (y / height) * 0.42;
    return { cx, radius: width * narrow };
  }

  function drawBackground(t, intensity) {
    const g = ctx.createLinearGradient(0, 0, 0, height);
    g.addColorStop(0, `rgba(32, 46, 64, ${0.72 * intensity})`);
    g.addColorStop(0.45, `rgba(58, 78, 104, ${0.55 * intensity})`);
    g.addColorStop(1, `rgba(210, 160, 90, ${0.38 * intensity})`);
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, width, height);

    // swirling haze bands
    for (let i = 0; i < 5; i++) {
      const y = ((t * 0.04 + i * 90) % (height + 120)) - 60;
      ctx.fillStyle = `rgba(255,255,255,${0.03 + i * 0.01})`;
      ctx.beginPath();
      ctx.ellipse(width * 0.5, y, width * 0.7, 28 + i * 8, 0, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  function drawFunnel(t, intensity) {
    const layers = 18;
    for (let i = 0; i < layers; i++) {
      const y0 = (i / layers) * height;
      const y1 = ((i + 1) / layers) * height;
      const f0 = funnelX(y0, t);
      const f1 = funnelX(y1, t);
      const wobble = Math.sin(t * 0.008 + i * 0.4) * 10;
      ctx.beginPath();
      ctx.moveTo(f0.cx - f0.radius + wobble, y0);
      ctx.lineTo(f0.cx + f0.radius + wobble, y0);
      ctx.lineTo(f1.cx + f1.radius - wobble * 0.5, y1);
      ctx.lineTo(f1.cx - f1.radius - wobble * 0.5, y1);
      ctx.closePath();
      const alpha = (0.035 + (i / layers) * 0.05) * intensity;
      ctx.fillStyle = `rgba(230, 238, 246, ${alpha})`;
      ctx.fill();
    }

    // core
    const core = ctx.createLinearGradient(width * 0.5, 0, width * 0.5, height);
    core.addColorStop(0, `rgba(255,255,255,${0.18 * intensity})`);
    core.addColorStop(1, `rgba(90, 122, 154,${0.08 * intensity})`);
    ctx.fillStyle = core;
    ctx.beginPath();
    for (let y = 0; y <= height; y += 8) {
      const f = funnelX(y, t);
      const x = f.cx + Math.sin(y * 0.02 + t * 0.01) * 8;
      if (y === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.lineWidth = 10;
    ctx.strokeStyle = `rgba(247,250,252,${0.35 * intensity})`;
    ctx.stroke();
  }

  function stepParticles(dt, t, intensity) {
    for (const p of particles) {
      p.a += (p.speed * dt) / Math.max(40, p.r * 0.08);
      p.y -= p.rise * dt * 0.06 * (0.6 + intensity);
      p.r *= 1 - 0.00035 * dt;
      if (p.y < -20 || p.r < 8) {
        p.y = height + Math.random() * 40;
        p.r = 40 + Math.random() * width * 0.35;
        p.a = Math.random() * Math.PI * 2;
      }
      const f = funnelX(p.y, t);
      const x = f.cx + Math.cos(p.a) * Math.min(p.r, f.radius);
      const y = p.y + Math.sin(p.a * 2) * 3;
      ctx.fillStyle = `rgba(${p.shade},${p.shade + 20},${p.shade + 35},${0.35 + 0.45 * intensity})`;
      ctx.beginPath();
      ctx.arc(x, y, p.size, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  function stepDebris(dt, t, intensity) {
    const cx = width * 0.52;
    for (const d of debris) {
      const f = funnelX(d.y, t);
      const dx = cx - d.x;
      const pull = 0.0008 * intensity * (1 + (d.y / height) * 2);
      d.vx += dx * pull * dt;
      d.vy += (-0.02 - Math.random() * 0.01) * dt * intensity;
      d.vx += (Math.random() - 0.5) * 0.15 * dt;
      d.x += d.vx * 0.05 * dt;
      d.y += d.vy * 0.05 * dt;
      d.rot += d.spin * dt * 0.05;
      d.spin += (Math.random() - 0.5) * 0.002 * dt;

      const dist = Math.hypot(d.x - f.cx, 0);
      if (dist < f.radius * 0.35 && d.y > height * 0.15) {
        d.caught = true;
        d.life -= 0.01 * dt;
        d.w *= 0.992;
        d.h *= 0.992;
      }

      if (d.y < -40 || d.life <= 0) {
        d.x = Math.random() * width;
        d.y = height + 20 + Math.random() * 80;
        d.vx = (Math.random() - 0.5) * 4;
        d.vy = -1 - Math.random() * 2;
        d.life = 1;
        d.w = 28 + Math.random() * 42;
        d.h = 16 + Math.random() * 24;
        d.caught = false;
      }

      ctx.save();
      ctx.translate(d.x, d.y);
      ctx.rotate(d.rot);
      ctx.globalAlpha = Math.max(0, d.life) * (0.55 + 0.4 * intensity);
      ctx.fillStyle = "#f7fafc";
      ctx.strokeStyle = "rgba(26,36,51,0.35)";
      ctx.lineWidth = 1;
      roundRect(-d.w / 2, -d.h / 2, d.w, d.h, 3);
      ctx.fill();
      ctx.stroke();
      ctx.fillStyle = "rgba(26,36,51,0.7)";
      ctx.font = `600 ${Math.max(9, d.h * 0.45)}px Figtree, sans-serif`;
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(d.label, 0, 0);
      ctx.restore();
    }
  }

  function roundRect(x, y, w, h, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.arcTo(x + w, y, x + w, y + h, r);
    ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r);
    ctx.arcTo(x, y, x + w, y, r);
    ctx.closePath();
  }

  function drawWind(t, intensity) {
    ctx.save();
    ctx.strokeStyle = `rgba(247,250,252,${0.12 * intensity})`;
    ctx.lineWidth = 1.5;
    for (let i = 0; i < 24; i++) {
      const y = ((i * 37 + t * 0.25) % height);
      const f = funnelX(y, t);
      const len = 40 + (i % 5) * 18;
      ctx.beginPath();
      ctx.moveTo(f.cx - f.radius - len, y);
      ctx.quadraticCurveTo(f.cx - f.radius * 0.6, y + 8, f.cx - f.radius * 0.2, y);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(f.cx + f.radius + len, y);
      ctx.quadraticCurveTo(f.cx + f.radius * 0.6, y - 8, f.cx + f.radius * 0.2, y);
      ctx.stroke();
    }
    ctx.restore();
  }

  function frame(now) {
    if (!running) return;
    if (!start) start = now;
    const elapsed = now - start;
    const progress = Math.min(1, elapsed / DURATION);
    // ramp up fast, hold, then ease out
    let intensity;
    if (progress < 0.15) intensity = progress / 0.15;
    else if (progress < 0.72) intensity = 1;
    else intensity = 1 - (progress - 0.72) / 0.28;

    const dt = 16;
    ctx.clearRect(0, 0, width, height);
    drawBackground(elapsed, intensity);
    drawFunnel(elapsed, intensity);
    drawWind(elapsed, intensity);
    stepParticles(dt, elapsed, intensity);
    stepDebris(dt, elapsed, intensity);

    // subtle screen shake via CSS variable on canvas
    const shake = intensity > 0.4 ? (Math.random() - 0.5) * 3 * intensity : 0;
    canvas.style.transform = `translate(${shake}px, ${shake * 0.6}px)`;

    if (progress >= 1) {
      finish();
      return;
    }
    raf = requestAnimationFrame(frame);
  }

  function finish() {
    running = false;
    cancelAnimationFrame(raf);
    canvas.style.transform = "";
    if (resolveDone) {
      const done = resolveDone;
      resolveDone = null;
      done();
    }
  }

  window.ClawTornado = {
    play() {
      return new Promise((resolve) => {
        resolveDone = resolve;
        resize();
        spawnStorm();
        start = 0;
        running = true;
        canvas.style.opacity = "1";
        canvas.classList.add("is-active");
        raf = requestAnimationFrame(frame);
      });
    },
    async stop() {
      running = false;
      cancelAnimationFrame(raf);
      canvas.style.transform = "";
      canvas.style.transition = "opacity 0.55s ease";
      canvas.style.opacity = "0";
      await new Promise((r) => setTimeout(r, 560));
      canvas.classList.remove("is-active");
      canvas.style.transition = "";
      ctx.clearRect(0, 0, width, height);
    },
    duration: DURATION,
  };

  window.addEventListener("resize", () => {
    if (running) resize();
  });
})();
