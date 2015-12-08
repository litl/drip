Drip
====

*somewhat fast data science*

![Mr. Coffee](http://goo.gl/G15qgG)

Drip is a Python library for exploring multivariate datasets. It
supports incremental filtering and efficient data queries using
filters back by [bitarrays](https://github.com/ilanschnell/bitarray).
Intersections, unions, nots, and xors of these filters are very fast.

# Usage

Drip operates on ordered lists of data and is agnostic about what the
data itself is. For example, a simple list of integers will do.

    >>> data = list(range(100))

The fundamental building block in Drip is the filter. A filter is
created against a given list of data with the filter() function. A
predicate is specified when creating a filter with the `pred` keyword
arg. Predicates can be any boolean function, but some common tests are
included in the drip module for convenience.

* eq (Equality)
* gt (Greater than)
* ge (Greater than or equal)
* lt (Less than)
* le (Less than or equal)

Any number of filters can be created on given dataset.

    >>> ge45 = drip.filter(data, pred=drip.ge(45))
    >>> le55 = drip.filter(data, pred=drip.le(55))

Queries are performed on the data with filters or combination of
filters. Filters may be combined or modified with any of the standard
Python bitwise operators such as `&`, `|`, `~`, and `^`.

_`query()` returns an iterable generator, so here we expand the results
into a list._

    >>> list(drip.query(data, ge45 & le55))
    [45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55]

A more typical dataset might be a list of tuples. Here we'll use a list
of words enumerated with sequential ids.

    >>> with open("/usr/share/dict/words", "r") as fd:
    ...    words = [l[:1] for l in fd.readlines()]
    >>> data = list(enumerate(words))

For convenience, the item_keys() function can be used to create key
functions for retrieving the columns of your data.

    >>> id, word = drip.item_keys(2)

These key functions are passed to filter() to select the column to
apply to the predicate.

    >>> dogs = drip.filter(data, key=word, pred=lambda x: "dog" in x)
    >>> cats = drip.filter(data, key=word, pred=lambda x: "cat" in x)

Queries may be performed on the individual filters.

    >>> len(list(drip.query(data, dogs)))
    222
    >>> len(list(drip.query(data, cats)))
    2257

Filters may be combined with bitwise operators.

    >>> list(drip.query(data, dogs & cats))
    [(31723, 'cathodograph'), (31724, 'cathodography'), (56575, 'dogcatcher')]

    >>> len(list(drip.query(data, dogs & ~cats)))
    219

## CSV Data Example

Here, we're working with the flight data file originally from the
[crossfilter demo](http://square.github.io/crossfilter/).

    >>> with open('flights-3m.csv', 'r') as csvfile:
    ...    data = list(csv.reader(csvfile))[1:]

Define applicable key functions corresponding to the columns of our data.

    >>> date, delay, dist, origin, dest = drip.item_keys((str, int, int, str, str))

Create some filters on that data: one to select all flights departing
L.A. and one to select all flights arriving in Oakland.

    >>> from_lax = drip.filter(data, key=origin, pred=drip.eq('LAX'))
    >>> to_oak = drip.filter(data, key=dest, pred=drip.eq('OAK'))

Query these filters individually if you like.

    >>> len(list(drip.query(data, from_lax)))
    10137

    >>> len(list(drip.query(data, to_oak)))
    9920

Peak at some data.

    >>> next(drip.query(data, to_oak))
    ['01010625', '-6', '361', 'ONT', 'OAK']

Filter based on something other than equality, such as all flights that
were more than 90 minutes late.

    >>> very_late = drip.filter(data, key=delay, pred=drip.gt(90))
    >>> len(list(drip.query(data, very_late)))
    4287

Combine filters using python's bitwise operators.

    >>> len(list(drip.query(data, from_lax | to_oak)))
    18067

    >>> len(list(drip.query(data, from_lax & to_oak)))
    1990

    >>> len(list(drip.query(data, from_lax & to_oak & very_late)))
    39

Alternatively, refine an existing query with an additional predicate.

    >>> lax_to_oak = drip.filter(data, from_lax, key=dest, pred=drip.eq('OAK'))
    >>> len(list(drip.query(data, lax_to_oak)))
    1990

Applying the predicate to create the filters is the slowest part.

    >>> len(data)
    231083

    : %timeit from_lax = drip.filter(data, key=origin, pred=drip.eq('LAX'))
    1 loops, best of 3: 287 ms per loop

    : %timeit very_late = drip.filter(data, key=delay, pred=drip.gt(90))
    1 loops, best of 3: 505 ms per loop

Refining existing filters is faster than creating new ones from the raw
data.

    : %timeit to_oak = drip.filter(data, key=dest, pred=drip.eq('OAK'))
    1 loops, best of 3: 288 ms per loop

    : %timeit lax_to_oak = drip.filter(data, from_lax, key=dest, pred=drip.eq('OAK'))
    10 loops, best of 3: 105 ms per loop

Once the filter(s) are created, queries are pretty fast.

    : %timeit list(drip.query(data, from_lax))
    100 loops, best of 3: 13.8 ms per loop

Combining filters does not slow things down.

    : %timeit list(drip.query(data, from_lax & to_oak))
    100 loops, best of 3: 12.7 ms per loop

    : %timeit list(drip.query(data, from_lax & to_oak & very_late))
    100 loops, best of 3: 12.4 ms per loop
