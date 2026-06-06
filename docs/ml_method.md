# Metoda ML

## Klasyfikacja

Klasyfikacja polega na przypisaniu rekordu do jednej z wcześniej zdefiniowanych klas. W projekcie rekordem jest jeden sklep w jednym miesiącu, a klasami są `low_efficiency`, `medium_efficiency` i `high_efficiency`.

## kNN

kNN, czyli k-nearest neighbors, klasyfikuje rekord na podstawie klas najbliższych obserwacji w przestrzeni cech. W projekcie użyto `KNeighborsClassifier`.

## Dlaczego kNN

kNN jest prosty, intuicyjny i dobry do projektu edukacyjnego. Pozwala pokazać znaczenie skalowania cech oraz wpływ parametru `k`.

## Skalowanie danych

kNN opiera się na odległościach. Bez skalowania cecha o dużej skali, np. przychód, zdominowałaby cechy takie jak stopa zwrotów. Dlatego użyto `StandardScaler`.

## Parametr k

Parametr `k` oznacza liczbę sąsiadów branych pod uwagę przy klasyfikacji. Testowane są wartości 3, 5, 7 i 9, a wybór odbywa się na podstawie F1-score macro.

## Metryki

Accuracy mierzy udział poprawnych klasyfikacji.

Precision mówi, jaka część rekordów przewidzianych jako dana klasa rzeczywiście do niej należy.

Recall mówi, jaka część rzeczywistych rekordów danej klasy została odnaleziona.

F1-score łączy precision i recall.

Confusion matrix pokazuje liczbę trafień i pomyłek między klasami.

## Ograniczenia

Dane są syntetyczne, a liczba rekordów po agregacji wynosi około 96. Projekt jest demonstracyjny. W praktyce biznesowej potrzebne byłyby dane rzeczywiste, większa liczba sklepów i dłuższy okres obserwacji.
