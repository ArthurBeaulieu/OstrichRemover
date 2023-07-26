# Python imports
import os
import datetime
import json
import icu
# Project imports
from src.utils.errorEnum import ErrorEnum
from src.utils.tools import createDirectory, removeSpecialCharFromString


# Generate an JSON file from the albumTesters array
def computeFillReport(version, duration, folderInfo, albumTesters, errorCounter, purity):
    # Creating output dict object
    now = datetime.datetime.now()
    output = {
        'date': "{}-{}-{}".format(now.year, now.month, now.day),
        'version': version,
        'elapsedSeconds': duration,
        'folderInfo': _computeFolderInfo(folderInfo, errorCounter, purity),
        'artists': []
    }
    currentArtistName = ''
    currentArtist = {}
    for albumTester in albumTesters:
        albumPathList = albumTester.preservedPath
        if currentArtistName != albumPathList[len(albumPathList) - 2]:  # Current Artist has changed
            if currentArtist != {}:  # Avoid to add the first empty artist when loop starts
                output['artists'].append(currentArtist)
                currentArtist = {}
            currentArtistName = albumPathList[len(albumPathList) - 2]
            currentArtist['name'] = currentArtistName
            currentArtist['albums'] = []
        album = {
            'title': albumPathList[len(albumPathList) - 1],
            'errors': [],
            'tracks': []
        }
        for error in albumTester.errors:
            album['errors'].append(error.value)
        for trackTester in albumTester.tracks:
            if trackTester.errorCounter > 0:
                track = {
                    'title': trackTester.track.fileName,
                    'errors': []
                }
                for error in trackTester.errors:
                    track['errors'].append(error.value)
                album['tracks'].append(track)
        currentArtist['albums'].append(album)
    output['artists'].append(currentArtist)
    return output


# Generate an JSON file from the metaAnalyzer class
def computeMetaAnalyzeReport(version, duration, metaAnalyzer):
    # Creating output dict object
    now = datetime.datetime.now()
    output = {
        'date': "{}-{}-{}".format(now.year, now.month, now.day),
        'version': version,
        'elapsedSeconds': duration,
        'metaAnalyze': metaAnalyzer.metaAnalysis,
        'dumps': metaAnalyzer.dumps
    }
    return output


# Generate an JSON file from the stats class
def computeStatReport(version, duration, artists, genres, labels, path):
    # Creating output dict object
    collator = icu.Collator.createInstance(icu.Locale('fr_FR.UTF-8'))
    now = datetime.datetime.now()
    output = {
        'date': "{}-{}-{}".format(now.year, now.month, now.day),
        'version': version,
        'elapsedSeconds': duration,
        'count': {
            'artists': len(artists),
            'genres': len(genres),
            'labels': len(labels)
        },
        'folderPath': path,
        'artists': sorted(artists, key=lambda x: collator.getSortKey(x['artist'])),
        'genres': sorted(genres, key=collator.getSortKey),
        'labels': sorted(labels, key=collator.getSortKey)
    }
    return output



# Convert the folderInfo object into a returned dict
def _computeFolderInfo(folderInfo, errorCounter, purity):
    output = {
        'name': folderInfo.folder,
        'files': folderInfo.filesCounter,
        'folders': folderInfo.foldersCounter,
        'size': folderInfo.folderSize,
        'flacCount': folderInfo.flacCounter,
        'mp3Count': folderInfo.mp3Counter,
        'flacPercentage': folderInfo.flacPercentage,
        'mp3Percentage': folderInfo.mp3Percentage,
        'jpgPercentage': folderInfo.jpgPercentage,
        'pngPercentage': folderInfo.pngPercentage,
        'jpgCount': folderInfo.jpgCounter,
        'pngCount': folderInfo.pngCounter,
        'artistsCount': folderInfo.artistsCounter,
        'albumsCount': folderInfo.albumsCounter,
        'tracksCount': folderInfo.tracksCounter,
        'coversCount': folderInfo.coversCounter,
        'errorsCount': errorCounter,
        'possibleErrors': folderInfo.tracksCounter * len(ErrorEnum),
        'purity': purity
    }
    return output


