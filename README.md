# Rafa García Juanicó — Estudio profesional

Sitio web estático para **Rafa García Juanicó**, estudio profesional unipersonal en Argentina.

- WhatsApp: [+54 9 11 4192-7700](https://wa.me/5491141927700)
- Email: [hola@rgj.com.ar](mailto:hola@rgj.com.ar)
- Instagram: [@rafagj](https://instagram.com/rafagj)

## Stack

- HTML5 semántico
- CSS moderno (custom properties, grid, clamp, animaciones)
- JavaScript vanilla (sin frameworks ni build)
- Tipografías: [Space Grotesk](https://fonts.google.com/specimen/Space+Grotesk) + [Fraunces](https://fonts.google.com/specimen/Fraunces) (Google Fonts)

## Estructura

```
.
├── index.html     # Página única con todas las secciones
├── styles.css     # Sistema de diseño + componentes
├── script.js      # Menú móvil, smooth scroll, reveal on scroll, formulario
└── README.md
```

## Secciones

1. **Hero** — Mensaje principal con CTA y stats.
2. **Sobre** — Quiénes somos + cita destacada.
3. **Servicios** — 4 áreas de práctica (derecho, contable, estrategia, compliance).
4. **Proceso** — 4 pasos de cómo trabajamos.
5. **CTA banner** — Llamada a la acción intermedia.
6. **Contacto** — Información + formulario validado.

## Cómo correrlo

No requiere build. Simplemente abrí `index.html` en el navegador, o serví la carpeta:

```bash
python3 -m http.server 8000
# luego abrir http://localhost:8000
```

## Personalización rápida

- **Colores y tipografías**: variables CSS en `:root` dentro de `styles.css`.
- **Texto y secciones**: editar directamente `index.html`.
- **Formulario**: el `script.js` simula el envío. Para producción, conectar el `submit` a un servicio como [Formspree](https://formspree.io/), [Resend](https://resend.com/) o un endpoint propio.

## Accesibilidad

- HTML semántico (`header`, `nav`, `main`, `section`, `footer`).
- Contraste alto, foco visible, `aria-*` en interacciones.
- Respeta `prefers-reduced-motion`.
- Navegación por teclado en el menú móvil y las cards.
