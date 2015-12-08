"""Drip is a library for exploring multivariate datasets."""


import bitarray
import functools
import operator

__version__ = "1.0.8"


def _identity(x):
    return x


def filter(data, fil=None, key=_identity, pred=None):
    """Creates filter on the specified data.

    This function can be used to create a new filter from the raw data
    or it can be used to refine a previously created filter.

    The returned filter is typed as a bitarray, and can be used with
    the python bitwise operators. i.e. two filters can be combined via
    bitwise operations to create a new filter.

    Args:
    data -- List of arbitrary data
    fil -- Existing filter to refine (optional).  When specified, only
           the data satisfying this filter will be tested for inclusion
           in the new filter.
    key -- The key function to be applied to datum. The returned value
           is what is passed to the predicate function. The default is
           the identity function which returns the full datum itself.
    pred -- The boolean predicate function is the test that is applied
            to each datum to test for inclusion in the filter. Note
            that the drip module provides the functions eq(), gt(),
            ge(), lt(), le() for this purpose.

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
    """Returns a generator iterating over the filtered data.

    Args:
    data -- The list of arbitrary data that the filter was created on.
    fil -- The filter to apply to the data as created by the filter()
           function.
    """
    return (data[i] for i, b in enumerate(fil) if b)


def _compose(*functions):
    def compose(f, g):
        return lambda x: f(g(x))

    return functools.reduce(compose, functions)


def item_keys(items):
    """Returns callables fetching values by positional index

    Args:
    items -- Specifies the number of key functions to generate. Value
             is either an int or an iterable of constructor functions.

        (int arg) Specifies the number of key functions to return.

        (iterable arg) The iterable specifies the constructor functions
                       to use for each key function to convert to the
                       appropriate type. This is particularly useful
                       when dealing with something like CSV data which
                       may be valued as strings regardless of the
                       original data type.

    Example usage:

    This is useful if you're working with data loaded from e.g. a CSV
    file which each datum is represented as a tuple of strings.

    $ with open('flights-3m.csv', 'r') as csvfile:
    ... data = list(csv.reader(csvfile))[1:]

    $ date, delay, dist, origin, dest = drip.item_keys(5)

    $ origin(data[13])
    'ONT'

    $ delay(data[13])
    '-6'

    Each of these functions now reports the corresponding value from
    the data row.

    However, since the data is stored as raw strings we are limited as
    to the predicates we can apply to it. If we want the values to be
    typed appropriately, we can pass an iterable of constructor
    functions which return the desired types.

    $ date, delay, dist, origin, dest = \
        drip.item_keys((str, int, int, str, str))

    $ delay(data[13])
    -6
    """
    try:
        iter(f for f in items)
    except TypeError:
        # if it's not an iterable, expect a number
        return map(operator.itemgetter, range(items))
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
    """Equality predicate"""
    return functools.partial(operator.eq, x)


def gt(x):
    """Greater than predicate"""
    return _rev(operator.gt, x)


def ge(x):
    """Greater than or equal predicate"""
    return _rev(operator.ge, x)


def lt(x):
    """Less than predicate"""
    return _rev(operator.lt, x)


def le(x):
    """Less than or equal predicate"""
    return _rev(operator.le, x)
