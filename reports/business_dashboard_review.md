# Audyt biznesowy dashboardu Streamlit

## 1. Cel audytu

Celem audytu jest ocena dashboardu Streamlit z perspektywy osoby biznesowej, ktora chce szybko zrozumiec efektywnosc oddzialow sieci sklepow obuwniczych i podjac decyzje operacyjne. Analiza obejmuje obecny dashboard, dane wynikowe, metryki, wykresy, tabele, filtry, interpretacje oraz sposob prezentacji modelu kNN.

Audyt nie ocenia przede wszystkim jakosci kodu. Patrzy na dashboard jako narzedzie decyzyjne: czy pokazuje, ktore oddzialy dzialaja dobrze lub slabo, dlaczego tak sie dzieje i co nalezy z tym zrobic.

## 2. Perspektywa uzytkownika biznesowego

Perspektywa przyjeta w audycie to regional manager lub dyrektor sprzedazy sieci sklepow obuwniczych. Taki uzytkownik nie chce analizowac szczegolow technicznych modelu na pierwszym ekranie. Chce odpowiedziec na kilka pytan:

- ktore oddzialy sa najlepsze,
- ktore oddzialy wymagaja uwagi,
- czy problem wynika z przychodu, zwrotow, rabatow, liczby transakcji lub sprzedazy na pracownika,
- czy oddzial poprawia sie czy pogarsza,
- czy wyniki sa na tyle wiarygodne, aby traktowac je jako demonstracyjna podstawe decyzji,
- jakie dzialania powinny zostac podjete.

## 3. Krotkie podsumowanie obecnego dashboardu

Dashboard jest juz dobrym prototypem analitycznym. Ma podzial na zakladki, podstawowe KPI, ranking oddzialow, tabele wynikow miesiecznych, filtry, szczegoly oddzialu, porownanie oddzialow oraz zakladke modelu kNN. Wykorzystuje gotowe pliki wynikowe z katalogu `output/`: `store_monthly_performance.csv`, `store_summary.csv`, `knn_results.csv` i `model_metrics.json`.

Obecne dane obejmuja 232 rekordy agregacji, 8 oddzialow i 29 okresow miesiecznych od 2024-01 do 2026-05. Rozklad klas jest zbalansowany: 79 rekordow wysokiej efektywnosci, 77 niskiej i 76 sredniej. Najlepszy sredni score ma Warszawa Centrum, a najwiecej miesiecy niskiej efektywnosci ma Lublin Felicity.

Najwieksza luka biznesowa polega na tym, ze dashboard pokazuje "co sie stalo", ale jeszcze zbyt slabo pokazuje "dlaczego" i "co z tym zrobic". Widok jest bardziej raportem analityczno-demonstracyjnym niz pelnym narzedziem do zarzadzania oddzialami.

## 4. Co dziala dobrze

- Dashboard ma sensowny podzial na zakladki: przeglad, oddzialy, wyniki miesieczne, szczegoly oddzialu, porownanie i model kNN.
- Pierwszy ekran pokazuje liczbe oddzialow, miesiecy, rekordow oraz metryki modelu, wiec uzytkownik widzi skale danych i jakosc demonstracyjnego modelu.
- Sekcja podsumowania biznesowego wskazuje najlepszy oddzial, oddzial z najwieksza liczba miesiecy wymagajacych uwagi oraz wynik F1-score.
- Ranking sredniego score'u oddzialow jest biznesowo przydatny i pozwala szybko znalezc liderow.
- Wykres miesiecy niskiej efektywnosci dobrze wskazuje oddzialy wymagajace uwagi.
- Heatmapa score'u miesiac po miesiacu jest bardzo dobrym pomyslem, bo laczy oddzialy, czas i poziom efektywnosci w jednym widoku.
- Tabela "Wyniki miesieczne" ma filtry po oddziale, roku, miesiacu i klasie efektywnosci.
- Zakladka szczegolow oddzialu pokazuje sredni score, dominujaca klase, najlepszy i najslabszy okres, przychod, zwroty, rabaty oraz sprzedaz na pracownika.
- Widok szczegolow oddzialu zawiera wykresy trendu score'u, przychodu i zwrotow.
- Porownanie oddzialow pozwala zestawic kilka sklepow na tych samych wykresach.
- Dashboard tlumaczy etykiety klas na jezyk polski: niska, srednia i wysoka efektywnosc.
- Zakladka modelu uczciwie informuje, ze wynik nalezy traktowac demonstracyjnie, bo dane sa syntetyczne i niewielkie.
- PCA jest opatrzone ostrzezeniem, ze to uproszczona wizualizacja, a model dziala w przestrzeni wielu cech.
- Dane sa eksportowalne do CSV, co jest praktyczne dla analityka lub managera przygotowujacego dalszy raport.

