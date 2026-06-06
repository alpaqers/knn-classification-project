# Import danych CSV

## Katalog wejściowy

Aplikacja czyta dane z katalogu `data/input/`.

## Wymagane pliki

- `dim_store.csv`
- `dim_product.csv`
- `dim_customer.csv`
- `dim_date.csv`
- `fact_sales.csv`

## Wymagane kolumny

`dim_store`: `store_id`, `store_name`, `city`, `region`, `location_type`, `store_size`, `opening_date`, `employee_count`

`dim_product`: `product_id`, `product_name`, `category`, `brand`, `gender`, `base_price`

`dim_customer`: `customer_id`, `age_group`, `city`, `customer_type`

`dim_date`: `date_id`, `date`, `day`, `month`, `month_name`, `quarter`, `year`, `season`

`fact_sales`: `sale_id`, `store_id`, `product_id`, `customer_id`, `date_id`, `quantity`, `revenue`, `discount_amount`, `is_returned`

## Minimalny przykład

Minimalny zestaw danych powinien zawierać przynajmniej jeden rekord w każdej tabeli, a identyfikatory w `fact_sales` muszą istnieć w odpowiednich wymiarach.

## Uruchomienie importu

```bash
python main.py --source csv
```

## Generowanie danych

```bash
python main.py --source generated
```

Ten tryb zapisuje pliki CSV do `data/input/`, a następnie uruchamia dokładnie ten sam importer, którego używa tryb `csv`.

## Najczęstsze błędy walidacji

- Brak wymaganego pliku CSV.
- Brak wymaganej kolumny.
- Pusty plik.
- Duplikaty identyfikatorów.
- Niepoprawny klucz obcy w `fact_sales`.
- Ujemne wartości przychodu albo rabatu.
- `is_returned` inne niż 0 lub 1.

## Podmiana danych

Aby użyć własnych danych, należy zastąpić pliki w `data/input/` i uruchomić `python main.py --source csv`.

## Tryb replace

Importer używa trybu replace: przed załadowaniem nowych danych usuwa stare rekordy z tabel. Dzięki temu kolejne uruchomienia nie dublują transakcji.
