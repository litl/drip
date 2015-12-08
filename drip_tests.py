import drip


def test_filter_nopred():
    data = list(range(100))
    fil = drip.filter(data)
    for b in fil:
        assert b


def test_filter():
    data = list(range(100))
    ge25 = drip.filter(data, pred=drip.ge(25))
    for i, b in enumerate(ge25):
        assert b == int(i >= 25)

    le75 = drip.filter(data, pred=drip.le(75))
    for i, b in enumerate(le75):
        assert b == int(i <= 75)

    for i, b in enumerate(ge25 & le75):
        assert b == int(25 <= i <= 75)


def test_query():
    data = list(range(100))
    ge25 = drip.filter(data, pred=drip.ge(25))
    results = list(drip.query(data, ge25))
    assert results == list(range(25, 100))


def test_item_keys_int():
    keys = drip.item_keys(5)
    datum = ['a', 'b', 'c', 'd', 'e']
    for i, k in enumerate(keys):
        assert k(datum) == datum[i]


def test_item_keys_iterable():
    i, s, f, l = drip.item_keys((int, str, float, list))
    datum = ["42", 42, "42.0", range(42)]
    assert i(datum) == 42
    assert s(datum) == "42"
    assert f(datum) == 42.0
    assert l(datum) == list(range(42))


def test_eq():
    assert drip.eq('foo')('foo')
    assert not drip.eq('foo')('bar')


def test_gt():
    assert drip.gt(3)(4)
    assert not drip.gt(3)(3)


def test_ge():
    assert drip.ge(3)(4)
    assert drip.ge(3)(3)
    assert not drip.ge(4)(3)


def test_lt():
    assert drip.lt(4)(3)
    assert not drip.lt(3)(3)


def test_le():
    assert drip.le(4)(3)
    assert drip.le(3)(3)
    assert not drip.le(3)(4)
