// Contenido editable de Sarapura house.
// Cambiá textos, imágenes y datos acá sin tocar los componentes.

export const site = {
  name: 'Sarapura house',
  tagline: 'Una casa con historia, una oficina con presente',
  description:
    'Las oficinas de Sarapura habitan un edificio histórico en el corazón de Buenos Aires. Un patrimonio restaurado donde el trabajo se encuentra con la memoria de la ciudad.',
  address: 'Av. de Mayo 000, Monserrat, Buenos Aires, Argentina',
  neighborhood: 'Monserrat · Buenos Aires',
  email: 'hola@sarapura.house',
  phone: '+54 11 0000 0000',
  instagram: 'https://instagram.com/sarapura',
  year: '1912',
};

export const nav = [
  { label: 'La casa', href: '#la-casa' },
  { label: 'Galería', href: '#galeria' },
  { label: 'Espacios', href: '#espacios' },
  { label: 'Historia', href: '#historia' },
  { label: 'Ubicación', href: '#ubicacion' },
  { label: 'Visitanos', href: '#contacto' },
];

// Cifras / datos destacados de la casa
export const stats = [
  { value: '1912', label: 'Año de construcción' },
  { value: '4', label: 'Plantas restauradas' },
  { value: '6 m', label: 'Altura de cielorrasos' },
  { value: '100%', label: 'Patrimonio recuperado' },
];

// Espacios de la casa
export const spaces = [
  {
    title: 'El hall de entrada',
    text: 'Mármoles originales, una escalera imperial y vitrales que filtran la luz porteña. La primera impresión es, también, la primera historia.',
    image: '/gallery/hall.svg',
  },
  {
    title: 'Las salas de trabajo',
    text: 'Cielorrasos de seis metros, molduras de yesería y ventanales que dan a la avenida. Espacios diáfanos donde las ideas tienen aire para crecer.',
    image: '/gallery/salas.svg',
  },
  {
    title: 'La biblioteca',
    text: 'Boiserie de roble, libros, y un silencio cómodo para pensar. El rincón donde el ritmo baja y la conversación se vuelve profunda.',
    image: '/gallery/biblioteca.svg',
  },
  {
    title: 'La terraza',
    text: 'Sobre los techos de Monserrat, entre cúpulas y mansardas, una terraza para los encuentros, los brindis y los finales de jornada.',
    image: '/gallery/terraza.svg',
  },
];

// Línea de tiempo / historia del edificio
export const timeline = [
  {
    year: '1912',
    title: 'Los cimientos',
    text: 'Se levanta el edificio en plena expansión de la Buenos Aires de principios de siglo, con la impronta del academicismo francés.',
  },
  {
    year: '1940',
    title: 'Una casa señorial',
    text: 'Durante décadas funcionó como residencia y oficinas, testigo del pulso comercial y cultural del centro porteño.',
  },
  {
    year: '2021',
    title: 'La restauración',
    text: 'Un trabajo minucioso devuelve a la luz sus mármoles, vitrales y carpinterías originales, respetando cada detalle del patrimonio.',
  },
  {
    year: 'Hoy',
    title: 'Sarapura house',
    text: 'El edificio renace como hogar de Sarapura: un lugar donde la historia y el trabajo creativo conviven todos los días.',
  },
];

// Galería de imágenes (lightbox).
// Reemplazá los .svg por tus fotos reales en /public/gallery (mantené los nombres o actualizalos acá).
export const gallery = [
  { src: '/gallery/fachada.svg', alt: 'Fachada del edificio histórico de Sarapura house', span: 'tall' },
  { src: '/gallery/hall.svg', alt: 'Hall de entrada con escalera imperial', span: 'wide' },
  { src: '/gallery/vitral.svg', alt: 'Vitral original filtrando la luz', span: 'normal' },
  { src: '/gallery/salas.svg', alt: 'Sala de trabajo con cielorrasos altos', span: 'normal' },
  { src: '/gallery/biblioteca.svg', alt: 'Biblioteca con boiserie de roble', span: 'wide' },
  { src: '/gallery/detalle.svg', alt: 'Detalle de moldura y yesería', span: 'normal' },
  { src: '/gallery/escalera.svg', alt: 'Escalera de mármol y baranda de bronce', span: 'tall' },
  { src: '/gallery/terraza.svg', alt: 'Terraza sobre los techos de Monserrat', span: 'wide' },
];
