# Visuell stilguide

## Naturtyper

| Naturtyp | Bakgrund | Ikonkälla | Brickskala |
|---|---|---|---:|
| Skog | `#C8E3A0` | `assets/icons/forest.svg` | 0,406 |
| Sjö | `#B9DDF3` | `assets/icons/lake.svg` | 0,406 |
| Äng | `#F7E28A` | `assets/icons/meadow.svg` | 0,3654 |
| Berg | `#D9D9D9` | `assets/icons/mountain.svg` | 0,406 |
| Våtmark | `#A9D9DF` | `assets/icons/wetland.svg` | 0,406 |

Våtmarkens bakgrund är avsiktligt blågrön och ligger visuellt mellan Skog och Sjö.

## Källor och output

- Ikonerna i `assets/icons/` är återanvändbara masterfiler.
- Färger och ikonstorlekar definieras i `data/style.yaml`.
- Brickfördelningen definieras i `data/tiles.yaml`.
- `scripts/build_landscape_tiles.py` bygger SVG-ark och PDF.
- Filer i `output/print/` är genererad output och ska inte vara enda källa.

## Regelikon: Valfri naturtyp

| Symbol | Fil | Användning |
|---|---|---|
| `?` i streckad ruta | `assets/icons/any-terrain.svg` | Visar att vilken naturtyp som helst får ligga på platsen |

Symbolen är inte en spelbar naturtyp och finns inte på landskapsbrickorna.
