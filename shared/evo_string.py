import math

def try_convert_to_float(text):
    try:
        return float(text)
    except ValueError as verr:
        pass # do job to handle: s does not contain anything convertible to int


def ordinal(number):
    """
    Converts integer number (1, 2, 3 etc) to an ordinal number representation (1st, 2nd, 3rd etc)
    https://stackoverflow.com/a/20007730/297131


    :param number: An integer number

    >>> [ordinal(n) for n in range(0,32)]
    ['0th', '1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th', '13th', '14th', '15th', '16th', '17th', '18th', '19th', '20th', '21st', '22nd', '23rd', '24th', '25th', '26th', '27th', '28th', '29th', '30th', '31st']
    """

    return "%d%s" % (number,"tsnrhtdd"[(math.floor(number/10)%10!=1)*(number%10<4)*number%10::4])

# Run the unit tests
if __name__ == "__main__":
    import doctest
    doctest.testmod()