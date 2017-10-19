# Внешняя сортировка

Версия 0.1

Автор: Волков Денис (denchick1997@mail.ru)

## Описание

Данная утилита является реализацией алгоритм Map Reduce и может быть использована для сортировки больших файлов с числами или строками с удобным установлением соответствующих параметров сортировки.

## Требования

* Python версии не ниже 3;
* Модуль psutil;

## Состав

* Генератор случайных строк: `generators/numbers_generator.py`
* Генератор случайных чисел `generators/strings_generator.py`
* Сортировщик: `sorter.py`
* Модули `map_reduce/`
* Тесты: `tests/`

Для запуска тестов можно использовать `runtest.sh` (нужен `bash`, `coverage3`)

## Запуск

Справка по запуску: `./sorter.py --help`

Пример запуска: 

```
./generators/numbers_generator.py -o big.txt -c 100
./sorter.py -o output.txt -s "\n" big.txt
```

где `big.txt` - файл, который необходимо отсортировать с `\n` в качестве разделителя между значениями.

## Подробности реализации

В основе реализации лежит алгоритм [MapReduce](https://en.wikipedia.org/wiki/MapReduce), в котором большой файл разбивается на маленькие, каждый из кусков сортируется, а потом все куски сливаются в одно целое. Модули, отвечающие за сортировку, находятся в пакете `map_reduce`. За сущность "кусочек" отвечает модуль `piece.Piece`. 

На модули `piece`, `utils`, `map_reduce` написаны тесты, их можно найти в `tests/`.
