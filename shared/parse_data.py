# Shared functions for parsing the input data file
import re

def read_model_number(line):
    '''
    Returns the model number if the line corresponds to the start of the new model.
    Otherwise, returns None.

    >>> read_model_number(' Nmodel=103271 Time= 7.594608453E+14 s =  2.406586196E+07 y  con zone=shell')
    103271

    >>> read_model_number('something else')

    '''
    if not line.startswith(' Nmodel='): return None
    match = re.search("Nmodel\s*=\s*([^\s]+)", line)
    if match: return int(match.group(1))
    return None

def variable_with_name(line, name, index=0):
    '''
    Extracts a variable value from a string.
    >>> variable_with_name('var1=one var2=two var3=three', 'var2')
    'two'

    >>> variable_with_name('var1=one var 2 = two2', 'var 2')
    'two2'

    >>> variable_with_name('var 2  =  two   var3=123', 'var 2')
    'two'

    >>> variable_with_name('', 'var 2')


    Supply an index if the variable is used multiple times
    >>> variable_with_name('var1=one var1=two var1=three', 'var1',1)
    'two'

    >>> variable_with_name('var1=one var1=two var1=three', 'var1',2)
    'three'
    '''
    p = re.compile(f"{re.escape(name)}\s*=\s*([^\s]+)")
    result = p.findall(line)
    if result == None: return None
    if len(result)-1 < index: return None
    return result[index]

import os

def reverse_readline(filename, buf_size=8192):
    """
    A generator that returns the lines of a file in reverse order
    Source: https://stackoverflow.com/a/23646049/297131
    """
    with open(filename) as fh:
        segment = None
        offset = 0
        fh.seek(0, os.SEEK_END)
        file_size = remaining_size = fh.tell()
        while remaining_size > 0:
            offset = min(file_size, offset + buf_size)
            fh.seek(file_size - offset)
            buffer = fh.read(min(remaining_size, buf_size))
            remaining_size -= buf_size
            lines = buffer.split('\n')
            # the first line of the buffer is probably not a complete line so
            # we'll save it and append it to the last line of the next buffer
            # we read
            if segment is not None:
                # if the previous chunk starts right from the beginning of line
                # do not concact the segment to the last line of new chunk
                # instead, yield the segment first 
                if buffer[-1] is not '\n':
                    lines[-1] += segment
                else:
                    yield segment
            segment = lines[0]
            for index in range(len(lines) - 1, 0, -1):
                if len(lines[index]):
                    yield lines[index]
        # Don't yield None if the file was empty
        if segment is not None:
            yield segment

# Run the unit tests
if __name__ == "__main__":
    import doctest
    doctest.testmod()