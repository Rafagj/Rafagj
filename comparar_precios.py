#!/usr/bin/env python3
"""
Comparador de precios de supermercados argentinos (Precios Claros).

Compara una canasta de ~50 productos IDÉNTICOS entre las cadenas:
    Coto, Carrefour, Dia, Disco y Jumbo

Usa la API pública del portal oficial Precios Claros (preciosclaros.gob.ar),
que releva precios de góndola informados por las propias cadenas.

NOTA SOBRE EL ENTORNO
---------------------
La API de Precios Claros suele estar geo-restringida a IPs de Argentina y el
sitio rota periódicamente su `x-api-key` y el host de su CDN. Si el script
falla con 403/401:
  1) Abrí https://www.preciosclaros.gob.ar en el navegador.
  2) En DevTools > Network mirá cualquier request a la API y copiá el header
     `x-api-key` y el host base (campos API_KEY y API_BASE más abajo).
Por eso este script NO puede ejecutarse desde sandboxes con la red filtrada;
corrélo desde una conexión en Argentina.

Salida:
    comparacion_resultado.csv  -> precio por producto y cadena
    + un ranking impreso en consola con el supermercado más barato.

Uso:
    python comparar_precios.py                 # AMBA por defecto
    python comparar_precios.py --lat -34.6 --lng -58.4 --radio 15
"""

from __future__ import annotations

import argparse
import csv
import sys
import time
from dataclasses import dataclass, field

import requests

# --- Configuración de la API (puede requerir actualización, ver docstring) ---
API_BASE = "https://d3e6htiiul5ek9.cloudfront.net/prod"
API_KEY = "fj4xnyyqf45opklbhh8sj37r2bb1dipi"  # clave pública del portal (rota)

HEADERS = {
    "x-api-key": API_KEY,
    "User-Agent": "Mozilla/5.0 (comparador-canasta)",
    "Referer": "https://www.preciosclaros.gob.ar/",
}

# Nombres tal como aparecen en `comercioRazonSocial` / `banderaDescripcion`.
CADENAS = {
    "Coto": ["coto"],
    "Carrefour": ["carrefour"],
    "Dia": ["dia argentina", "dia "],
    "Disco": ["disco"],
    "Jumbo": ["jumbo"],
}

# --- Canasta de 50 productos idénticos (marca líder + presentación) ----------
# Se busca por texto; el script toma la mejor coincidencia por cadena.
PRODUCTOS = [
    "Leche entera La Serenisima 1L sachet",
    "Aceite girasol Natura 1.5L",
    "Aceite de girasol Cocinero 1.5L",
    "Arroz largo fino Gallo Oro 1kg",
    "Fideos guiseros Matarazzo 500g",
    "Fideos spaghetti Lucchetti 500g",
    "Harina de trigo 000 Blancaflor 1kg",
    "Azucar Ledesma 1kg",
    "Yerba mate Playadito 1kg",
    "Yerba mate Taragui 1kg",
    "Cafe La Virginia molido 500g",
    "Cafe instantaneo Nescafe Dolca 170g",
    "Te Green Hills 25 saquitos",
    "Sal fina Celusal 500g",
    "Pure de tomate Arcor 520g",
    "Tomate triturado La Campagnola 520g",
    "Arvejas Arcor lata 350g",
    "Atun al natural La Campagnola 170g",
    "Mayonesa Hellmanns 500g",
    "Ketchup Hellmanns 500g",
    "Mostaza Savora 250g",
    "Mermelada Arcor durazno 390g",
    "Dulce de leche La Serenisima 400g",
    "Galletitas Oreo 118g",
    "Galletitas crackers Express 100g",
    "Pan lactal Bimbo 460g",
    "Manteca La Serenisima 200g",
    "Queso cremoso La Paulina 500g",
    "Yogur bebible Ser frutilla 900g",
    "Huevos blancos docena",
    "Harina leudante Pureza 1kg",
    "Polenta Presto Pronta 500g",
    "Lentejas secas 400g",
    "Garbanzos secos 400g",
    "Gaseosa Coca-Cola 2.25L",
    "Gaseosa Sprite 2.25L",
    "Agua mineral Villavicencio 2L",
    "Jugo en polvo Tang naranja 18g",
    "Cerveza Quilmes 1L",
    "Vino tinto Termidor 1L",
    "Papel higienico Elite 4 rollos",
    "Rollo de cocina Sussex x2",
    "Servilletas Elite 100u",
    "Detergente Magistral 750ml",
    "Jabon en polvo Skip 800g",
    "Suavizante Vivere 900ml",
    "Lavandina Ayudin 1L",
    "Jabon de tocador Lux 125g",
    "Shampoo Sedal 340ml",
    "Pasta dental Colgate 90g",
]


@dataclass
class Sucursal:
    id: str
    cadena: str
    nombre: str


@dataclass
class FilaProducto:
    descripcion: str
    precios: dict = field(default_factory=dict)  # cadena -> (precio, nombre_real)


