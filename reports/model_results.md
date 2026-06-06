# Wyniki modelu kNN

Najlepsza wartość k: **7**

| Metryka | Wartość |
|---|---:|
| Accuracy | 0.8276 |
| Precision macro | 0.8382 |
| Recall macro | 0.8272 |
| F1-score macro | 0.8261 |

## Porównanie wartości k

| k | Accuracy | Precision | Recall | F1-score |
|---:|---:|---:|---:|---:|
| 3 | 0.8276 | 0.8283 | 0.8263 | 0.8249 |
| 5 | 0.7759 | 0.7823 | 0.7754 | 0.7743 |
| 7 | 0.8276 | 0.8382 | 0.8272 | 0.8261 |
| 9 | 0.7931 | 0.8014 | 0.7939 | 0.7916 |

## Classification report

```text
                   precision    recall  f1-score   support

  high_efficiency       1.00      0.85      0.92        20
   low_efficiency       0.75      0.95      0.84        19
medium_efficiency       0.76      0.68      0.72        19

         accuracy                           0.83        58
        macro avg       0.84      0.83      0.83        58
     weighted avg       0.84      0.83      0.83        58

```