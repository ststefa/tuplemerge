# Coding Task 2

## Task

Implement a MERGE function that receives a list of intervals and returns a list of intervals as a result. All overlapping intervals should be merged in the result. All non-overlapping intervals remain unaffected.

https://docs.google.com/document/d/1FS272sy-boGQ49TBFKirIbn5YLasZi1XcyAq5NZ2uBI/edit#

### Example

Input: [25, 30] [2, 19] [14, 23] [4, 8]

Output:[2,23] [25,30]

### Questions

- What is the runtime of your program?
- How can robustness be ensured, especially considering very large inputs ?


## Further assumptions

Some assumptions need to be made to clearly define the rules for intervals and interval overlapping

1. An interval [x, y] represents all natural numbers ranging from x to y where y is equal to or bigger than x.

    Examples for valid intervals

    - [23, 234]
    - [0, 0]

    Examples for invalid intervals

    - [-1, 5]
    - [4, 3]
    - [1.5, 2]

1. Two intervals i1 and i2 are considered overlapping if i2 contains one or more numbers which are also represented by i1.

    Examples for overlapping intervals

    - [5, 10], [8, 12]
    - [0, 10], [3, 4]
    - [5, 6], [6, 9]

    Examples for non-overlapping intervals

    - [5, 10], [11, 15]
    - [5, 10], [1, 2]

## Implementation

I assume that the performance matters because the algorithm is used for a performance critical task. I opted to make the merge-strategy implementation modular in this regard to encourage experimentation and continued development. One might rightfully consider this over-engineering. However given the suggested time to complete the exercise I went for a more-than-minimal approach. In order not to inflate the code unnecessarily, I have avoided the implementation of distracting (distracting within the scope of the task) functionality like handling of files or logging.

The actual merge algorithms are implemented in `*_strategy` methods. The are invoked dynamically. To add a "whatever" strategy, implement a `whatever_strategy()` method and add `whatever` to the list of choices in the `merge` argument-parser.

# Usage

The code is entirely implemented in the python script `tuple.py`. It features a list of commands which can specified as an argument. Each command might have varying input parameters. All commands (except "gen") read data from stdin. All commands write their result to stdout. JSON is used as both in- and output format.

To be able to verify the correctness of the algorithms I added some tool-functions which can be used for exploration. Commands are meant to be chained using stdin/stdout, e.g.

    ./tuple.py gen 0 10000000 9000 10000 | ./tuple.py merge | ./tuple.py verify

...generates a list of 10000 tuples between 0 and 10000000 with a maximum range of 9000, merges them using the default strategy and verifies that the result does not contain overlapping elements.

## tuple.py commands

### `gen` command

Generate a random list of tuples and write them to stdout. The min/max boundaries, the maximum size of elements as well as the number of elements is specified as positional arguments.

    $ ./tuple.py gen 0 10 3 5
    [[5, 6], [4, 7], [0, 2], [5, 7], [0, 1]]

### `merge` command

Merge a list of tuples read from stdin and write the result to stdout. The merge strategy can be specified as an argument.

    $ echo [[5, 6], [4, 7], [0, 2], [5, 7], [0, 1]] | ./tuple.py merge -s naive
    [[0, 2], [4, 7]]

### `verify` command

Read a list of tuples from stdin and validate that no overlapping tuples exist. Writes the input to stdout if validation succeeded or raises an error otherwise.

    $ echo [[1, 2], [3, 4]] | ./tuple.py verify
    [[1, 2], [3, 4]]
    $ echo [[1, 2], [2, 4]] | ./tuple.py verify
    Error: Elements [2, 4] and [1, 2] overlap

### `sort` command

Read a list of tuples from stdin, sort them by their lower bound and print the result to stdout. Can be useful to compare results visually.

    $ echo [[2, 6],[1, 5]] | ./tuple.py sort
    [[1, 5], [2, 6]]

### `count` command

Read a list of tuples from stdin, count their elements and write the result to stdout. Can be useful to explore how the characteristics of the input data influence the output quantitatively.

    $ ./tuple.py gen 0 10000000 1000 100000 | ./tuple.py merge | ./tuple.py count
    [614]
    $ ./tuple.py gen 0 10000000 2000 50000 | ./tuple.py merge | ./tuple.py count
    [310]
    $ ./tuple.py gen 0 10000000 4000 25000 | ./tuple.py merge | ./tuple.py count
    [179]