def _get(path: str, params: dict) -> dict:
    """GET con reintentos y backoff exponencial ante errores de red."""
    url = f"{API_BASE}{path}"
    for intento in range(4):
        try:
            r = requests.get(url, headers=HEADERS, params=params, timeout=20)
            if r.status_code == 200:
                return r.json()
            if r.status_code in (401, 403):
                raise SystemExit(
                    f"\nLa API devolvio {r.status_code}. La x-api-key o el host "
                    f"caducaron, o tu IP no es de Argentina. Ver instrucciones "
                    f"en el docstring del script."
                )
            print(f"  HTTP {r.status_code}, reintento {intento + 1}/4...")
        except requests.RequestException as e:
            print(f"  Error de red ({e}), reintento {intento + 1}/4...")
        time.sleep(2 ** (intento + 1))
    raise SystemExit("No se pudo contactar la API tras 4 reintentos.")


def resolver_sucursales(lat: float, lng: float) -> dict:
    """Devuelve una sucursal representativa por cada cadena objetivo."""
    print("Buscando sucursales cercanas...")
    data = _get(
        "/sucursales",
        {"lat": lat, "lng": lng, "limit": 100, "offset": 0},
    )
    elegidas: dict = {}
    for suc in data.get("sucursales", []):
        etiqueta = (
            f"{suc.get('comercioRazonSocial', '')} "
            f"{suc.get('banderaDescripcion', '')}"
        ).lower()
        for cadena, claves in CADENAS.items():
            if cadena in elegidas:
                continue
            if any(k in etiqueta for k in claves):
                elegidas[cadena] = Sucursal(
                    id=suc["id"],
                    cadena=cadena,
                    nombre=f"{suc.get('banderaDescripcion','')} - "
                    f"{suc.get('direccion','')}",
                )
    for cadena in CADENAS:
        estado = "OK" if cadena in elegidas else "NO ENCONTRADA en la zona"
        print(f"  {cadena:10s}: {estado}")
    return elegidas


def precio_en_sucursal(termino: str, sucursal: Sucursal) -> tuple | None:
    """Mejor coincidencia (menor precio) de `termino` en una sucursal."""
    data = _get(
        "/productos",
        {
            "string": termino,
            "id_sucursal": sucursal.id,
            "limit": 5,
            "offset": 0,
        },
    )
    productos = data.get("productos", [])
    candidatos = [p for p in productos if p.get("precioLista")]
    if not candidatos:
        return None
    mejor = min(candidatos, key=lambda p: p["precioLista"])
    return (float(mejor["precioLista"]), mejor.get("nombre", termino))


def comparar(sucursales: dict) -> list:
    filas = []
    for i, termino in enumerate(PRODUCTOS, 1):
        print(f"[{i:2d}/{len(PRODUCTOS)}] {termino}")
        fila = FilaProducto(descripcion=termino)
        for cadena, suc in sucursales.items():
            res = precio_en_sucursal(termino, suc)
            if res:
                fila.precios[cadena] = res
            time.sleep(0.3)  # cortesia con la API
        filas.append(fila)
    return filas


def exportar_csv(filas: list, cadenas: list, ruta: str) -> None:
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Producto"] + cadenas)
        for fila in filas:
            w.writerow(
                [fila.descripcion]
                + [
                    f"{fila.precios[c][0]:.2f}" if c in fila.precios else ""
                    for c in cadenas
                ]
            )
    print(f"\nCSV escrito en {ruta}")


def ranking(filas: list, cadenas: list) -> None:
    """Suma de la canasta restringida a productos presentes en TODAS las cadenas."""
    comparables = [f for f in filas if all(c in f.precios for c in cadenas)]
    print(
        f"\n{len(comparables)}/{len(filas)} productos estan disponibles en las "
        f"{len(cadenas)} cadenas (canasta comparable)."
    )
    if not comparables:
        print("No hay productos comunes para rankear.")
        return

    totales = {c: sum(f.precios[c][0] for f in comparables) for c in cadenas}
    orden = sorted(totales.items(), key=lambda kv: kv[1])
    barato = orden[0][1]

    print("\n=== RANKING DE LA CANASTA (mas barato primero) ===")
    for pos, (cadena, total) in enumerate(orden, 1):
        dif = (total / barato - 1) * 100
        extra = "(MAS BARATO)" if pos == 1 else f"(+{dif:.1f}%)"
        print(f"  {pos}. {cadena:10s} ${total:>12,.2f}  {extra}")

    g, _ = orden[0]
    print(f"\n>>> Mejor precio global: {g}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Comparador de canasta de supermercados")
    ap.add_argument("--lat", type=float, default=-34.6037, help="Latitud (def: CABA)")
    ap.add_argument("--lng", type=float, default=-58.3816, help="Longitud (def: CABA)")
    ap.add_argument("--out", default="comparacion_resultado.csv")
    args = ap.parse_args()

    sucursales = resolver_sucursales(args.lat, args.lng)
    if not sucursales:
        print("No se encontraron sucursales de las cadenas objetivo en la zona.")
        return 1

    filas = comparar(sucursales)
    cadenas = list(sucursales.keys())
    exportar_csv(filas, cadenas, args.out)
    ranking(filas, cadenas)
    return 0


if __name__ == "__main__":
    sys.exit(main())
