# Comparación de precios: Coto · Carrefour · Día · Disco · Jumbo

_Última actualización: junio 2026_

## TL;DR — ¿Cuál tiene los mejores precios?

**Carrefour** es, de las cinco cadenas, la **más barata para una compra completa**
de productos idénticos (mismas marcas y presentaciones), seguida de cerca por
**Día**. **Coto** queda en una franja media, mientras que **Jumbo** y **Disco**
(ambas del grupo Cencosud, con posicionamiento premium) son sistemáticamente las
**más caras**. Para una misma lista de productos la brecha entre la cadena más
barata y la más cara ronda el **9–20 %**, y en productos puntuales (yerba, café)
puede superar el **40–50 %**.

> ⚠️ **Sobre los datos.** Esta conclusión se apoya en relevamientos
> comparativos públicos de dic-2025 / 2026 (ver Fuentes), **no** en una descarga
> propia de 50 precios: el entorno donde se generó este informe tiene la red
> filtrada y no puede acceder ni a la API oficial ni a las webs de las cadenas.
> Para obtener **tu** tabla exacta de 50 productos con precios en vivo, usá el
> script `comparar_precios.py` incluido en este repo (corrélo desde Argentina).

---

## Por qué Carrefour gana

1. **Marca propia agresiva.** Su línea propia suele ubicarse por debajo del
   promedio del mercado, lo que baja el ticket de la canasta completa.
2. **Lidera o empata en productos clave.** En relevamientos producto-por-producto
   quedó primero o empatado en **yerba, pan y fideos**.
3. **Promos acumulables y convenios bancarios** que potencian el descuento de
   góndola (días de banco, reintegros, etc.).

## Cómo queda cada cadena

| Posición | Cadena | Fortalezas | Debilidades |
|---|---|---|---|
| 🥇 1 | **Carrefour** | Marca propia barata; yerba, pan, fideos; promos bancarias | Frescos menos competitivos que Coto |
| 🥈 2 | **Día** | Secos y marca propia; campañas fuertes (40 % pañales, 3x2, 2x1) | En compra mensual completa la ventaja se diluye; menos variedad en frescos |
| 🥉 3 | **Coto** | **Carnes, pollo y congelados** muy competitivos | Almacén, limpieza y bebidas más caros |
| 4 | **Jumbo** | Surtido amplio, importados y gourmet | Precios altos; perfil premium |
| 5 | **Disco** | Cercanía/experiencia de compra | **La más cara** del relevamiento |

## Ejemplos reales producto-por-producto

- **Café Nescafé Dolca 170 g:** $9.554 en **Día** · $10.240 **Carrefour** ·
  $10.610 **Coto** · $11.225 **Jumbo** → brecha > **$1.600 (≈17 %)**.
- **Yerba mate:** la diferencia entre cadenas para el mismo paquete llegó a
  rozar el **50 %**; Carrefour del lado barato, Jumbo del lado caro.
- **Leche, arroz, papel higiénico:** brecha del orden del **20 %** entre extremos.

## Matices que cambian el resultado

- **Las promos mandan.** Con 3x2 en leche/aceite, cadenas como ChangoMás (fuera
  de tu lista de 5) pueden volverse imbatibles aunque su precio de lista sea más
  alto. Mirar la promo del día puede pesar más que elegir la cadena.
- **No hay ganador único por categoría.** Coto gana en carnicería; Día en secos;
  Carrefour en el agregado. La compra óptima suele ser **mixta**.
- **Varía por zona, día y medio de pago.** Un mismo SKU cambia entre sucursales.

## Metodología recomendada (la que aplica el script)

1. Canasta de **50 productos idénticos**: misma marca, misma presentación (ver
   lista en `comparar_precios.py`).
2. Precio de **lista de góndola sin promociones** (comparación "limpia").
3. Una sucursal representativa por cadena en la misma zona geográfica.
4. Ranking por **suma de la canasta**, restringido a los productos disponibles
   en las 5 cadenas para que la comparación sea justa.

## Fuentes

- iProfesional — [Cuál es el supermercado más barato de Argentina en 2026](https://www.iprofesional.com/actualidad/445916-cual-es-el-supermercado-mas-barato-de-argentina-en-2026)
- iProfesional — [Ranking diciembre 2025: más barato y más caro](https://www.iprofesional.com/negocios/443478-ranking-clave-cual-es-supermercado-mas-barato-y-mas-caro-diciembre-2025)
- iProfesional — [Compra mensual más barata en 2026](https://www.iprofesional.com/economia/443070-cual-es-el-supermercado-mas-barato-para-hacer-la-compra-mensual-en-2026)
- iProfesional — [Cuánto te podés ahorrar entre el más caro y el más barato](https://www.iprofesional.com/economia/438193-productos-de-consumo-masivo-cuanta-plata-te-podes-ahorrar-entre-el-supermercado-mas-caro-y-el-mas-barato)
- Portal oficial — [Precios Claros](https://www.preciosclaros.gob.ar/) (fuente de datos en vivo para el script)
