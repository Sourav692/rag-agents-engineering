// Animated diagrams (inlined into index.html for modules with animated diagrams): step through each .anim figure.
// It plays while at least half of it is on screen and stops when it leaves; with reduced motion it never
// plays by itself and opens on the finished frame. Without script the figure already shows that frame.
for (const fig of document.querySelectorAll(".anim")) {
  const steps = [...fig.querySelectorAll(".anim__steps button")];
  const controls = fig.querySelector(".anim__controls");
  const play = fig.querySelector('[data-act="play"]');
  const tok = fig.querySelector(".tok");
  const still = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const n = steps.length;
  let cur = n, timer = null, chosen = false;

  const show = (k) => {
    cur = k;
    fig.dataset.step = k;
    for (let i = 1; i <= n; i++) fig.classList.toggle(`s${i}`, i <= k);
    steps.forEach((b, i) => (i + 1 === k ? b.setAttribute("aria-current", "step") : b.removeAttribute("aria-current")));
    const at = steps[k - 1]?.dataset.tok;
    if (tok && at) tok.style.transform = `translate(${at.split(",").map((v) => `${v}px`).join(", ")})`;
  };
  const stop = () => {
    clearInterval(timer);
    timer = null;
    play.setAttribute("aria-pressed", "false");
    play.textContent = "Play";
  };
  const start = () => {
    if (timer) return;
    if (cur >= n) show(1);
    play.setAttribute("aria-pressed", "true");
    play.textContent = "Pause";
    let rest = 0;  // hold the finished frame for two ticks before starting over
    timer = setInterval(() => {
      if (cur < n) show(cur + 1);
      else if (++rest > 2) { rest = 0; show(1); }
    }, 2200);
  };

  fig.classList.add("is-anim");
  controls.hidden = false;
  show(n);
  play.addEventListener("click", () => { chosen = true; timer ? stop() : start(); });
  fig.querySelector('[data-act="prev"]').addEventListener("click", () => { chosen = true; stop(); show(Math.max(1, cur - 1)); });
  fig.querySelector('[data-act="next"]').addEventListener("click", () => { chosen = true; stop(); show(Math.min(n, cur + 1)); });
  steps.forEach((b, i) => b.addEventListener("click", () => { chosen = true; stop(); show(i + 1); }));
  if (!still && "IntersectionObserver" in window) {
    new IntersectionObserver(([e]) => {
      if (chosen) return;  // once the reader takes over, only the reader plays it
      if (e.isIntersecting) start();
      else stop();
    }, { threshold: 0.5 }).observe(fig);
  }
}
