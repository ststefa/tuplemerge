import tuple
import random


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


def test_gen():
    tuples = tuple.generate_tuples(0, 10, 3, 10000)
    lval_list = [x for (x, y) in tuples]
    rval_list = [y for (x, y) in tuples]
    assert 0 in lval_list
    assert 0 not in rval_list
    assert 10 in rval_list
    assert 10 not in lval_list


def _generate_test_set():
    testset = {}
    testset['minval'] = random.randint(0, 10000)
    testset['maxval'] = testset['minval']+random.randint(0, 10000)
    testset['maxrange'] = random.randint(100, 10000)
    testset['num'] = random.randint(0, 100000)
    return testset


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
