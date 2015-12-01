__author__ = 'andreuke'

from tabular import solve


def minimize(ones, dc):
    length = len(ones[0])
    minterms, dontcares = __convertInput(ones, dc)
    print 'algo inputs', minterms, dontcares
    output = solve(minterms, dontcares, length)

    return __convertOutput(output, length)


def __convertInput(ones, dc):
    minterms = []
    dontcares = []

    for one in ones:
        mList = __stringToMinterms(one)
        minterms = list(set(minterms) | set(mList))

    for d in dc:
        dcList = __stringToMinterms(d)
        dontcares = list(set(dontcares) | set(dcList))

    return minterms, dontcares


def __convertOutput(output, length):
    ones = []

    solutions = output[0][5:].replace(' ', '').split('+')

    for s in solutions:
        ones.append(__literalsToBit(s, length))

    return ones


def __stringToMinterms(string):
    minterms = []

    results = ['']
    for char in string:
        value = []
        if char == '-':
            value.append('0')
            value.append('1')
        else:
            value.append(char)

        # Append values
        newStrings = []
        for v in value:
            for r in results:
                newStrings.append(r+v)
        results = newStrings

    for r in results:
        minterm = int(r, 2)
        minterms.append(minterm)

    minterms.sort()

    return minterms



def __literalsToBit(literals, length):
    ones = []
    zeros = []

    i = 0
    while i < len(literals):
        letter = literals[i]

        index = ord(letter) - ord('A')

        if i < len(literals)-1 and literals[i+1] == "'":
            zeros.append(index)
            i += 1
        else:
            ones.append(index)
        i += 1

    bits = ""
    for i in range(length):
        if i in ones:
            bits += '1'
        elif i in zeros:
            bits += '0'
        else:
            bits += '-'

    return bits