# Tests

Simple unit tests as well as algorithm-correctness tests are performed using pytest. To run

  1. `pip install pytest`
  1. `pytest -v`

# Answers

## What is the runtime of your program?

Time/complexity can be measured e.g. using pythons builtin profiler. For large inputs, the runtime is determined almost entirely by the merge algorithm. Two example algorithms have been implemented:

### naive strategy

Modeled after the scheme how one would manually approach the problem. On every iteration, one element is sliced off from the input data. Then that element is compared with every element of the result list, merging any overlaps that are found.

Because this requires to iterate over the result list for every element in the input list it has a computational complexity of O(n^2) and is not very efficient.

    $ ./tuple.py gen 0 10000000 1000 100000 | python3 -m cProfile -s cumtime ./tuple.py merge -s naive | head -n 20
    [[716992, 717107], [8531351, 8531378], ...
            380040047 function calls (380039788 primitive calls) in 274.842 seconds

      Ordered by: cumulative time

      ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        17/1    0.000    0.000  274.842  274.842 {built-in method builtins.exec}
            1    0.002    0.002  274.842  274.842 tuple.py:4(<module>)
            1    0.000    0.000  274.824  274.824 tuple.py:204(main)
            1    0.000    0.000  274.452  274.452 tuple.py:40(merge_tuples)
            1   68.361   68.361  274.452  274.452 tuple.py:80(naive_strategy)
    379427459  195.320    0.000  195.320    0.000 tuple.py:126(_overlaps)
        99358   10.486    0.000   10.486    0.000 {method 'remove' of 'list' objects}
            1    0.322    0.322    0.323    0.323 {method 'read' of '_io.TextIOWrapper' objects}
        99357    0.096    0.000    0.245    0.000 tuple.py:147(_merge)
        99469    0.118    0.000    0.118    0.000 {built-in method builtins.min}
            1    0.000    0.000    0.044    0.044 __init__.py:299(loads)
            1    0.000    0.000    0.044    0.044 decoder.py:332(decode)
            1    0.044    0.044    0.044    0.044 decoder.py:343(raw_decode)
        99377    0.031    0.000    0.031    0.000 {built-in method builtins.max}

## sort strategy

If the input is sorted then we can take advantage of the fact that all potentially overlapping elements are necessarily neighbours. It does not matter whether the upper or lower bound is used for sorting. In my implementation I chose to use the lower bound.

We can iterate over the sorted input once, merging any element with its overlapping neighbor(s). This leads to a computational complexity of O(n).

Theoretically, this advantage would be reduced by the fact that sorting the list itself has a complexity of (at least) O(n*log(n)). However, the Python sort algorithm is very efficient and adaptive. The efficiency of the sort-strategy is therefore much better than the simple naive-strategy.

    $ ./tuple.py gen 0 10000000 1000 100000 | python3 -m cProfile -s cumtime ./tuple.py merge -s sort | head -n 20
    [[5, 7993], [8064, 9071]...
            713857 function calls (713598 primitive calls) in 0.695 seconds

      Ordered by: cumulative time

      ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        17/1    0.000    0.000    0.695    0.695 {built-in method builtins.exec}
            1    0.022    0.022    0.695    0.695 tuple.py:4(<module>)
            1    0.000    0.000    0.656    0.656 tuple.py:204(main)
            1    0.316    0.316    0.317    0.317 {method 'read' of '_io.TextIOWrapper' objects}
            1    0.000    0.000    0.288    0.288 tuple.py:40(merge_tuples)
            1    0.083    0.083    0.288    0.288 tuple.py:103(sort_strategy)
        99350    0.044    0.000    0.090    0.000 tuple.py:147(_merge)
        99999    0.051    0.000    0.051    0.000 tuple.py:126(_overlaps)
            1    0.000    0.000    0.046    0.046 __init__.py:299(loads)
            1    0.000    0.000    0.046    0.046 decoder.py:332(decode)
            1    0.046    0.046    0.046    0.046 decoder.py:343(raw_decode)
            3    0.037    0.012    0.046    0.015 {method 'sort' of 'list' objects}
        99462    0.025    0.000    0.025    0.000 {built-in method builtins.min}
        99370    0.022    0.000    0.022    0.000 {built-in method builtins.max}

## How can robustness be ensured, especially considering very large inputs ?

Rodustness can be validated running test cases with varying inputs. The implemented tool functions are meant to help in this regard.
