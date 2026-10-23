import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import * as k from "../../../.agents/skills/anatomy/kit/iso-kit.mjs";
import { kitScript } from "../../../.agents/skills/anatomy/scripts/inline-kit.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));
const OUT = join(HERE, "..", "outputs", "anatomy-mechanism-v001");
mkdirSync(OUT, { recursive: true });
const theme = process.argv.includes("--light") ? "light" : "dark";
const WIDTH = 760, HEIGHT = 520;

const BASE = { x: -126, y: -62, w: 252, d: 124, r: 7 };
const FLOOR_Z = 0, CHAMBER_Z = 16, CHAMBER_H = 76;
const P = k.fitProjection(
  [...k.boxCorners(BASE, -10, 102), [-150, -70, 0], [156, 70, 112]],
  WIDTH, HEIGHT, { pad: 34, azimuth: 46 },
);
const at = (p) => k.iso(p, P);
const S = (paths, style) => k.solidSvg(paths, style);
const L = (d, style) => k.lineSvg(d, style);
const D = (points, style) => k.dotsSvg(points, style);

function slab(plan, z, h, tone = "mid", options = {}) {
  return S(k.slabOf(plan, z, h, P, options.steps ?? 5, options.bevel ?? 0.8), { tone, crease: options.crease ?? "lo", lit: options.lit });
}

function staticMachine() {
  const out = [];
  out.push(`<path class="iso-halo" d="${k.haloOf(BASE, -10, 10, P)}"/>`);
  for (const [x, y] of k.corners(BASE, 13)) {
    out.push(S(k.cylinder(x, y, 7, -10, 4, P, 24), { tone: "lo" }));
  }
  out.push(slab(BASE, -6, 10, "mid", { bevel: 1.2 }));
  out.push(L(k.planOutline(k.insetPlan(BASE, 5), 4, P), { tone: "faint" }));
  out.push(D(k.corners(BASE, 11).map(([x, y]) => at([x, y, 4])), { size: 0.55 }));

  // Chamber floor, rear wall, ribs and top rails.
  out.push(slab({ x: -66, y: -45, w: 150, d: 90, r: 3 }, 4, 12, "mid"));
  out.push(slab({ x: -66, y: 38, w: 150, d: 7, r: 1 }, 16, 78, "mid"));
  for (const x of [-62, -28, 6, 40, 74]) {
    out.push(slab({ x, y: 34, w: 5, d: 8, r: 1 }, 14, 84, "mid", { bevel: 0.5 }));
    out.push(D([at([x + 2.5, 38, 24]), at([x + 2.5, 38, 86])], { size: 0.45 }));
  }
  out.push(slab({ x: -70, y: 31, w: 158, d: 7, r: 1 }, 94, 6, "hi"));
  out.push(slab({ x: -70, y: -45, w: 158, d: 6, r: 1 }, 12, 5, "lo"));

  // Infeed conveyor: bed, six rollers and guards.
  out.push(slab({ x: -148, y: -31, w: 78, d: 62, r: 3 }, 24, 7, "lo"));
  for (let i = 0; i < 6; i++) {
    const x = -140 + i * 12;
    out.push(S(k.cylinder(x, 0, 5, 31, 4, P, 22), { tone: i % 2 ? "mid" : "lo" }));
  }
  out.push(slab({ x: -150, y: -36, w: 84, d: 5, r: 1 }, 25, 18, "mid"));
  out.push(slab({ x: -150, y: 31, w: 84, d: 5, r: 1 }, 25, 18, "mid"));

  // Hydraulic body, flange and fixed guide rails.
  out.push(S(k.cylinder(-91, 0, 17, 40, 44, P, 36), { tone: "mid" }));
  out.push(S(k.cylinder(-91, 0, 20, 39, 5, P, 36), { tone: "hi" }));
  out.push(L(k.sideArc(-91, 0, 17, 57, P, 20), { tone: "faint" }));
  for (const y of [-31, 27]) out.push(slab({ x: -67, y, w: 144, d: 4, r: 1 }, 18, 4, "lo"));

  // Gate rails and header.
  for (const x of [76, 88]) out.push(slab({ x, y: -43, w: 5, d: 86, r: 1 }, 12, 98, "mid"));
  out.push(slab({ x: 73, y: -46, w: 22, d: 92, r: 2 }, 108, 7, "mid"));
  return out.join("");
}