## 5. Czego brakuje

- Brakuje osobnej sekcji "Oddzialy wymagajace uwagi" z priorytetem interwencji i krotkim uzasadnieniem.
- Brakuje wyjasnienia przyczyn klasyfikacji dla konkretnego oddzialu lub miesiaca. Uzytkownik widzi klase, ale nie dostaje jasnej odpowiedzi: przychod byl niski, zwroty wysokie, rabaty wysokie czy produktywnosc pracownikow slaba.
- Brakuje porownania oddzialu do sredniej sieci. Same wartosci bez benchmarku sa trudniejsze do interpretacji.
- Brakuje trendu biznesowego typu "poprawa", "stabilnie", "pogorszenie".
- Brakuje analizy sezonowosci. Dane pokazuja mocne miesiace, np. grudzien 2024 i grudzien 2025, ale dashboard nie opowiada tego wprost.
- Brakuje informacji, jak czesto oddzial przechodzil miedzy klasami miesiac do miesiaca.
- Brakuje listy najwiekszych problemow w sieci: zwroty, rabaty, niski przychod, niska liczba transakcji, niska sprzedaz na pracownika.
- Brakuje rekomendowanych dzialan. Dashboard pokazuje dane, ale nie przeklada ich na decyzje.
- Brakuje business scorecard dla oddzialu, czyli skondensowanego widoku statusu, ryzyka, trendu, benchmarku i rekomendacji.
- Brakuje prostego slownika metryk ML. F1-score, precision, recall, k i macierz pomylek sa zrozumiale dla analityka technicznego, ale nie dla wiekszosci odbiorcow biznesowych.
- Brakuje jasnej legendy klas efektywnosci z opisem, co oznacza niska, srednia i wysoka efektywnosc dla decyzji biznesowej.
- Brakuje wyraznego komunikatu, ze klasy sa wyznaczone percentylowo na podstawie syntetycznego score'u, a nie sa etykietami z rzeczywistej oceny managerow.
- Brakuje miary pewnosci lub ostroznosci interpretacyjnej dla pojedynczego wyniku. kNN moze sklasyfikowac rekord, ale dashboard nie pokazuje, czy przypadek jest blisko granicy klas.

## 6. Co moze byc mylace

- Nazwa `performance_score` lub "Performance score" jest techniczna i nie mowi od razu, czy 0.35 to dobrze czy slabo. Warto nazwac ja "wynik efektywnosci" i pokazac skale.
- Metryki `Accuracy`, `Precision macro`, `Recall macro` i `F1 macro` na glownym ekranie moga sugerowac, ze dashboard jest przede wszystkim narzedziem ML, a nie narzedziem biznesowym.
- "Najlepsze k" jest niezrozumiale bez wyjasnienia. Dla biznesu wazniejsze jest, czy model jest wystarczajaco dobry do demonstracji.
- Macierz pomylek jest przydatna technicznie, ale bez komentarza biznesowego moze byc trudna do odczytania.
- Klasy `low_efficiency`, `medium_efficiency`, `high_efficiency` istnieja w danych i tabelach modelowych. Chociaz dashboard tlumaczy je w wielu miejscach, angielskie nazwy nadal moga pojawiac sie w tabelach technicznych lub hoverach.
- Brakuje jednostek i formatowania w niektorych tabelach. Kwoty powinny byc konsekwentnie sformatowane jako PLN, a procenty jako procenty.
- Nie zawsze jest jasne, czy wartosc jest miesieczna, srednia miesieczna, suma czy wskaznik.
- Heatmapa score'u jest dobra, ale bez opisowej legendy moze byc czytana jako absolutna prawda, mimo ze score jest syntetyczny i wzgledny.
- PCA moze wygladac bardzo naukowo i przekonujaco. Bez mocniejszego komentarza uzytkownik moze nadinterpretowac odleglosci miedzy punktami.
- Model kNN uczy sie na klasach wyprowadzonych z tego samego zestawu cech i score'u. To jest dobre demonstracyjnie, ale nie oznacza, ze model odkryl niezalezna prawde biznesowa.

