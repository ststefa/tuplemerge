import tuple
import random
import pytest


def _generate_test_set():
    """ Helper method to generate a random input dataset """
    test_set = {}
    test_set['minval'] = random.randint(0, 1000)
    test_set['maxval'] = test_set['minval']+random.randint(0, 1000)
    test_set['maxrange'] = random.randint(10, 100)
    test_set['num'] = random.randint(0, 100000)
    return test_set


def test_generate_tuples():
    tuples = tuple.generate_tuples(0, 10, 3, 10000)
    lval_list = [x for (x, y) in tuples]
    rval_list = [y for (x, y) in tuples]
    # check edges
    assert 0 in lval_list
    assert 0 not in rval_list
    assert 10 in rval_list
    assert 10 not in lval_list
    # check middle part
    for i in range(1, 10):
        assert i in lval_list
        assert i in rval_list


def test_verify_tuples():
    assert tuple.verify_tuples([(1, 1), (2, 3)])
    assert tuple.verify_tuples([(10, 20), (2, 3)])
    with pytest.raises(tuple.TupleException):
        tuple.verify_tuples([(1, 2), (2, 3)])
    with pytest.raises(tuple.TupleException):
        tuple.verify_tuples([(5, 10), (2, 3), (8, 12)])


def test_sort_tuples():
    assert tuple.sort_tuples([(1, 1), (2, 3)]) == [(1, 1), (2, 3)]
    assert tuple.sort_tuples([(2, 3), (1, 1)]) == [(1, 1), (2, 3)]


def test_count_tuples():
    # simple tests
    assert tuple.count_tuples([]) == 0
    assert tuple.count_tuples([(1, 1)]) == 1
    # run some random tests
    for _ in range(0, 10):
        testset = _generate_test_set()
        tuples = tuple.generate_tuples(**testset)
        assert tuple.count_tuples(tuples) == testset['num']


def test_overlap():
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


def test_merge():
    assert tuple._merge((1, 1), (1, 1)) == (1, 1)
    assert tuple._merge((0, 1), (1, 2)) == (0, 2)
    assert tuple._merge((3, 5), (2, 5)) == (2, 5)
    assert tuple._merge((3, 5), (2, 4)) == (2, 5)
    assert tuple._merge((3, 5), (4, 7)) == (3, 7)


def test_naive_strategy():
    for _ in range(0, 10):
        testset = _generate_test_set()
        print(testset)
        tuples = tuple.generate_tuples(**testset)
        result = tuple.naive_strategy(tuples)
        try:
            tuple.verify_tuples(result)
        except tuple.TupleException as e:
            raise tuple.TupleException(
                f'Validation failed for input data {tuples} with: {e}')


def test_sort_strategy():
    for _ in range(0, 10):
        testset = _generate_test_set()
        print(testset)
        tuples = tuple.generate_tuples(**testset)
        result = tuple.sort_strategy(tuples)
        try:
            tuple.verify_tuples(result)
        except tuple.TupleException as e:
            raise tuple.TupleException(
                f'Validation failed for input data {tuples} with: {e}')
