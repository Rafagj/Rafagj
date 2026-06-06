# Sarapura house — landing

Landing tipo *showcase* / galería para **Sarapura house**: las oficinas de Sarapura
en un edificio histórico de Buenos Aires. Construida con [Astro](https://astro.build)
como sitio estático (sin dependencias de runtime, deploy en cualquier hosting estático).

## Estructura

```
sarapura-house/
├── public/
│   ├── gallery/          # imágenes de la galería y secciones (SVG placeholder)
│   └── favicon.svg
├── scripts/
│   └── gen-placeholders.mjs   # genera los SVG placeholder
└── src/
    ├── components/       # Header, Hero, Intro, Gallery, Spaces, Timeline, Location, Contact, Footer
    ├── data/content.ts   # ← TODO el contenido editable (textos, datos, galería)
    ├── layouts/Layout.astro
    ├── pages/index.astro
    └── styles/global.css # sistema de diseño (paleta, tipografías)
```

## Desarrollo

```bash
npm install
npm run dev        # http://localhost:4321
npm run build      # genera dist/
npm run preview    # sirve el build de producción
```

## Editar el contenido

Casi todo se edita desde **`src/data/content.ts`**:

- `site` — nombre, tagline, dirección, email, teléfono, Instagram.
- `nav` — ítems del menú.
- `stats` — cifras destacadas de la casa.
- `spaces` — los ambientes (título, texto, imagen).
- `timeline` — la línea de tiempo / historia.
- `gallery` — imágenes de la galería (con `span: 'normal' | 'wide' | 'tall'`).

Los colores y tipografías están en `src/styles/global.css` (variables CSS en `:root`).

## Reemplazar los placeholders por fotos reales

Las imágenes actuales son **SVG placeholder** generados automáticamente. Para usar fotos reales:

1. Copiá tus fotos a `public/gallery/` (recomendado `.webp` o `.jpg` optimizados).
2. Actualizá las rutas en `src/data/content.ts` (`gallery`, `spaces`) y, si cambian
   los nombres, también las referencias en `Hero.astro` (`fachada`) y `Contact.astro` (`terraza`).
3. Listo — el lightbox, el grid y las secciones toman las nuevas imágenes automáticamente.

> Para regenerar los placeholders: `node scripts/gen-placeholders.mjs`

## Deploy

El build genera `dist/` estático. Funciona en Netlify, Vercel, Cloudflare Pages,
GitHub Pages, etc. Si vas a deployar bajo un subpath (ej. GitHub Pages),
descomentá y ajustá `base` en `astro.config.mjs`.

## Notas

- Los datos de dirección/teléfono/email son **placeholder** — reemplazalos por los reales en `content.ts`.
- Accesible: navegación por teclado en el lightbox (← → Esc), `prefers-reduced-motion` respetado.