## 7. Priorytety zmian

### High priority

| Zmiana | Dlaczego | Efekt biznesowy | Rozmiar techniczny |
|---|---|---|---|
| Dodac sekcje "Oddzialy wymagajace uwagi" | Uzytkownik potrzebuje natychmiastowej listy problemow | Szybsza decyzja, ktore sklepy analizowac jako pierwsze | Srednia |
| Dodac wyjasnienie przyczyn slabej klasyfikacji | Sama klasa nie tlumaczy przyczyny | Manager wie, czy reagowac na zwroty, rabaty, przychod czy produktywnosc | Srednia |
| Dodac porownanie oddzialu do sredniej sieci | Bez benchmarku wartosci sa trudne do oceny | Latwiejsza interpretacja KPI i rozmowa z kierownikami oddzialow | Srednia |
| Dodac trend: poprawa, stabilnie, pogorszenie | Biznes musi wiedziec, czy sytuacja sie zmienia | Oddzial jednorazowo slaby nie jest traktowany tak samo jak stale pogarszajacy sie | Srednia |
| Dodac rekomendowane dzialania | Dashboard powinien wspierac decyzje, nie tylko opis danych | Przejscie z raportowania do operacyjnego zarzadzania | Srednia |
| Przeniesc lub ograniczyc metryki ML na pierwszym ekranie | Obecnie moga odciagac uwage od decyzji biznesowych | Lepszy storytelling dla nietechnicznego odbiorcy | Mala |

### Medium priority

| Zmiana | Dlaczego | Efekt biznesowy | Rozmiar techniczny |
|---|---|---|---|
| Dodac analize sezonowosci | Dane pokazuja mocne i slabe miesiace | Lepsze planowanie promocji, zatowarowania i obslugi | Srednia |
| Dodac ranking problemow w sieci | Manager potrzebuje widziec najczestsze zrodla ryzyka | Priorytetyzacja dzialan na poziomie sieci | Srednia |
| Dodac business scorecard oddzialu | Obecny widok szczegolow jest dobry, ale rozproszony | Jeden ekran do rozmowy o konkretnym oddziale | Srednia |
| Dodac legende klas efektywnosci | Klasy musza miec znaczenie decyzyjne | Mniej niejasnosci dla odbiorcy biznesowego | Mala |
| Dodac prosty opis metryk modelu | F1-score i k nie sa intuicyjne | Lepsze zaufanie i mniejsze ryzyko nadinterpretacji | Mala |
| Ujednolicic formatowanie kwot i procentow w tabelach | Tabele sa czytelniejsze, gdy jednostki sa konsekwentne | Mniej bledow interpretacyjnych | Mala |

### Low priority

| Zmiana | Dlaczego | Efekt biznesowy | Rozmiar techniczny |
|---|---|---|---|
| Dodac tooltips do KPI i metryk | Pomagaja nowym uzytkownikom | Lepsza samoobslugowosc dashboardu | Mala |
| Dodac eksport raportu oddzialu | Przydatne do spotkan operacyjnych | Latwiejsze dzielenie sie wnioskami | Srednia |
| Dodac bardziej opisowe tytuly wykresow | Obecne wykresy sa poprawne, ale malo narracyjne | Dashboard staje sie latwiejszy do czytania | Mala |
| Dodac widok "benchmark do najlepszego oddzialu" | Przydatne, ale mniej pilne niz srednia sieci | Pokazuje dystans do lidera | Srednia |

## 8. Propozycje nowych elementow dashboardu

### 1. Sekcja "Oddzialy wymagajace uwagi"

- Cel: pokazac sklepy, ktore najczesciej maja niska efektywnosc albo pogarszaja sie w ostatnich miesiacach.
- Potrzebne dane: `low_months`, `avg_score`, ostatnie 3-6 miesiecy score'u, liczba spadkow klasy.
- Sposob prezentacji: tabela lub karty z oddzialem, poziomem ryzyka, liczba miesiecy niskiej efektywnosci, trendem i glowna przyczyna.
- Przydatnosc biznesowa: manager od razu widzi, gdzie zaczac interwencje.

### 2. Sekcja "Dlaczego ten oddzial jest slaby?"