# Save the output json file
def saveReportFile(report, type, minify, path):
    # Set default path to dump folder if not provided
    if path is None:
        path = 'dump'
    # Ensure folder is created if not existing
    createDirectory(path)
    # Then name and dump report as JSON file
    fileName = "OstrichRemover-{}-{}".format(type, datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
    with open('{}/{}.json'.format(path, fileName), 'w') as file:
        if minify == True:
            json.dump(report, file, separators=(',', ':'))
        else:
            json.dump(report, file, indent=2)


# Save the output json file
def saveGeneratedJSONFile(elements, contributions, type, path):
    # Set default path to dump folder if not provided
    if path is None:
        path = 'dump'
    # Ensure folder is created if not existing
    path = '{}/{}/txt'.format(path, type);
    createDirectory(path)
    for element in elements:
        # Then name and dump report as JSON file
        filePath = "{}".format('{}/{}.json'.format(path, element))
        jsonContent = generateOutputJSON(type, element, contributions[element])
        # Only create JSON if not alreay exists
        if not os.path.exists(filePath):
            with open(filePath, 'w', encoding='utf-8') as file:
                json.dump(jsonContent, file, indent=2, ensure_ascii=False)
        # Otherwise, mudt only update useful values and not erase anything
        else:
            with open(filePath, 'r', encoding='utf-8') as file:
                fData = json.loads(file.read())
                if type == 'artists':
                    if fData['realName'] != jsonContent['realName'] or fData['originCountry'] != jsonContent['originCountry'] or fData['yearsActive'] != jsonContent['yearsActive'] or sorted(fData['artists']) != sorted(jsonContent['artists']) or sorted(fData['genres']) != sorted(jsonContent['genres']) or sorted(fData['labels']) != sorted(jsonContent['labels']):
                        fData['realName'] = jsonContent['realName']
                        fData['originCountry'] = jsonContent['originCountry']
                        fData['yearsActive'] = jsonContent['yearsActive']
                        fData['genres'] = jsonContent['genres']
                        fData['labels'] = jsonContent['labels']
                        with open(filePath, 'w', encoding='utf-8') as file:
                            json.dump(fData, file, indent=2, ensure_ascii=False)
                elif type == 'genres':
                    if fData['yearsActive'] != jsonContent['yearsActive'] or sorted(fData['places']) != sorted(jsonContent['places']) or sorted(fData['artists']) != sorted(jsonContent['artists']) or sorted(fData['labels']) != sorted(jsonContent['labels']):
                        fData['yearsActive'] = jsonContent['yearsActive']
                        fData['places'] = jsonContent['places']
                        fData['artists'] = jsonContent['artists']
                        fData['labels'] = jsonContent['labels']
                        with open(filePath, 'w', encoding='utf-8') as file:
                            json.dump(fData, file, indent=2, ensure_ascii=False)
                elif type == 'labels':
                    if fData['yearsActive'] != jsonContent['yearsActive'] or sorted(fData['artists']) != sorted(jsonContent['artists']):
                        fData['yearsActive'] = jsonContent['yearsActive']
                        fData['artists'] = jsonContent['artists']
                        with open(filePath, 'w', encoding='utf-8') as file:
                            json.dump(fData, file, indent=2, ensure_ascii=False)



def generateOutputJSON(type, element, contributions):
    print(element)
    if type == 'artists':
        return generateArtistJSON(element, contributions)
    elif type == 'genres':
        return generateGenreJSON(element, contributions)
    else:
        return generateLabelJSON(element, contributions)


def generateArtistJSON(artist, contributions):
    labels = []
    genres = []
    artists = []
    start = 3000
    end = 1000
    lang = []
    realName = ''
    for album in contributions['albumArtist']:
        if album.compilation == '0':
            genres = genres + list(set(album.genres) - set(genres))
        if not album.label in labels:
            labels.append(album.label)
        if int(album.year) < int(start):
            start = album.year
        if int(album.year) > int(end):
            end = album.year
        if len(lang) == 0:
            lang = album.lang
        if not removeSpecialCharFromString(album.albumArtist) in artists:
            artists.append(removeSpecialCharFromString(album.albumArtist))
    for album in contributions['artist']:
        if album.compilation == '0':
            genres = genres + list(set(album.genres) - set(genres))
        if not album.label in labels:
            labels.append(album.label)
        if int(album.year) < int(start):
            start = album.year
        if int(album.year) > int(end):
            end = album.year
        if not removeSpecialCharFromString(album.albumArtist) in artists:
            artists.append(removeSpecialCharFromString(album.albumArtist))
    for album in contributions['performer']:
        if album.compilation == '0':
            genres = genres + list(set(album.genres) - set(genres))
        if not album.label in labels:
            labels.append(album.label)
        if int(album.year) < int(start):
            start = album.year
        if int(album.year) > int(end):
            end = album.year
        if not removeSpecialCharFromString(album.albumArtist) in artists:
            artists.append(removeSpecialCharFromString(album.albumArtist))
    for album in contributions['producer']:
        if album.compilation == '0':
            genres = genres + list(set(album.genres) - set(genres))
        if not album.label in labels:
            labels.append(album.label)
        if int(album.year) < int(start):
            start = album.year
        if int(album.year) > int(end):
            end = album.year
        if not removeSpecialCharFromString(album.albumArtist) in artists:
            artists.append(removeSpecialCharFromString(album.albumArtist))
    for album in contributions['composer']:
        if album.compilation == '0':
            genres = genres + list(set(album.genres) - set(genres))
        if not album.label in labels:
            labels.append(album.label)
        if int(album.year) < int(start):
            start = album.year
        if int(album.year) > int(end):
            end = album.year
        if not removeSpecialCharFromString(album.albumArtist) in artists:
            artists.append(removeSpecialCharFromString(album.albumArtist))
    if 'realName' in contributions and contributions['realName'] != None:
        realName = contributions['realName']
    output = {
        "type": "",
        "name": artist,
        "realName": realName,
        "alias": [],
        "originCountry": lang,
        "birth": "",
        "placeOfBirth": "",
        "countryOfBirth": "",
        "death": "",
        "placeOfDeath": "",
        "countryOfDeath": "",
        "yearsActive": "{}-{}".format(start, end),
        "members": [],
        "pastMembers": [],
        "links": [],
        "artists": artists,
        "genres": genres,
        "labels": labels,
        "bio": {
            "en": ""
        },
        "testimony": {
            "en": {
                "from": "",
                "text": ""
            }
        }
    }
    return output


def generateGenreJSON(genre, contributions):
    artists = []
    labels = []
    start = 3000
    end = 1000
    places = []
    for album in contributions:
        if not album.albumArtist in artists:
            artists.append(album.albumArtist)
        if not album.label in labels:
            labels.append(album.label)
        if int(album.year) < int(start):
            start = album.year
        if int(album.year) > int(end):
            end = album.year
        if album.lang not in places:
            places = places + list(set(album.lang) - set(places))
    output = {
        "name": genre,
        "alias": [],
        "start": "",
        "end": "",
        "originCountry": [],
        "places": places,
        "yearsActive": "{}-{}".format(start, end),
        "parent": "",
        "influences": [],
        "subgenres": [],
        "artists": artists,
        "labels": labels,
        "desc": {
            "en": ""
        }
    }
    return output


def generateLabelJSON(label, contributions):
    artists = []
    start = 3000
    end = 1000
    for album in contributions:
        if not album.albumArtist in artists:
            artists.append(album.albumArtist)
        if int(album.year) < int(start):
            start = album.year
        if int(album.year) > int(end):
            end = album.year
    output = {
        "name": label,
        "alias": [],
        "start": "",
        "end": "",
        "originCountry": [],
        "yearsActive": "{}-{}".format(start, end),
        "artists": artists,
        "desc": {
            "en": ""
        }
    }
    return output
