def non_increasing(L):
    '''
    >>> non_increasing([1,2,3])
    False

    >>> non_increasing([3,2,1])
    True

    >>> non_increasing([3,2,2,1])
    True
    '''
    return all(x>=y for x, y in zip(L, L[1:]))

def non_decreasing(L):
    '''
    >>> non_decreasing([1,2,3])
    True

    >>> non_decreasing([1,2,2,3])
    True

    >>> non_decreasing([3,2,1])
    False

    >>> non_decreasing([3,2,2,1])
    False
    '''
    return all(x<=y for x, y in zip(L, L[1:]))

def monotonic(L):
    '''
    >>> monotonic([1,2,3,4])
    True

    >>> monotonic([1,2,3,3])
    True

    >>> monotonic([4,3,2,1,1])
    True

    >>> monotonic([1,2,3,2])
    False

    >>> monotonic([4,3,3,5])
    False
    '''
    return non_increasing(L) or non_decreasing(L)


# Run the unit tests
if __name__ == "__main__":
    import doctest
    doctest.testmod()