- Cel: wyjasnic, ktore KPI najbardziej odbiegaja od sredniej sieci.
- Potrzebne dane: przychod, liczba transakcji, srednia wartosc transakcji, zwroty, rabaty, sprzedaz na pracownika, srednie sieci.
- Sposob prezentacji: lista 3 najwiekszych odchylen z oznaczeniem pozytywne/negatywne.
- Przydatnosc biznesowa: uzytkownik dostaje przyczyne, a nie tylko etykiete klasy.

### 3. Sekcja "Porownanie do sredniej sieci"

- Cel: pokazac, czy oddzial jest powyzej czy ponizej standardu sieci.
- Potrzebne dane: wartosci KPI oddzialu i srednie KPI dla wszystkich oddzialow.
- Sposob prezentacji: scorecard, wykres slupkowy odchylen lub tabela "oddzial vs siec".
- Przydatnosc biznesowa: ulatwia rozmowe z kierownikami i ocene lokalnych wynikow.

### 4. Sekcja "Trend: poprawa/stabilnie/pogorszenie"

- Cel: sklasyfikowac kierunek zmiany oddzialu.
- Potrzebne dane: score i klasa miesiac po miesiacu.
- Sposob prezentacji: etykieta trendu, miniwykres score'u i zmiana miesiac do miesiaca.
- Przydatnosc biznesowa: odroznia problem chwilowy od narastajacego.

### 5. Sekcja "Rekomendowane dzialania"

- Cel: przelozyc diagnoze na dzialania operacyjne.
- Potrzebne dane: problem dominujacy, wartosci KPI, odchylenia od sredniej.
- Sposob prezentacji: 2-4 rekomendacje tekstowe dla oddzialu lub miesiaca.
- Przydatnosc biznesowa: dashboard staje sie narzedziem decyzyjnym, a nie tylko raportem.

### 6. Alerty biznesowe

- Cel: oznaczyc przypadki wymagajace natychmiastowej uwagi.
- Potrzebne dane: prog niskiego score'u, wysokie zwroty, wysokie rabaty, spadek przychodu, spadek klasy.
- Sposob prezentacji: lista alertow na pierwszym ekranie, np. "Lublin Felicity: 18 miesiecy niskiej efektywnosci".
- Przydatnosc biznesowa: szybkie wychwycenie ryzyka.

### 7. Business scorecard dla oddzialu

- Cel: dac jeden zwarty widok sytuacji oddzialu.
- Potrzebne dane: sredni score, dominujaca klasa, trend, low/medium/high months, benchmark, glowne odchylenia.
- Sposob prezentacji: metryki, krotki opis, benchmark i rekomendacje w jednej zakladce.
- Przydatnosc biznesowa: dobry format do comiesiecznego przegladu wynikow.

### 8. Ranking problemow

- Cel: pokazac, ktore problemy sa najwieksze w skali sieci.
- Potrzebne dane: odchylenia KPI od srednich, progi alertow.
- Sposob prezentacji: ranking "najwyzszy udzial zwrotow", "najwyzszy udzial rabatow", "najnizszy przychod", "najnizsza sprzedaz na pracownika".
- Przydatnosc biznesowa: pomaga zdecydowac, czy problem jest lokalny czy systemowy.

### 9. Wyjasnienie modelu kNN prostym jezykiem

- Cel: zmniejszyc bariere techniczna.
- Potrzebne dane: metryki modelu i lista cech.
- Sposob prezentacji: ramka tekstowa w zakladce modelu, bez nadmiaru terminologii.
- Przydatnosc biznesowa: uzytkownik rozumie, kiedy moze zaufac wynikowi i jakie sa ograniczenia.

### 10. Legenda klas efektywnosci

- Cel: nadac klasom znaczenie biznesowe.
- Potrzebne dane: definicja percentylowa i opis interpretacyjny.
- Sposob prezentacji: mala legenda na gorze dashboardu.
- Przydatnosc biznesowa: mniejsza liczba blednych interpretacji.

## 9. Propozycje nowych wskaznikow

