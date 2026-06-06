# Podsumowanie projektu

Zbudowano kompletny pipeline analityczny dla projektu z Hurtowni danych: generator CSV, walidator, importer SQLite, model gwiazdy, agregację sklep + miesiąc, klasy efektywności, model kNN, wykresy, dokumentację i testy.

## Uruchomienie

```bash
python main.py --source generated
python main.py --source csv
pytest
```

## Lokalizacje wyników

- Pliki CSV: `data/input/`
- Baza SQLite: `/home/user/projekty-studia/hurtownie-danych/knn-classification-project/data/output/shoe_stores_dw.sqlite`
- Wykresy: `/home/user/projekty-studia/hurtownie-danych/knn-classification-project/output/plots`
- Raport techniczny: `reports/technical_report.md`
- Wyniki modelu: `reports/model_results.md`
- Testy automatyczne: przygotowano 16 testów pytest; podczas przygotowania projektu wynik wyniósł 16/16 passed.

## Wyniki modelu kNN

Najlepsze k: 9

Accuracy: 0.7500

Precision macro: 0.7500

Recall macro: 0.7500

F1-score macro: 0.7500

## Decyzje projektowe

- Oba tryby uruchomienia korzystają z tego samego importera CSV.
- Model danych to uproszczona gwiazda z jedną tabelą faktów.
- Klasy efektywności są wyznaczane percentylowo z syntetycznego `performance_score`.
- kNN używa skalowania, ponieważ odległości są wrażliwe na skalę cech.

## Ograniczenia i rozwój

Dane są syntetyczne, a liczba rekordów po agregacji jest mała. W rozwoju warto dodać dane rzeczywiste, wiele lat obserwacji, koszty, marżę i porównanie z innymi algorytmami.
