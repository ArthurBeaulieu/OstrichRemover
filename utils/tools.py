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


def computePurity(errorCounter, folderInfo):
    totalTracks = (folderInfo.flacCounter + folderInfo.mp3Counter) * 17 # Enum length minus 1 (ErrorCode 17 doesn't concerns a track but an album)
    return round(100 - round((errorCounter * 100) / totalTracks, 2), 2)


def getTopicStringFromErrorCode(errorCode):
    topic = '                  '
    if errorCode == 0:
        topic = '--- Release artists'
    elif errorCode == 1 or errorCode == 3 or errorCode == 4:
        topic = '-------------- Year'
    elif errorCode == 2 or errorCode == 5 or errorCode == 6:
        topic = '------------- Album'
    elif errorCode == 7:
        topic = '- Disc/TrackNumber'
    elif errorCode == 8 or errorCode == 9:
        topic = '----------- Artists'
    elif errorCode == 10:
        topic = '------------- Title'
    elif errorCode == 14:
        topic = '- Album Total Track'
    elif errorCode == 15:
        topic = '-- Album Total Disc'
    elif errorCode == 16:
        topic = '-------- Album Year'
    return topic
