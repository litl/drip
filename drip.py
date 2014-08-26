import bitarray
import collections
import copy
import functools
import math
import operator


def identity(x):
    return x


def filter(data, fil=None, key=identity, pred=None):
    """Create filter on the specified data

    This function can be used to create a new filter from the raw data
    or it can be used to refine a previously created filter.

    The returned filter is valued as a bitarray, and can be used with
    the python bitwise operators. i.e. two filters can be combined via
    bitwise operations to create a new filter.
    """
    if fil is None:
        fil = bitarray.bitarray(len(data))
        fil.setall(True)

    if pred is None:
        return fil

    new_fil = bitarray.bitarray(len(fil))
    for i, b in enumerate(fil):
        new_fil[i] = b and pred(key(data[i]))
    return new_fil


def query(data, fil):
    """Return a generator iterating over the filtered data"""
    return (data[i] for i, b in enumerate(fil) if b)


def _compose(*functions):
    def compose(f, g):
        return lambda x: f(g(x))

    return functools.reduce(compose, functions)


def item_keys(items):
    """Return key functions for data rows

    This is useful if you're working with data loaded from e.g. a CSV
    file.

    $ with open('flights-3m.csv', 'r') as csvfile:
    ... data = list(csv.reader(csvfile))[1:]

    $ date, delay, dist, origin, dest = drip.item_keys(5)

    $ origin(data[13])
    'ONT'

    $ delay(data[13])
    '-6'

    Each of these functions now reports the corresponding value from
    the data row.

    However, since the data is loaded from CSV all values are raw
    strings. If we want the values to have other types, we can pass
    an iterable of constructor functions which return the desired
    types:

    $ date, delay, dist, origin, dest = \
        drip.item_keys((str, int, int, str, str))

    $ delay(data[13])
    -6
    """
    try:
        _ = (f for f in items)
    except TypeError:
        # if it's not an iterable, expect a number
        return map(operator.itemgetter, xrange(items))
    else:
        return [_compose(f, operator.itemgetter(i))
                for i, f in enumerate(items)]


# The following functions are useful for succinctly defining
# predicates for filtering data.


# Like functools.partial but swaps the arg order.
def _rev(f, x):
    def g(y):
        return f(y, x)
    return g


def eq(x):
    return functools.partial(operator.eq, x)


def gt(x):
    return _rev(operator.gt, x)


def ge(x):
    return _rev(operator.ge, x)


def lt(x):
    return _rev(operator.lt, x)


def le(x):
    return _rev(operator.le, x)