| Wskaznik | Co oznacza | Jak policzyc | Dlaczego przydatny |
|---|---|---|---|
| `revenue_per_order` | Przychod na transakcje | `monthly_revenue / orders_count` | Bardziej biznesowa nazwa dla sredniej wartosci transakcji |
| `revenue_per_customer` | Przychod na unikalnego klienta | `monthly_revenue / unique_customers` | Pokazuje wartosc klienta w oddziale |
| `returns_value` | Szacunkowa wartosc zwrotow | suma przychodu dla transakcji zwroconych, jesli dane transakcyjne sa dostepne | Pozwala ocenic skale finansowa zwrotow, nie tylko procent |
| `net_revenue` | Przychod po korekcie zwrotow | `monthly_revenue - returns_value` | Blizsze rzeczywistemu efektowi finansowemu |
| `discount_rate` | Udzial rabatow w cenie przed rabatem | juz zblizone do `discount_share` | Pomaga ocenic, czy wynik jest kupowany rabatami |
| `customer_repeat_rate` | Udzial klientow powracajacych | klienci powracajacy / wszyscy klienci w okresie | Pokazuje lojalnosc i jakosc bazy klientow |
| `month_over_month_growth` | Zmiana przychodu miesiac do miesiaca | `(revenue_t - revenue_t-1) / revenue_t-1` | Wykrywa poprawy i spadki |
| `score_change_month_over_month` | Zmiana score'u miesiac do miesiaca | `score_t - score_t-1` | Prosty sygnal trendu efektywnosci |
| `class_change_month_over_month` | Zmiana klasy wzgledem poprzedniego miesiaca | porownanie klasy `t` i `t-1` | Pokazuje awanse i spadki oddzialu |
| `deviation_from_network_average` | Odchylenie KPI od sredniej sieci | `store_metric - network_avg_metric` | Najprostsze wyjasnienie, dlaczego oddzial odstaje |
| `percentile_rank` | Pozycja oddzialu w sieci | percentyl score'u lub KPI | Latwiejsze niz surowy score, np. "top 20%" |
| `risk_flag` | Flaga ryzyka | reguly: niski score, wysokie zwroty, spadek klasy | Szybkie alerty biznesowe |
| `action_priority` | Priorytet dzialania | kombinacja ryzyka, trendu i skali odchylenia | Pomaga kolejkowac interwencje |

## 10. Propozycje zmian w ukladzie dashboardu

Obecny dashboard jest logiczny, ale storytelling moglby mocniej prowadzic od obrazu sieci do decyzji. Rekomendowany uklad:

1. **Przeglad sieci**
   - status sieci,
   - liczba oddzialow, okresow i rekordow,
   - rozklad klas,
   - najlepszy oddzial,
   - oddzialy wymagajace uwagi,
   - najwazniejsze alerty.

2. **Ranking i alerty**
   - ranking najlepszych i najslabszych oddzialow,
   - ranking miesiecy niskiej efektywnosci,
   - ranking problemow: zwroty, rabaty, przychod, sprzedaz na pracownika.

3. **Szczegoly oddzialu**
   - business scorecard,
   - trend,
   - porownanie do sredniej sieci,
   - wyjasnienie przyczyn,
   - rekomendowane dzialania.

4. **Trendy i sezonowosc**
   - heatmapa score'u,
   - sredni score sieci miesiac po miesiacu,
   - miesiace sezonowo mocne i slabe,
   - zmiany klas miesiac do miesiaca.

5. **Porownanie oddzialow**
   - wybrane sklepy na wspolnych wykresach,
   - tabela porownawcza z formatowanymi KPI,
   - roznice wzgledem sredniej i lidera.

6. **Dane szczegolowe**
   - filtrowalna tabela store-month,
   - eksport CSV.

7. **Model i ograniczenia**
   - proste wyjasnienie kNN,
   - metryki modelu,
   - macierz pomylek,
   - PCA,
   - ograniczenia danych syntetycznych.

Taki uklad lepiej odpowiada naturalnemu przeplywowi pracy: najpierw "co sie dzieje w sieci", potem "kogo dotyczy problem", dalej "dlaczego" i na koncu "co robimy".

## 11. Propozycje tekstow wyjasniajacych dla uzytkownika biznesowego

### Legenda klas

> Niska efektywnosc oznacza, ze wynik oddzialu w danym miesiacu znajduje sie w dolnej czesci rozkladu sieci. Taki oddzial warto przeanalizowac pod katem przychodu, zwrotow, rabatow i sprzedazy na pracownika.

> Srednia efektywnosc oznacza wynik typowy dla sieci w analizowanym okresie. Oddzial nie wymaga pilnej interwencji, ale warto obserwowac trend.

