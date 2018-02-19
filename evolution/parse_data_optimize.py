'''
Functions that help reading large data file by reading only some models and skipping the others.
'''

def get_skip_models(file_size, SKIP_PER_SIZE=5_000_000):
    '''
    Return the number of models to be skipped after each model is read
    based on the file_size given in bytes. For small files no models are skipped and the
    return value is 0.

    :param SKIP_PER_SIZE:
        Skips file_size/SKIP_PER_SIZE number of models if the file size in bytes
        is greater than SKIP_PER_SIZE.
        The smaller the number the faster the program reads the data file.

    >>> get_skip_models(file_size=999_999, SKIP_PER_SIZE=1_000_000)
    0

    >>> get_skip_models(file_size=1_000_000, SKIP_PER_SIZE=1_000_000)
    1

    >>> get_skip_models(file_size=1_000_000, SKIP_PER_SIZE=1_000_000)
    1

    >>> get_skip_models(file_size=7_300_000, SKIP_PER_SIZE=1_000_000)
    7
    '''

    return int(file_size / SKIP_PER_SIZE)


# Run the unit tests
if __name__ == "__main__":
    import doctest
    doctest.testmod()