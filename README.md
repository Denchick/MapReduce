# External sorting

# Description

This utility can be used to sort files that do not fit in the RAM and consist of numbers or lines. It is also possible to set sorting parameters (in reverse order, case insensitive, etc.).

# Dependencies

* Python 3
* psutil and shutil modules

# Package structure

* Random values generator `generator.py`
* Entry point: `sorter.py`
* Internal modules `map_reduce / `
* Tests: `tests / `

Modules `piece`, `utils`, `map_reduce` have tests and can be found in `/tests`.

You can use `runtest.sh` (you need `bash`, `coverage3`) to run the tests.

# How to run

Help: `. / sorter.py - -help`

Example:

```
. / generator.py - o big - c 1000 numbers
. / sorter.py - f big.txt - o output - n
```

# Details

The implementation is based on the algorithm [MapReduce](https: // en.wikipedia.org / wiki / MapReduce), in which a large file is broken up into small ones (each of which can be placed in the RAM), the data inside each piece is sorted and then all the pieces are merged into one. The modules responsible for sorting are in the `map_reduce` package. The `piece.Piece` module is responsible for the essence of the `fragment`.
