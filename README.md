# Titanic

Итоговый проект

Стек:

ML: sklearn, pandas, numpy
API: flask
Данные: с kaggle - https://www.kaggle.com/c/titanic

Задача: определение вероятности, что пассажир Титаника утонул при его параметрах: классе билета, поле, возрасте, порту отплытия.

Используемые признаки:

- Pclass (integer)
- Sex (integer)
- Age (integer)
- Embarked (integer)

Преобразования признаков: one hot encoding, stanart scaler

Модель: logreg

### Клонируем репозиторий и создаем образ
```
$ git clone https://github.com/titanic_docker.git
$ cd titanic_docker
$ sudo docker build -t titanic_docker:v3 .
```

### Запускаем контейнер
```
$ sudo docker run -p 8180:8180 -p 8181:8181 titanic_docker:v3
```

### Переходим на localhost:8181