> Wysoka efektywnosc oznacza, ze oddzial jest w gornej czesci rozkladu sieci. Takie oddzialy moga sluzyc jako benchmark dla pozostalych.

### Wyjasnienie score'u

> Wynik efektywnosci laczy kilka wskaznikow sprzedazowych. Wyzej premiowane sa przychod, sprzedaz na pracownika, srednia wartosc transakcji i aktywnosc klientow. Wynik obnizaja wysoki udzial zwrotow i rabatow.

### Wyjasnienie kNN

> Model kNN klasyfikuje miesiac oddzialu przez porownanie go do najbardziej podobnych miesiecy w danych. Jesli podobne przypadki mialy wysoka efektywnosc, model przypisuje podobna klase.

### Wyjasnienie k

> Parametr k oznacza liczbe podobnych przypadkow, ktore model bierze pod uwage. W tym projekcie najlepszy wynik demonstracyjny uzyskano dla k = 7.

### Wyjasnienie F1-score

> F1-score pokazuje, jak dobrze model laczy trafnosc i kompletne wykrywanie klas. Wartosc 0.826 oznacza dobry wynik demonstracyjny, ale nie powinna byc traktowana jako gwarancja jakosci produkcyjnej.

### Wyjasnienie macierzy pomylek

> Macierz pomylek pokazuje, kiedy model poprawnie rozpoznal klase oddzialu, a kiedy pomylil ja z inna klasa. Dla uzytkownika biznesowego najwazniejsze sa pomylki miedzy niska i wyzsza efektywnoscia, bo moga zmienic priorytet dzialan.

### Ograniczenie demonstracyjne

> Dane sa syntetyczne, a klasy efektywnosci zostaly wyznaczone na podstawie reguly score'u. Wyniki dobrze pokazuja proces analityczny, ale nie powinny byc traktowane jako gotowy model produkcyjny dla rzeczywistej sieci sklepow.

## 12. Rekomendowany plan implementacji zmian

### Etap 1: szybkie usprawnienia biznesowe

- Dodac legende klas efektywnosci.
- Zmienic nazwe "Performance score" na "Wynik efektywnosci".
- Dodac prosty opis F1-score, k i danych syntetycznych.
- Ujednolicic formatowanie kwot i procentow w tabelach.
- Przesunac metryki ML nizej albo do zakladki modelu.

### Etap 2: diagnoza i priorytety

- Dodac sekcje "Oddzialy wymagajace uwagi".
- Dodac porownanie oddzialu do sredniej sieci.
- Dodac wskazanie 3 glownych przyczyn slabej klasyfikacji.
- Dodac `risk_flag` i `action_priority`.
- Dodac ranking problemow.

### Etap 3: trend i sezonowosc

- Dodac zmiany miesiac do miesiaca dla score'u, klasy i przychodu.
- Dodac trend: poprawa, stabilnie, pogorszenie.
- Dodac widok sezonowosci sieci.
- Dodac liczbe awansow i spadkow klasy dla oddzialu.

### Etap 4: rekomendacje i storytelling

- Dodac rekomendowane dzialania dla oddzialow.
- Dodac business scorecard oddzialu.
- Przebudowac kolejnosc zakladek wedlug przeplywu decyzyjnego.
- Rozszerzyc sekcje modelu o interpretacje bledow modelu w jezyku biznesowym.

## 13. Podsumowanie koncowe

Dashboard ma solidna baze: pokazuje ranking oddzialow, miesieczne wyniki, porownania, trendy i jakosc modelu kNN. Jest czytelny jako projekt demonstracyjny laczacy hurtownie danych, agregacje i klasyfikacje.

Najwazniejszy kierunek rozwoju to przesuniecie akcentu z prezentacji danych na wsparcie decyzji. Uzytkownik biznesowy powinien po kilku minutach wiedziec nie tylko, ktory oddzial jest slaby, ale tez dlaczego jest slaby, czy problem sie pogarsza, jak wypada na tle sieci i jakie dzialanie nalezy podjac.

Rekomendowane pierwsze zmiany to: sekcja oddzialow wymagajacych uwagi, diagnoza przyczyn klasyfikacji, benchmark do sredniej sieci, trend poprawy/pogorszenia oraz proste wyjasnienie modelu i klas efektywnosci.