function waste() {
  const out = [];
  const pieces = [
    [-42,-22,34,12,10,8],[-28,-8,38,14,11,10],[-14,12,32,13,10,9],[0,-18,37,11,12,8],
    [14,4,35,14,10,11],[28,18,31,12,9,8],[-34,20,52,11,10,9],[-17,-18,55,13,9,10],
    [2,15,54,12,11,8],[20,-10,51,14,10,9],[37,8,44,11,9,10],[48,-19,36,12,10,8],
  ];
  pieces.forEach(([x,y,z,w,d,h], i) => {
    out.push(slab({ x, y, w, d, r: 2 }, z, h, i % 4 === 0 ? "lit" : i % 3 === 0 ? "hi" : "mid", { bevel: 1.2 }));
  });
  return out.join("");
}

function movingParts() {
  const out = [];
  // Rod, compression/discharge platen, finished bale, four straps and rising gate.
  out.push(`<g data-part="ram"><g data-part="rod">${slab({ x: -74, y: -5, w: 58, d: 10, r: 3 }, 52, 10, "hi", { lit: true })}</g>`);
  out.push(`<g data-part="platen">${slab({ x: -18, y: -34, w: 8, d: 68, r: 2 }, 20, 68, "lit", { lit: true })}</g></g>`);
  out.push(`<g data-part="waste">${waste()}</g>`);
  const baleBody = slab({ x: 10, y: -31, w: 58, d: 62, r: 3 }, 18, 62, "hi", { bevel: 1.5 });
  const straps = [-2, 13, 28, 43].map((dx) => slab({ x: 16 + dx, y: -32, w: 3, d: 64, r: 0.5 }, 17, 65, "lo", { bevel: 0.2 })).join("");
  out.push(`<g data-part="bale" opacity="0">${baleBody}${straps}</g>`);
  out.push(`<g data-part="gate">${slab({ x: 79, y: -38, w: 7, d: 76, r: 2 }, 16, 76, "mid", { bevel: 1.0 })}</g>`);
  return out.join("");
}

const svg = k.figureSvg({
  width: WIDTH,
  height: HEIGHT,
  label: "Interactive isometric concept figure of a horizontal baler. Loose material enters from the left, a hydraulic platen compresses it, the outlet gate rises, and the same platen discharges the finished bale to the right.",
  body: [staticMachine(), movingParts()],
});

