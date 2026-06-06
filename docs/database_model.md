# Model bazy danych

## Tabela faktów i wymiary

Tabela faktów przechowuje zdarzenia biznesowe, czyli transakcje sprzedaży. Tabele wymiarów opisują kontekst tych zdarzeń: sklep, produkt, klienta i datę.

## Dlaczego model gwiazdy

Model gwiazdy jest czytelny i dobrze pasuje do raportowania sprzedaży. Centralna tabela `fact_sales` łączy się bezpośrednio z wymiarami, co upraszcza agregacje do poziomu sklepu, produktu, klienta lub czasu.

## Tabela `fact_sales`

Kolumny: `sale_id`, `store_id`, `product_id`, `customer_id`, `date_id`, `quantity`, `revenue`, `discount_amount`, `is_returned`.

Jeden rekord oznacza sprzedaż konkretnego produktu w konkretnym sklepie, danego dnia, dla konkretnego klienta.

## Wymiary

`dim_store` opisuje oddziały: nazwa, miasto, region, typ lokalizacji, rozmiar sklepu, data otwarcia i liczba pracowników.

`dim_product` opisuje produkty: nazwa, kategoria, marka, płeć docelowa i cena bazowa.

`dim_customer` opisuje klientów: grupa wieku, miasto i typ klienta.

`dim_date` opisuje kalendarz: dzień, miesiąc, kwartał, rok i sezon.

## Relacje

```text
dim_store.store_id       -> fact_sales.store_id
dim_product.product_id   -> fact_sales.product_id
dim_customer.customer_id -> fact_sales.customer_id
dim_date.date_id         -> fact_sales.date_id
```

## Diagram tekstowy

```text
                 dim_product
                      |
dim_store ---- fact_sales ---- dim_customer
                      |
                   dim_date
```

## Mermaid

```mermaid
erDiagram
    DIM_STORE ||--o{ FACT_SALES : has
    DIM_PRODUCT ||--o{ FACT_SALES : has
    DIM_CUSTOMER ||--o{ FACT_SALES : has
    DIM_DATE ||--o{ FACT_SALES : has

    DIM_STORE {
        int store_id PK
        string store_name
        string city
        string region
        string location_type
        string store_size
        string opening_date
        int employee_count
    }

    DIM_PRODUCT {
        int product_id PK
        string product_name
        string category
        string brand
        string gender
        float base_price
    }

    DIM_CUSTOMER {
        int customer_id PK
        string age_group
        string city
        string customer_type
    }

    DIM_DATE {
        int date_id PK
        string date
        int day
        int month
        string month_name
        int quarter
        int year
        string season
    }

    FACT_SALES {
        int sale_id PK
        int store_id FK
        int product_id FK
        int customer_id FK
        int date_id FK
        int quantity
        float revenue
        float discount_amount
        int is_returned
    }
```
