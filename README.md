# Klasyfikacja efektywności sklepów obuwniczych

Projekt studencki z kursu **Hurtownie danych**. Aplikacja buduje prosty pipeline analityczny dla sieci sklepów obuwniczych: importuje dane CSV, waliduje je, ładuje do SQLite, tworzy model gwiazdy, agreguje sprzedaż do poziomu sklep + miesiąc i klasyfikuje efektywność oddziałów algorytmem kNN.

## Cel biznesowy

Celem jest wsparcie porównywania oddziałów sieci sklepów: wykrywanie słabszych placówek, analiza wpływu rabatów i zwrotów, ocena sprzedaży na pracownika oraz wskazanie sklepów o wysokiej efektywności.

## Wymagania

- Python 3.10+
- pandas
- numpy
- scikit-learn
- matplotlib
- pytest

Instalacja zależności:

```bash
pip install -r requirements.txt
```

## Uruchomienie

Wygenerowanie danych testowych, zapis do CSV i pełny pipeline:

```bash
python main.py --source generated
```

Import istniejących plików CSV z `data/input/` i pełny pipeline:

```bash
python main.py --source csv
```

Tryb `generated` nie omija importera. Przepływ to: generator danych -> CSV -> walidator -> importer -> SQLite -> agregacja -> kNN -> wykresy -> raporty.

## Struktura katalogów

```text
src/              kod aplikacji
tests/            testy pytest
data/input/       wejściowe pliki CSV
data/output/      baza SQLite
output/plots/     wykresy PNG
docs/             dokumentacja techniczna
reports/          raporty i wyniki modelu
```

## Pipeline

1. Utworzenie wymaganych katalogów.
2. Opcjonalne wygenerowanie danych CSV.
3. Walidacja struktury i spójności danych.
4. Utworzenie tabel SQLite w modelu gwiazdy.
5. Import danych do tabel wymiarów i tabeli faktów.
6. Agregacja do `store_monthly_performance`.
7. Obliczenie `performance_score` i klas percentylowych.
8. Trenowanie i ocena modelu kNN.
9. Zapis wykresów i raportów.

## Wyniki

- Baza SQLite: `data/output/shoe_stores_dw.sqlite`
- Wykresy: `output/plots/`
- Raport techniczny: `reports/technical_report.md`
- Wyniki modelu: `reports/model_results.md`
- Podsumowanie: `reports/summary.md`

## Testy

```bash
pytest
```
