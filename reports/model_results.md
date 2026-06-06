# Wyniki modelu kNN

Najlepsza wartość k: **9**

| Metryka | Wartość |
|---|---:|
| Accuracy | 0.7500 |
| Precision macro | 0.7500 |
| Recall macro | 0.7500 |
| F1-score macro | 0.7500 |

## Porównanie wartości k

| k | Accuracy | Precision | Recall | F1-score |
|---:|---:|---:|---:|---:|
| 3 | 0.6250 | 0.6422 | 0.6250 | 0.6319 |
| 5 | 0.7083 | 0.7149 | 0.7083 | 0.7100 |
| 7 | 0.6250 | 0.6422 | 0.6250 | 0.6319 |
| 9 | 0.7500 | 0.7500 | 0.7500 | 0.7500 |

## Classification report

```text
                   precision    recall  f1-score   support

  high_efficiency       0.75      0.75      0.75         8
   low_efficiency       0.88      0.88      0.88         8
medium_efficiency       0.62      0.62      0.62         8

         accuracy                           0.75        24
        macro avg       0.75      0.75      0.75        24
     weighted avg       0.75      0.75      0.75        24

```