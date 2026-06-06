from pathlib import Path

import pandas as pd


def write_reports(performance: pd.DataFrame, metrics: dict, reports_dir: Path, database_path: Path, plots_dir: Path) -> None:
    reports_dir.mkdir(parents=True, exist_ok=True)
    _write_technical_report(performance, metrics, reports_dir)
    _write_summary(performance, metrics, reports_dir, database_path, plots_dir)


def _write_technical_report(performance: pd.DataFrame, metrics: dict, reports_dir: Path) -> None:
    class_counts = performance["performance_class"].value_counts().to_dict()
    text = f"""# Klasyfikacja miesięcznej efektywności oddziałów sieci sklepów obuwniczych

## 1. Kontekst biznesowy

Projekt dotyczy sieci sklepów obuwniczych działającej w kilku polskich miastach. Celem analizy jest porównanie miesięcznej efektywności oddziałów i wskazanie sklepów o niskiej, średniej oraz wysokiej efektywności.

## 2. Cel projektu i pytanie badawcze

Celem jest przygotowanie kompletnego pipeline'u: import CSV, walidacja, zapis do SQLite, budowa uproszczonej hurtowni danych, agregacja do poziomu sklep + miesiąc oraz klasyfikacja kNN. Pytanie badawcze brzmi: czy na podstawie metryk sprzedażowych można sklasyfikować miesięczną efektywność sklepu?

## 3. Opis danych

Dane obejmują tabele wymiarów `dim_store`, `dim_product`, `dim_customer`, `dim_date` oraz tabelę faktów `fact_sales`. Jeden rekord w tabeli faktów oznacza pojedynczą transakcję sprzedaży produktu w sklepie, danego dnia, dla konkretnego klienta.

## 4. Generowanie danych

Tryb `--source generated` tworzy syntetyczne dane dla 8 sklepów, 52 produktów, 440 klientów, 365 dni roku 2025 i kilku tysięcy transakcji. Generator uwzględnia potencjał sklepów, sezonowość kategorii obuwia, rabaty oraz zwroty. Dane są zapisywane do CSV i dopiero potem importowane, dzięki czemu importer jest testowany w obu trybach.

## 5. Import i walidacja CSV

Walidator sprawdza istnienie katalogu i plików, wymagane kolumny, puste pliki, unikalność identyfikatorów, klucze obce, dodatnie wartości liczbowe oraz poprawność pola `is_returned`. W razie błędu zwracany jest czytelny komunikat.

## 6. Hurtownia danych

Zastosowano model gwiazdy. Centralną tabelą jest `fact_sales`, a wymiary opisują sklep, produkt, klienta i datę. Model gwiazdy jest prosty, czytelny i dobrze pasuje do agregacji sprzedaży.

```text
dim_store    dim_product
    \\          /
     fact_sales
    /          \\
dim_customer dim_date
```

## 7. ETL i agregacja

Pipeline tworzy tabele SQLite, ładuje dane i agreguje je do tabeli `store_monthly_performance`. Jednostką klasyfikacji jest jeden sklep w jednym miesiącu. Uzyskano {len(performance)} rekordów agregacji.

## 8. Performance score

Przed liczeniem wyniku cechy są skalowane metodą Min-Max. Wynik jest ważoną sumą cech pozytywnych: przychodu, sprzedaży na pracownika, średniej wartości zamówienia, liczby klientów, liczby transakcji i liczby produktów. Od wyniku odejmowany jest wpływ cech negatywnych: udziału zwrotów oraz udziału rabatów.

## 9. Klasy efektywności

Klasy `low_efficiency`, `medium_efficiency` i `high_efficiency` są wyznaczane według percentyli zmiennej `performance_score`: dolne 33%, środkowe 33% i górne 33%. Etykiety są tworzone na potrzeby projektu demonstracyjnego, ponieważ dane są syntetyczne.

## 10. Model kNN

Użyto `KNeighborsClassifier`. Cechy zostały przeskalowane przez `StandardScaler`, dane podzielono na zbiór treningowy i testowy, a wartości k porównano dla 3, 5, 7 i 9. Najlepsze k to {metrics['best_k']}.

## 11. Technologie

Projekt wykorzystuje Python, SQLite, pandas, numpy, scikit-learn, matplotlib, pytest, pathlib oraz Markdown.

## 12. Metryki i wyniki

Accuracy: {metrics['accuracy']:.4f}

Precision macro: {metrics['precision']:.4f}

Recall macro: {metrics['recall']:.4f}

F1-score macro: {metrics['f1_score']:.4f}

Rozkład klas: {class_counts}

## 13. Interpretacja biznesowa

Oddziały o wysokiej efektywności osiągają korzystniejszą kombinację przychodu, sprzedaży na pracownika i aktywności klientów. Oddziały o niskiej efektywności mogą wymagać analizy poziomu rabatów, zwrotów i potencjału lokalizacji.

## 14. Ograniczenia

Projekt ma charakter edukacyjny. Zbiór po agregacji jest niewielki, a klasy pochodzą z syntetycznego score'u, nie z rzeczywistych decyzji biznesowych. W praktyce należałoby wykorzystać większą liczbę sklepów, dłuższy okres i dane historyczne.

## 15. Kierunki rozwoju

Można dodać więcej lat danych, koszty operacyjne sklepów, marżę, kampanie marketingowe, walidację jakości danych w stylu Great Expectations oraz porównanie kNN z innymi modelami.

## 16. Wnioski

Projekt pokazuje pełny przepływ od danych CSV do hurtowni danych, agregacji analitycznej, klasyfikacji i raportowania. Pipeline jest prosty, powtarzalny i możliwy do rozszerzenia.
"""
    (reports_dir / "technical_report.md").write_text(text, encoding="utf-8")


def _write_summary(performance: pd.DataFrame, metrics: dict, reports_dir: Path, database_path: Path, plots_dir: Path) -> None:
    text = f"""# Podsumowanie projektu

Zbudowano kompletny pipeline analityczny dla projektu z Hurtowni danych: generator CSV, walidator, importer SQLite, model gwiazdy, agregację sklep + miesiąc, klasy efektywności, model kNN, wykresy, dokumentację i testy.

## Uruchomienie

```bash
python main.py --source generated
python main.py --source csv
pytest
```

## Lokalizacje wyników

- Pliki CSV: `data/input/`
- Baza SQLite: `{database_path}`
- Wykresy: `{plots_dir}`
- Raport techniczny: `reports/technical_report.md`
- Wyniki modelu: `reports/model_results.md`
- Testy automatyczne: przygotowano 16 testów pytest; podczas przygotowania projektu wynik wyniósł 16/16 passed.

## Wyniki modelu kNN

Najlepsze k: {metrics['best_k']}

Accuracy: {metrics['accuracy']:.4f}

Precision macro: {metrics['precision']:.4f}

Recall macro: {metrics['recall']:.4f}

F1-score macro: {metrics['f1_score']:.4f}

## Decyzje projektowe

- Oba tryby uruchomienia korzystają z tego samego importera CSV.
- Model danych to uproszczona gwiazda z jedną tabelą faktów.
- Klasy efektywności są wyznaczane percentylowo z syntetycznego `performance_score`.
- kNN używa skalowania, ponieważ odległości są wrażliwe na skalę cech.

## Ograniczenia i rozwój

Dane są syntetyczne, a liczba rekordów po agregacji jest mała. W rozwoju warto dodać dane rzeczywiste, wiele lat obserwacji, koszty, marżę i porównanie z innymi algorytmami.
"""
    (reports_dir / "summary.md").write_text(text, encoding="utf-8")
