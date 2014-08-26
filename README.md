Drip
====

*somewhat fast filtering*

![Mr. Coffee](http://goo.gl/G15qgG)

# Example Usage

Load some interesting data into a list. Here, we're working with the
flight data file from the crossfilter demo.

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

Filter based on something other than equality, such as all flights that were more than 90 minutes late.

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

Refining existing filters is faster than creating new ones from the raw data.

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
