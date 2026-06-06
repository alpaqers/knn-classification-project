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
- Dane dashboardu: `output/store_monthly_performance.csv`, `output/store_summary.csv`, `output/knn_results.csv`, `output/model_metrics.json`
- Wykresy: `/home/user/projekty-studia/hurtownie-danych/knn-classification-project/output/plots`
- Raport techniczny: `reports/technical_report.md`
- Wyniki modelu: `reports/model_results.md`
- Testy automatyczne: przygotowano 23 testy pytest; podczas przygotowania projektu wynik wyniósł 23/23 passed.
- Dashboard Streamlit: `streamlit run app.py`

## Wyniki modelu kNN

Najlepsze k: 7

Accuracy: 0.8276

Precision macro: 0.8382

Recall macro: 0.8272

F1-score macro: 0.8261

## Decyzje projektowe

- Oba tryby uruchomienia korzystają z tego samego importera CSV.
- Model danych to uproszczona gwiazda z jedną tabelą faktów.
- Klasy efektywności są wyznaczane percentylowo z syntetycznego `performance_score`.
- kNN używa skalowania, ponieważ odległości są wrażliwe na skalę cech.

## Ograniczenia i rozwój

Dane są syntetyczne, a liczba rekordów po agregacji jest mała. W rozwoju warto dodać dane rzeczywiste, wiele lat obserwacji, koszty, marżę i porównanie z innymi algorytmami.
