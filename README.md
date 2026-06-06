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
- streamlit
- plotly
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

Szczegółowa specyfikacja formatu plików CSV znajduje się w [docs/csv_import_specification.md](docs/csv_import_specification.md). Dokument opisuje wymagane pliki, kolumny, typy danych, relacje i najczęstsze błędy importu.

Import CSV obsługuje dane z dowolnego roku albo zakresu lat. Warunkiem jest poprawny plik `dim_date.csv` oraz spójne odwołania `date_id` w `fact_sales.csv`.

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
- Dane miesięczne dashboardu: `output/store_monthly_performance.csv`
- Podsumowanie oddziałów: `output/store_summary.csv`
- Wyniki kNN dla różnych k: `output/knn_results.csv`
- Metryki najlepszego modelu: `output/model_metrics.json`
- Wykresy: `output/plots/`
- Raport techniczny: `reports/technical_report.md`
- Wyniki modelu: `reports/model_results.md`
- Podsumowanie: `reports/summary.md`

## Dashboard Streamlit

Dashboard jest warstwą prezentacyjną. Czyta gotowe wyniki z katalogu `output/` i nie importuje ani nie generuje danych.

Najpierw uruchom pipeline:

```bash
python main.py --source generated
python main.py --source csv
```

Następnie uruchom dashboard:

```bash
streamlit run app.py
```

Jeżeli korzystasz z lokalnego środowiska `.venv`:

```bash
.venv/bin/streamlit run app.py
```

Dashboard pokazuje:

- kafelki z liczbą oddziałów, miesięcy, rekordów oraz metrykami modelu,
- rozkład klas efektywności,
- ranking oddziałów według średniego `performance_score`,
- ranking oddziałów wymagających uwagi,
- heatmapę sklep-miesiąc,
- wykaz oddziałów z podsumowaniem,
- tabelę wyników miesięcznych z filtrami,
- szczegóły wybranego oddziału,
- porównanie 2-4 oddziałów,
- wyniki modelu kNN,
- macierz pomyłek,
- wizualizacje PCA 2D,
- interaktywny scatter plot cech modelu.

Jeśli pliki wynikowe nie istnieją, dashboard pokaże komunikat z prośbą o uruchomienie pipeline'u z terminala i odświeżenie widoku.

Wizualizacja PCA 2D pokazuje każdy rekord klasyfikacyjny jako punkt, czyli jeden oddział w jednym miesiącu. Kolor punktu oznacza klasę efektywności. To uproszczenie, ponieważ model kNN działa na wielu cechach jednocześnie, a PCA sprowadza je do dwóch osi.

Interaktywny scatter plot pozwala wybrać dowolne dwie cechy modelu, np. miesięczny przychód i sprzedaż na pracownika. Tooltip pokazuje oddział, miesiąc, wynik `performance_score` i klasę efektywności.

## Testy

```bash
pytest
```
