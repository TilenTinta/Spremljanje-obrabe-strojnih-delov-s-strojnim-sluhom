# Spremljanje-obrabe-strojnih-delov-s-strojnim-sluhom
Seminarska projekta (študijski in praktični) pri predmetu Inteligentni avdio in govorni sistemi na drugi stopnji BMS na Fakulteti za elektrotehniko smer Avvtomatika in informatika (podsmer: strojno učenje)
---
## Študijski projekt
Raziskava v obliki članka o spremljanju obrabe strojnih delov s strojnim sluhov. 
Članek vsebuje:
- Povzetek
- Uvod
- Sorodna dela
- Teoretično ozadje
    - Časovna domena
    - Frekvenčna domena
    - Časovno-frekvenčna domena
    - Naprednejše metode
- Tehnologija stroja s sluhom
- Metode za spremljanje obrabe
    - Skriti markovovi modeli
    - Metoda podpornih vektorjev - SVM
    - Dolgi kratkoročni spomin - LSTM
    - Transferno učenje
    - Ostale metode
- Prednost in omejitve stroja s sluhom
- Praktični primer uporabe
- Prihodnje smernice raziskav
- Zaključek
- Literatura

---
## Praktični projekt
Praktični projekt nosi enak naslov kot študijski. Ta se ukvarja s klasifikacijo industrijskega zvoka. V mojem primeru so to zvočni posnetki ventilov med delovanjem oz. zvok pretoka skozi njih, ki jih je mogoče najti: 
- Sounds of valves in heating systems for classification and condition monitoring [https://data.mendeley.com/datasets/y6fkrybb32/1]

Dataset je sestavljen iz posnetkov, ki se delijo v štiri kategorije. To so:
    - Kavitacija
    - Rožljanje
    - Piskanje
    - Pravilno delovanje

Projekt sestavljajo štirje programi:
- sort.py: na osnovi excel datoteke iz dataseta razdeli posnetke v 4 mape,
- splitChunks.py: vsak posnetek, ki traja 3 sekunde z oknjenjem razdeli na 8 krajših delov dolgih 500ms s 100ms prekrivanja. S tem zbirko znatno povečamo.
- audioProcessing.py: iz vsakega posentka poseben izlušči značilke ter jih shrani v CSV format. Te se nato lahko uporabi za učenje klasifikatorjev,
- klasifikator_SVM.py: SVM klasifikator, ki bere CSV datoteke, jih obdela ter razdeli na učno ter testno množico. Na osnovi tega se nauči SVM, katerega se na koncu še testira

### Rezultati
```bash
Accuracy: 0.9532163742690059

Classification Report:
               precision    recall  f1-score   support

  Cavitation       0.98      0.99      0.99       189 
        Flow       0.94      1.00      0.97       426 
    Rattling       0.88      0.22      0.35        32 
   Whistling       1.00      0.86      0.93        37 

    accuracy                           0.95       684 
   macro avg       0.95      0.77      0.81       684 
weighted avg       0.95      0.95      0.94       684 
```