# Klasyfikacja miesięcznej efektywności oddziałów sieci sklepów obuwniczych

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
    \          /
     fact_sales
    /          \
dim_customer dim_date
```

## 7. ETL i agregacja

Pipeline tworzy tabele SQLite, ładuje dane i agreguje je do tabeli `store_monthly_performance`. Jednostką klasyfikacji jest jeden sklep w jednym miesiącu. Uzyskano 96 rekordów agregacji.

## 8. Performance score

Przed liczeniem wyniku cechy są skalowane metodą Min-Max. Wynik jest ważoną sumą cech pozytywnych: przychodu, sprzedaży na pracownika, średniej wartości zamówienia, liczby klientów, liczby transakcji i liczby produktów. Od wyniku odejmowany jest wpływ cech negatywnych: udziału zwrotów oraz udziału rabatów.

## 9. Klasy efektywności

Klasy `low_efficiency`, `medium_efficiency` i `high_efficiency` są wyznaczane według percentyli zmiennej `performance_score`: dolne 33%, środkowe 33% i górne 33%. Etykiety są tworzone na potrzeby projektu demonstracyjnego, ponieważ dane są syntetyczne.

## 10. Model kNN

Użyto `KNeighborsClassifier`. Cechy zostały przeskalowane przez `StandardScaler`, dane podzielono na zbiór treningowy i testowy, a wartości k porównano dla 3, 5, 7 i 9. Najlepsze k to 9.

## 11. Technologie

Projekt wykorzystuje Python, SQLite, pandas, numpy, scikit-learn, matplotlib, pytest, pathlib oraz Markdown.

## 12. Metryki i wyniki

Accuracy: 0.7500

Precision macro: 0.7500

Recall macro: 0.7500

F1-score macro: 0.7500

Rozkład klas: {'high_efficiency': 33, 'low_efficiency': 32, 'medium_efficiency': 31}

## 13. Interpretacja biznesowa

Oddziały o wysokiej efektywności osiągają korzystniejszą kombinację przychodu, sprzedaży na pracownika i aktywności klientów. Oddziały o niskiej efektywności mogą wymagać analizy poziomu rabatów, zwrotów i potencjału lokalizacji.

## 14. Ograniczenia

Projekt ma charakter edukacyjny. Zbiór po agregacji jest niewielki, a klasy pochodzą z syntetycznego score'u, nie z rzeczywistych decyzji biznesowych. W praktyce należałoby wykorzystać większą liczbę sklepów, dłuższy okres i dane historyczne.

## 15. Kierunki rozwoju

Można dodać więcej lat danych, koszty operacyjne sklepów, marżę, kampanie marketingowe, walidację jakości danych w stylu Great Expectations oraz porównanie kNN z innymi modelami.

## 16. Wnioski

Projekt pokazuje pełny przepływ od danych CSV do hurtowni danych, agregacji analitycznej, klasyfikacji i raportowania. Pipeline jest prosty, powtarzalny i możliwy do rozszerzenia.
