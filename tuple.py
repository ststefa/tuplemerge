#!/usr/bin/env python3
# $Id: ststefa 20201118 $

import argparse
import json
import random
import sys
from typing import List, Tuple

# A RangeTuple represents a sequential range of natural numbers
RangeTuple = Tuple[int, int]


def generate_tuples(minval: int, maxval: int, maxrange: int, num: int) -> List[RangeTuple]:
    """ Generate a list of (minval, maxval) tuples. Any generated tuple (x, y)
        spans one or more numbers (i.e. x <= y)

        :param minval: The minimum lower bound for any tuple
        :param maxval: The maximum upper bound for any tuple
        :param maxrange: The maximum number of values any tuple can contain
        :param num: The number of tuples to generate
        :raises: TupleException: In case of invalid args (e.g. minval>maxval)
    """
    if minval < 0 or maxval < 0 or maxrange < 1 or num < 1:
        raise TupleException(
            'minval- and maxval must be >= 0, maxrange and num must be > 0')
    if maxval < minval:
        raise TupleException('maxval must be bigger or equal to minval')
    result: List[RangeTuple] = []
    for _ in range(num):
        lower = random.randint(minval, maxval)
        upper = random.randint(lower, min(maxval, lower+maxrange))
        # add tuple to list (note double "(())")
        result.append((lower, upper))
    return result


def merge_tuples(strategy: str, tuples: List[RangeTuple]) -> List[RangeTuple]:
    """ Dynamically invoke <strategy>_strategy() function

        :param strategy: The merge strategy to use. A corresponding method
            <strategy>_strategy() must exist. If a strategy is added the
            parser also needs to be extended to accept the new choice.
    """
    # Using a class maybe preferrable over using globals(). Omitting here for brevity.
    # see https://www.danielmorell.com/blog/dynamically-calling-functions-in-python-safely
    try:
        func = globals()[strategy + '_strategy']
    except KeyError as e:
        raise TupleException(f'No such merge strategy: {e}')
    result = func(tuples)
    return result


def verify_tuples(tuples: List[RangeTuple]) -> List[RangeTuple]:
    """ Check list of tuples for overlaping elements

        :raises: TupleException: If two tuples overlap
    """
    # create a copy, we want to change the input
    result = tuples[:]
    result.sort(key=lambda elem: elem[0])
    elem = result.pop()
    while len(result) > 0:
        next_elem = result.pop()
        if _overlaps(elem, next_elem):
            raise TupleException(f'Elements {elem} and {next_elem} overlap')
        elem = next_elem
    return tuples


def sort_tuples(tuples: List[RangeTuple]) -> List[RangeTuple]:
    """ Sort list of tuples by lower boundary """
    tuples.sort(key=lambda elem: elem[0])
    return tuples


def count_tuples(tuples: List[RangeTuple]) -> int:
    """ Count number of tuples """
    return len(tuples)


def naive_strategy(tuples: List[RangeTuple]) -> List[RangeTuple]:
    """ Strategy:
        - For every element in input list
            - Iterate over result list and merge with any overlapping
              element, removing the merged elements from the result
            - Add element to result list
        The strategy iterates over the input list. For every element it
        iterates over the result list. This leads to a complexity of O(n^2).
    """
    result = []
    while tuples:
        current_tuple = tuples.pop()
        # we need to create a copy of the result list because we might remove
        # elements inside the loop which would lead to incorrect results
        iter_list = result[:]
        for result_tuple in iter_list:
            if _overlaps(current_tuple, result_tuple):
                result.remove(result_tuple)
                current_tuple = _merge(current_tuple, result_tuple)
        result.append(current_tuple)
    return result


def sort_strategy(tuples: List[RangeTuple]) -> List[RangeTuple]:
    """ Strategy
        - Sort the list by lower tuple value
        - For every element in input list
            - Test if element overlaps with last element of result
            - If so, replace last element with merged tuple
            - Otherwise append element to result
        The strategy iterates once over the list of input tuples and therefore
        has a complexity of O(n)
    """
    # sort by first tuple element
    tuples.sort(key=lambda elem: elem[0])
    result = [tuples[0]]
    for input_tuple in tuples[1:]:
        last_tuple = result.pop()
        if _overlaps(input_tuple, last_tuple):
            result.append(_merge(input_tuple, last_tuple))
        else:
            result.append(last_tuple)
            result.append(input_tuple)
    return result


