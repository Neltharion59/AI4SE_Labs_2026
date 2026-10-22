# Cviko 4. tyzden - Requirements

## Zadanie

Cielom bolo vytvorit agenticku siet, ktora nacita textove dokumenty a vytvori z nich jeden strukturovany dokument softverovych poziadaviek.

## Riesenie

Siet je implementovana v Pythone pomocou LangGraphu:

`nacitanie -> extrakcia -> konsolidacia -> kontrola <-> oprava -> validacia -> vystup`

| Uzol | Typ | Model | Uloha |
| --- | --- | --- | --- |
| `load_documents` | deterministicky | - | Nacita `.txt` a `.eml` subory a rozdeli ich na chunky. |
| `extract_candidates` | LLM | `gpt-4o-mini` | Najde Extracted Items v zdrojovych dokumentoch. |
| `consolidate_requirements` | LLM | `gpt-5-mini` | Spoji duplicity a vytvori navrh poziadaviek. |
| `review_quality` | LLM | `gpt-6-luna` | Kontroluje kvalitu, konzistentnost a uplnost. |
| `revise_requirements` | LLM | `gpt-5-mini` | Opravuje problemy najdene kontrolou. |
| `validate_deterministically` | deterministicky | - | Kontroluje ID, zdroje, priority a pokrytie Extracted Items. |
| `assign_ids_and_render` | deterministicky | - | Vytvori finalny Markdown dokument. |

`gpt-4o-mini` som pouzila na davkovu extrakciu, `gpt-5-mini` na narocnejsie spajanie a opravy a `gpt-6-luna` ako nezavisleho reviewera. Prompty pouzivaju strukturovany vystup a zoznam povolenych ID, aby modely nevymyslali zdroje alebo identifikatory.

Feedback loop je medzi `review_quality` a `revise_requirements`. Pocet oprav je obmedzeny, aby sa siet nezacyklila.

## Spustenie

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

V `.env` musia byt nastavene `OPENAI_API_KEY` a `OPENAI_BASE_URL`.

```powershell
python main.py --input-dir data/corpus --output output/requirements.md
```

## Vysledok

Posledny beh spracoval:

- 20 vstupnych dokumentov,
- 33 Extracted Items,
- 29 finalnych poziadaviek,
- 10 revizii.

Vystup je v subore [output/requirements.md](output/requirements.md). Po 10 reviziach zostali 4 review a 7 validacnych problemov. Zadanie pripusta, ze vystup nemusi splnit vsetky OS poziadavky dokonale, ak ich siet kontroluje a pokusa sa ich opravit.

## Splnenie zadania

- 4 LLM uzly a 3 rozne modely,
- viacero deterministickych uzlov,
- feedback loop medzi kontrolou a opravou,
- implementacia v LangGraphu,
- rekurzivne nacitanie vstupneho adresara bez hardcoded suborov,
- unikatne ID, priority a traceability ku zdrojom,
- kontrola duplicit, konfliktov, uplnosti a blacklistu.

## Odovzdavane subory

- [main.py](main.py) a [requirements_refiner](requirements_refiner/) - implementacia siete,
- [README.md](README.md) - popis riesenia,
- [output/requirements.md](output/requirements.md) - vygenerovany dokument poziadaviek.