const live = `
const P = ${JSON.stringify(P)};
const stage = document.querySelector('.iso-stage');
const waste = stage.querySelector('[data-part="waste"]');
const bale = stage.querySelector('[data-part="bale"]');
const platen = stage.querySelector('[data-part="platen"]');
const rod = stage.querySelector('[data-part="rod"]');
const gate = stage.querySelector('[data-part="gate"]');
const readout = document.querySelector('[data-readout]');
const still = matchMedia('(prefers-reduced-motion: reduce)');
let visible = false, frame = 0, last = 0, clock = 0, manual = null;
const clamp = (v,a,b) => Math.max(a, Math.min(b,v));
const ease = (v) => v*v*(3-2*v);
function model(t) {
  t = ((t % 12) + 12) % 12;
  let phase='feeding', ram=0, lift=0, push=0, compact=0;
  if (t < 2) { phase='feeding'; }
  else if (t < 5.2) { phase='compressing'; compact=ease((t-2)/3.2); ram=compact; }
  else if (t < 7.2) { phase='opening gate'; compact=1; ram=1; lift=ease((t-5.2)/2); }
  else if (t < 10.4) { phase='discharging'; compact=1; ram=1; lift=1; push=ease((t-7.2)/3.2); }
  else { phase='resetting'; const q=ease((t-10.4)/1.6); compact=1-q; ram=1-q; lift=1-q; push=1-q; }
  return {phase,ram,lift,push,compact};
}
function draw(m) {
  const ramX = 70*m.ram + 64*m.push;
  platen.setAttribute('transform', translateAlong(P,[ramX,0,0]));
  rod.setAttribute('transform', translateAlong(P,[ramX*0.5,0,0]) + ' scale(' + (1+ramX/100) + ',1)');
  gate.setAttribute('transform', translateAlong(P,[0,0,74*m.lift]));
  bale.setAttribute('transform', translateAlong(P,[64*m.push,0,0]));
  bale.setAttribute('opacity', String(clamp((m.compact-0.62)/0.25,0,1)));
  waste.setAttribute('opacity', String(1-clamp((m.compact-0.25)/0.62,0,1)));
  waste.setAttribute('transform', translateAlong(P,[35*m.compact,0,-5*m.compact]) + ' scale(' + (1-0.36*m.compact) + ',' + (1-0.08*m.compact) + ')');
  readout.textContent = m.phase + ' · ram ' + Math.round(m.ram*100) + '% · gate ' + Math.round(m.lift*100) + '%';
}
function tick(now) {
  const dt=last?Math.min((now-last)/1000,1/30):1/60; last=now;
  if (manual===null && !still.matches) clock += dt;
  draw(model(manual===null?clock:manual));
  frame = visible && manual===null && !still.matches ? requestAnimationFrame(tick) : 0;
}
function run(){if(!frame&&visible){last=0;frame=requestAnimationFrame(tick)}}
new IntersectionObserver(es=>{visible=es[es.length-1].isIntersecting;if(visible)run()},{rootMargin:'120px 0px'}).observe(stage);
stage.addEventListener('pointermove',e=>{const b=stage.getBoundingClientRect();manual=clamp((e.clientX-b.left)/b.width,0,1)*10.35;draw(model(manual));});
stage.addEventListener('pointerleave',()=>{manual=null;run();});
stage.addEventListener('keydown',e=>{if(!['ArrowLeft','ArrowRight','Home','End',' '].includes(e.key))return;e.preventDefault();if(e.key===' '){manual=null;run();return;}manual=manual??0;if(e.key==='ArrowRight')manual=clamp(manual+1,0,10.35);if(e.key==='ArrowLeft')manual=clamp(manual-1,0,10.35);if(e.key==='Home')manual=0;if(e.key==='End')manual=10.35;draw(model(manual));});
draw(model(0));
`;

const body = k.plateHtml({
  fig: "Fig 1",
  title: "Horizontal baler — concept sequence",
  hint: "Hover to scrub · arrow keys step · Space resumes",
  readout: "feeding · ram 0% · gate 0%",
  keys: [
    { mark: "lit", label: "Main platen: compresses, then continues to discharge" },
    { mark: "raised", label: "Outlet gate rises only after the bale is formed" },
    { mark: "edge", label: "Concept geometry — dimensions and safety logic unverified" },
  ],
  caption: "Loose material enters from the left. The hydraulic platen compresses it into a bale, the outlet gate rises completely, and the same platen continues its stroke to discharge the bale. This is an explanatory motion proxy, not a certified section of a production machine.",
  body: `<div class="iso-stage" tabindex="0" role="slider" aria-label="Horizontal baler sequence. Hover or use arrow keys to inspect feeding, compression, gate opening and discharge." aria-valuemin="0" aria-valuemax="10">${svg}</div>`,
});

const filename = theme === "light" ? "jenailv-baler-anatomy-v001-light.html" : "jenailv-baler-anatomy-v001.html";
writeFileSync(join(OUT, filename), k.pageHtml({ title: "Jenailv baler concept", theme, body, script: kitScript() + live, width: 820 }));
console.log("wrote", join(OUT, filename));
