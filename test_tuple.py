import random

import pytest

import tuple

from hypothesis import given, assume
import hypothesis.strategies as st


@st.composite
def generate_tuple_params(draw):
    """ use hypothesis to generate parameter sets """
    result = {}
    result['minval'] = draw(st.integers(min_value=0, max_value=1000))
    result['maxval'] = draw(st.integers(
        min_value=result['minval'], max_value=100000))
    assume(result['maxval'] >= result['minval'])
    result['maxrange'] = draw(st.integers(min_value=1, max_value=1000))
    result['num'] = draw(st.integers(min_value=1, max_value=1000))
    return result


@given(generate_tuple_params())
def generate_tuples_test_composite(params):
    ### use hypothesis composite to generate tuples from random input ###
    # redundant with generate_tuples_test_data. Just to check out hypothesis
    tuple.generate_tuples(**params)

@given(st.data())
def generate_tuples_test_data(data):
    ### draw from hypothesis data to generate tuples from random input ###
    # redundant with generate_tuples_test_composite. Just to check out hypothesis
    x = data.draw(st.integers(min_value=0, max_value=1000))
    y = data.draw(st.integers(min_value=x, max_value=100000))
    r = data.draw(st.integers(min_value=1, max_value=1000))
    n = data.draw(st.integers(min_value=1, max_value=1000))
    tuples = tuple.generate_tuples(x, y, r, n)

def generate_tuples_test_probability():
    ### test value distribution in generated tuples ###
    tuples = tuple.generate_tuples(0, 100, 10, 100000)
    lval_list = [x for (x, _) in tuples]
    rval_list = [y for (_, y) in tuples]
    # check edges
    assert 0 in lval_list
    assert 100 in rval_list
    # check middle part
    for i in range(1, 100):
        assert i in lval_list
        assert i in rval_list

# playing around with hypothesis really ;)
@pytest.mark.parametrize("tuple1, tuple2, output", [
    ((1, 1), (1, 1), (1, 1)),
    ((0, 1), (1, 2), (0, 2)),
    ((3, 5), (2, 5), (2, 5)),
    ((3, 5), (2, 4), (2, 5)),
    ((3, 5), (4, 7), (3, 7)),
])
def merge_test(tuple1, tuple2, output):
    ### test correctness of merge logic ###
    assert tuple._merge(tuple1, tuple2) == output


def verify_tuples_test():
    ### test correctness of verify logic (must raise on overlap) ###
    assert tuple.verify_tuples([(1, 1), (2, 3)])
    assert tuple.verify_tuples([(10, 20), (2, 3)])
    with pytest.raises(tuple.TupleException):
        tuple.verify_tuples([(1, 2), (2, 3)])
    with pytest.raises(tuple.TupleException):
        tuple.verify_tuples([(5, 10), (2, 3), (8, 12)])


def sort_tuples_test():
    assert tuple.sort_tuples([(1, 1), (2, 3)]) == [(1, 1), (2, 3)]
    assert tuple.sort_tuples([(2, 3), (1, 1)]) == [(1, 1), (2, 3)]


@given(generate_tuple_params())
def count_tuples_test(params):
    # simple tests
    assert tuple.count_tuples([]) == 0
    assert tuple.count_tuples([(1, 1)]) == 1
    # run some random tests
    for _ in range(0, 10):
        tuples = tuple.generate_tuples(**params)
        assert tuple.count_tuples(tuples) == params['num']


def overlap_test():
    ### test correctness of overlap logic ###
    assert tuple._overlaps((1, 1), (1, 1)) == True
    assert tuple._overlaps((3, 5), (1, 3)) == True
    assert tuple._overlaps((3, 5), (1, 4)) == True
    assert tuple._overlaps((3, 5), (3, 5)) == True
    assert tuple._overlaps((3, 5), (2, 4)) == True
    assert tuple._overlaps((3, 5), (3, 6)) == True
    assert tuple._overlaps((2, 5), (5, 1)) == True
    assert tuple._overlaps((2, 7), (5, 1)) == True
    assert tuple._overlaps((2, 10), (5, 10)) == True
    assert tuple._overlaps((5, 10), (5, 10)) == True
    assert tuple._overlaps((5, 11), (5, 10)) == True
    assert tuple._overlaps((6, 10), (5, 10)) == True
    assert tuple._overlaps((1, 2), (3, 4)) == False
    assert tuple._overlaps((5, 6), (3, 4)) == False


@pytest.mark.slow
@given(generate_tuple_params())
def naive_strategy_test(params):
    for _ in range(0, 10):
        tuples = tuple.generate_tuples(**params)
        result = tuple.naive_strategy(tuples)
        try:
            tuple.verify_tuples(result)
        except tuple.TupleException as e:
            raise tuple.TupleException(
                f'Validation failed for input data {tuples} with: {e}')


@pytest.mark.slow
@given(generate_tuple_params())
def sort_strategy_test(params):
    for _ in range(0, 10):
        tuples = tuple.generate_tuples(**params)
        result = tuple.sort_strategy(tuples)
        try:
            tuple.verify_tuples(result)
        except tuple.TupleException as e:
            raise tuple.TupleException(
                f'Validation failed for input data {tuples} with: {e}')
