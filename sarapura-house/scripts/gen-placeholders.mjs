// Genera placeholders SVG arquitectónicos para la galería.
// Ejecutar: node scripts/gen-placeholders.mjs
// Reemplazá estos SVG por fotos reales (.jpg/.webp) y actualizá las rutas en src/data/content.ts.

import { writeFileSync, mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const OUT = join(__dirname, '..', 'public', 'gallery');
mkdirSync(OUT, { recursive: true });

const W = 1600;
const H = 1200;

// Paleta cálida coherente con el sitio
const palettes = [
  ['#e9ddc8', '#cdb189', '#9a6b3f'],
  ['#efe7da', '#d8c4a4', '#7c5430'],
  ['#e4d6bd', '#c2a677', '#6b4a2c'],
  ['#f1eadd', '#dac9a8', '#8a6438'],
];

const grain = `
  <filter id="n">
    <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/>
    <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.04 0"/>
    <feComposite operator="over" in2="SourceGraphic"/>
  </filter>`;

const frame = (inner, [a, b, c], label) => `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="${label}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="${a}"/>
      <stop offset="1" stop-color="${b}"/>
    </linearGradient>
    ${grain}
  </defs>
  <rect width="${W}" height="${H}" fill="url(#bg)"/>
  <g stroke="${c}" stroke-width="3" fill="none" opacity="0.55" stroke-linecap="round" stroke-linejoin="round">
    ${inner}
  </g>
  <rect width="${W}" height="${H}" fill="transparent" filter="url(#n)"/>
  <g opacity="0.4">
    <rect x="40" y="40" width="${W - 80}" height="${H - 80}" fill="none" stroke="${c}" stroke-width="2"/>
  </g>
  <text x="${W / 2}" y="${H - 70}" text-anchor="middle" font-family="Georgia, serif" font-size="42" fill="${c}" opacity="0.85" font-style="italic">${label}</text>
</svg>`;

// Motivos arquitectónicos
const facade = `
  <rect x="500" y="220" width="600" height="760"/>
  <line x1="500" y1="360" x2="1100" y2="360"/>
  <line x1="500" y1="660" x2="1100" y2="660"/>
  ${[600, 800, 1000].map((x) => `<rect x="${x - 35}" y="420" width="70" height="160" rx="35 35 0 0"/><rect x="${x - 35}" y="720" width="70" height="160" rx="35 35 0 0"/>`).join('')}
  <path d="M480 220 L800 90 L1120 220"/>
  <rect x="740" y="820" width="120" height="160" rx="60 60 0 0"/>`;

const hall = `
  <path d="M200 980 L200 300 Q200 240 260 240 L1340 240 Q1400 240 1400 300 L1400 980"/>
  <line x1="200" y1="640" x2="1400" y2="640"/>
  ${[420, 800, 1180].map((x) => `<line x1="${x}" y1="240" x2="${x}" y2="980"/>`).join('')}
  <path d="M620 980 L620 720 L980 720 L980 980"/>
  <circle cx="800" cy="430" r="60"/>`;

const window = `
  <rect x="560" y="200" width="480" height="800" rx="240 240 0 0"/>
  <line x1="560" y1="600" x2="1040" y2="600"/>
  <line x1="800" y1="200" x2="800" y2="1000"/>
  ${[680, 920].map((x) => `<line x1="${x}" y1="320" x2="${x}" y2="1000"/>`).join('')}
  <path d="M560 440 Q800 360 1040 440"/>`;

const room = `
  <path d="M260 940 L260 360 L1340 360 L1340 940"/>
  <path d="M260 360 L520 540 L1080 540 L1340 360"/>
  <line x1="520" y1="540" x2="520" y2="940"/>
  <line x1="1080" y1="540" x2="1080" y2="940"/>
  <rect x="640" y="640" width="320" height="300"/>`;

const library = `
  ${[360, 520, 680, 840].map((y) => `<line x1="280" y1="${y}" x2="800" y2="${y}"/>`).join('')}
  ${[320, 440, 560, 680, 760].map((x) => `<line x1="${x}" y1="320" x2="${x}" y2="900"/>`).join('')}
  <rect x="880" y="420" width="440" height="480" rx="220 220 0 0"/>
  <line x1="1100" y1="420" x2="1100" y2="900"/>`;

const detail = `
  <circle cx="800" cy="600" r="260"/>
  <circle cx="800" cy="600" r="160"/>
  ${Array.from({ length: 12 }, (_, i) => {
    const a = (i / 12) * Math.PI * 2;
    return `<line x1="${800 + Math.cos(a) * 160}" y1="${600 + Math.sin(a) * 160}" x2="${800 + Math.cos(a) * 260}" y2="${600 + Math.sin(a) * 260}"/>`;
  }).join('')}
  <circle cx="800" cy="600" r="70"/>`;

const stairs = `
  <path d="M300 980 L300 200"/>
  ${Array.from({ length: 9 }, (_, i) => `<path d="M${300 + i * 90} ${980 - i * 86} h160 v-86"/>`).join('')}
  <path d="M300 200 Q900 260 1300 200" />
  <line x1="1300" y1="200" x2="1300" y2="520"/>`;

const terrace = `
  <line x1="160" y1="760" x2="1440" y2="760"/>
  ${[300, 520, 740, 960, 1180].map((x) => `<rect x="${x - 60}" y="500" width="120" height="260" rx="60 60 0 0"/>`).join('')}
  <path d="M260 500 L420 380 L560 500"/>
  <circle cx="1180" cy="300" r="90"/>
  <line x1="160" y1="900" x2="1440" y2="900"/>`;

const map = `
  ${[300, 600, 900, 1200].map((x) => `<line x1="${x}" y1="120" x2="${x - 120}" y2="1080"/>`).join('')}
  ${[300, 540, 780, 1020].map((y) => `<line x1="80" y1="${y}" x2="1520" y2="${y - 60}"/>`).join('')}
  <circle cx="800" cy="560" r="26" fill="${'#7c5430'}" opacity="0.9"/>`;

const items = [
  { name: 'fachada', motif: facade, label: 'Fachada · 1912', p: 0 },
  { name: 'hall', motif: hall, label: 'Hall de entrada', p: 1 },
  { name: 'vitral', motif: window, label: 'Vitral original', p: 2 },
  { name: 'salas', motif: room, label: 'Salas de trabajo', p: 0 },
  { name: 'biblioteca', motif: library, label: 'Biblioteca', p: 1 },
  { name: 'detalle', motif: detail, label: 'Detalle · yesería', p: 2 },
  { name: 'escalera', motif: stairs, label: 'Escalera imperial', p: 0 },
  { name: 'terraza', motif: terrace, label: 'Terraza · Monserrat', p: 1 },
  { name: 'mapa', motif: map, label: 'Monserrat · Buenos Aires', p: 2 },
];

for (const it of items) {
  const pal = palettes[it.p].map((c) => c.replace(/\s/g, ''));
  writeFileSync(join(OUT, `${it.name}.svg`), frame(it.motif, pal, it.label).trim());
  console.log('✓', `${it.name}.svg`);
}

// Favicon
const fav = `<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="14" fill="#1a1714"/>
  <text x="32" y="45" text-anchor="middle" font-family="'Jost','Century Gothic',sans-serif" font-weight="500" font-size="38" fill="#c89a5b">S</text>
</svg>`;
writeFileSync(join(__dirname, '..', 'public', 'favicon.svg'), fav.trim());
console.log('✓ favicon.svg');