def _overlaps(tuple1: RangeTuple, tuple2: RangeTuple) -> bool:
    """ Helper method to test if two RangeTuples overlap. (a,b) and (c,d) are
        considered overlapping if the boundaries of one tuple are located within
        the boundaries of the other tuple. I.e. in these cases:

            b >= c >= a
            b >= d >= a
            d >= a >= c
            d >= b >= c
    """
    if tuple1[1] >= tuple2[0] >= tuple1[0]:
        return True
    if tuple1[1] >= tuple2[1] >= tuple1[0]:
        return True
    if tuple2[1] >= tuple1[0] >= tuple2[0]:
        return True
    if tuple2[1] >= tuple1[1] >= tuple2[0]:
        return True
    return False


def _merge(tuple1: RangeTuple, tuple2: RangeTuple) -> RangeTuple:
    """ Merge two overlapping RangeTuples and return the result spanning the
        maximum range, i.e.

            _merge((a, b), (c, d)) -> (min(a, c), max(b, d))
    """
    lower = min(tuple1[0], tuple2[0])
    upper = max(tuple1[1], tuple2[1])
    return (lower, upper)


def init_parser() -> argparse.ArgumentParser:
    """ Prepare parser with possible invocation args
    """

    parser = argparse.ArgumentParser(
        description='Tuple exercise 2. Generate, merge and verify lists of tuples.', formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog='Choose command')

    root_parsers = parser.add_subparsers(dest='object', title='Tuple commands')

    sub_parser = root_parsers.add_parser('gen',
                                         help='Randomly generate n tuples (min, max) and dump them to stdout in json format.')
    sub_parser.add_argument(
        'minval', type=int, help='smallest possible lower tuple value')
    sub_parser.add_argument(
        'maxval', type=int, help='largest possible upper tuple value')
    sub_parser.add_argument(
        'maxrange', type=int, help='largest tuple range min..max (i.e. max-min <= range)')
    sub_parser.add_argument('num', type=int, help='number of tuples')
    sub_parser.set_defaults(func=generate_tuples)

    sub_parser = root_parsers.add_parser('merge',
                                         help='Read a list of tuples in json format from stdin and merge them so that overlapping tuples are combined. Two tuples are considered overlapping if both contain at least one identical element.')
    sub_parser.add_argument('-s', '--strategy', default="sort", choices=['naive', 'sort'],
                            help='Strategy to use for computation')
    sub_parser.set_defaults(func=merge_tuples)

    sub_parser = root_parsers.add_parser('sort',
                                         help='Read a list of tuples in json format from stdin, sort by lower bound and print to stdout.')
    sub_parser.set_defaults(func=sort_tuples)

    sub_parser = root_parsers.add_parser('verify',
                                         help='Verify if a list of tuples does contain overlapping elements')
    sub_parser.set_defaults(func=verify_tuples)

    sub_parser = root_parsers.add_parser('count',
                                         help='Count the number of tuples')
    sub_parser.set_defaults(func=count_tuples)

    return parser


class TupleException(Exception):
    pass


def main():
    args = init_parser().parse_args()
    # see http://stackoverflow.com/questions/16878315/what-is-the-right-way-to-treat-python-argparse-namespace-as-a-dictionary#16878364
    arg_list = dict(vars(args))
    del arg_list['func']
    del arg_list['object']
    if args.object != 'gen':
        input_data = json.loads(sys.stdin.read())
        arg_list['tuples'] = input_data
    result = args.func(**arg_list)
    print(json.dumps(result))


if __name__ == '__main__':
    try:
        main()
        sys.exit(0)
    except TupleException as e:
        sys.stderr.write(f'Error: {e}\n')
        sys.exit(1)
