from utils.errorEnum import ErrorEnum


# Converts a given number to a properly formatted file size
def convertBytes(num):
    for i in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return '%3.2f %s' % (num, i)
        num /= 1024.0


def prefixDot(charList):
    if charList[0] == '.':
        return True
    else:
        return False


def prefixThreeDots(charList):
    if charList[0] == '.' and charList[1] == '.' and charList[2] == '.':
        return True
    else:
        return False


def suffixDot(charList):
    if charList[len(charList) - 1] == '.':
        return True
    else:
        return False


def suffixThreeDots(charList):
    if charList[len(charList) - 1] == '.' and charList[len(charList) - 2] == '.' and charList[len(charList) - 3] == '.':
        return True
    else:
        return False


def computePurity(errorCounter, tracksSample):
    totalPossibleError = tracksSample * len(ErrorEnum)
    return round(100 - round((errorCounter * 100) / totalPossibleError, 2), 2)


def removeSpecialCharFromString(string):
    # Checking first that the differents char are bc of an illegal symbol
    forbiddenChars = ['*', '/', '\\', ':', ';', '?', '<', '>', '\"', '|']
    for x in range(0, len(string)):
        if string[x] in forbiddenChars:
            string[x] = '-'
    return string


def removeSpecialCharFromArray(array):
    forbiddenChars = ['*', '/', '\\', ':', ';', '?', '<', '>', '\"', '|']
    output = []
    for item in array:
        string = ''
        for x in range(0, len(item)):
            if item[x] in forbiddenChars:
                string += '-'
            else:
                string += item[x]
        output.append(string)
    return output


def accentSort(l):
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    l.sort( key=alphanum_key )
