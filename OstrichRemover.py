#!/usr/bin/env python3


# Python imports
import os
import sys
import argparse
import time
import datetime
import re
# Project imports
from src.models.folderInfo import FolderInfo
from src.scan.albumTester import AlbumTester
from src.fill.albumFiller import AlbumFiller
from src.clean.albumCleaner import AlbumCleaner
from src.analyze.metaAnalyzer import MetaAnalyzer
from src.stat.statMaker import StatMaker
from src.utils.tools import computePurity
from src.utils.reportBuilder import *
from src.utils.uiBuilder import *
from src.utils.tools import *
# Globals
global scriptVersion
scriptVersion = '1.6.0'


# Script main frame
def main():
    # Init argparse arguments
    ap = argparse.ArgumentParser()
    ap.add_argument('folder', help='The input folder path to crawl (absolute or relative)')
    # Main modes
    ap.add_argument('-s', '--scan', help='Scan a folder to test it against naming convention', action='store_true')
    ap.add_argument('-f', '--fill', help='Prefill tags with folder name and file name information', action='store_true')
    ap.add_argument('-a', '--analyze', help='Analyze a folder of JSON dumps to make a meta analysis', action='store_true')
    ap.add_argument('-t', '--stat', help='Aggregates stats about a given library', action='store_true')
    ap.add_argument('-g', '--gen', help='Generates a JSON for each release artist', action='store_true')
    # Additional modes
    ap.add_argument('-c', '--clean', help='Clean all previously set tags, and ambiguous ones', action='store_true')
    # Arguments
    ap.add_argument('-d', '--dump', help='Dump JSON in ./dump folder by default, see -p for custom output folder', action='store_true')
    ap.add_argument('-m', '--minify', help='Minify the JSON output', action='store_true')
    ap.add_argument('-e', '--errors', help='Log errors only during run', action='store_true')
    ap.add_argument('-v', '--verbose', help='Log detailed progress when running', action='store_true')
    ap.add_argument('-p', '--path', help='The output path to store the dumped JSON', type=os.path.abspath)
    args = vars(ap.parse_args())
    # Preventing path from missing its trailing slash (or backslash for win compatibility)
    if not args['folder'].endswith('\\') and not args['folder'].endswith('/'):
        printInvalidPath(args['folder'])
        sys.exit(-1)
    # Exec script
    printCredentials(scriptVersion)
    # Perform a scan for the given folder against the naming convention
    if args['scan']:
        scanFolder(args)
    # Pre-fill folder's track tags with information held in folder name and file name
    elif args['fill']:
        fillTags(args)
    # Make a meta analysis of previously made scan to compile values
    elif args['analyze']:
        metaAnalysis(args)
    # Make a meta analysis of previously made scan to compile values
    elif args['stat']:
        extractStats(args)
    # Create a JSON file for all release artists and genre founds
    elif args['gen']:
        generateJSON(args)
    # Clean all previously set tags (to prepare a track to be properly filled)
    elif args['clean']:
        if queryYesNo('> Warning, this command will erase any previously existing tags on audio files in this path. Just do it?', 'yes'):
            printLineBreak()
            cleanTags(args)
    # Otherwise print an error message (missing arguments)
    else:
        printMissingArguments()
    # Clean the tmp.jpg image that could resides from fill or scan
    if os.path.exists('tmp.jpg'):
        os.remove('tmp.jpg') # GC


# Will crawl the folder path given in argument, and all its sub-directories
def scanFolder(args):
    # Retrieve folder global information
    printRetrieveFolderInfo()
    folderInfo = FolderInfo(args['folder'])
    printRootFolderInfo(folderInfo)
    # Scan internals
    totalTracks = folderInfo.flacCounter + folderInfo.mp3Counter
    rootPathLength = len(args['folder'].split(os.sep))
    scannedTracks = 0
    errorCounter = 0
    albumTesters = []
    # Scan progression utils
    step = 10
    percentage = step
    previousLetter = '1' # Ordered folder/file parsing begins with numbers
    # Start scan
    printScanStart(args['folder'], totalTracks, len(ErrorEnum))
    startTime = time.time()
    # Sort directories so they are handled in the alphabetical order
    for root, directories, files in sorted(os.walk(args['folder'])):
        files = [f for f in files if not f[0] == '.'] # Ignore hidden files
        directories[:] = [d for d in directories if not d[0] == '.'] # ignore hidden directories
        # Split root into an array of folders
        path = root.split(os.sep)
        # Mutagen needs a preserved path when using ID3() or FLAC()
        preservedPath = list(path)
        # Poping all path element that are not the root folder, the artist sub folder or the album sub sub folder
        for x in range(rootPathLength - 1):
            path.pop(0)
        # Current path is for an album directory : perform tests
        if len(path) == 2 and path[1] != '':
            albumTester = AlbumTester(files, preservedPath)
            scannedTracks += albumTester.album.totalTrack
            errorCounter += albumTester.tracksErrorCounter()
            errorCounter += albumTester.errorCounter
            albumTesters.append(albumTester)
            # Display a progress every step %
            scannedPercentage = (scannedTracks * 100) / totalTracks
            if totalTracks > 10 and scannedPercentage >= step and scannedTracks < totalTracks:
                if (scannedTracks * 100) / totalTracks > percentage and percentage < 100:
                    printScanProgress(percentage, previousLetter, path[0][0], errorCounter, scannedTracks,
                                      computePurity(errorCounter, scannedTracks))
                    percentage += step
                    previousLetter = path[0][0]  # path[0] is the Artists name
    # In this case, ui has display a percentage progression. No need to add a line break if no progression is to be displayed
    if totalTracks > 10 and percentage != 10:
        printLineBreak()
    duration = round(time.time() - startTime, 2)
    printScanEnd(duration, errorCounter, totalTracks, computePurity(errorCounter, scannedTracks))
    # Compute and save JSON report
    if args['dump']:
        saveReportFile(computeFillReport(scriptVersion, duration, folderInfo, albumTesters, errorCounter,
                                     computePurity(errorCounter, scannedTracks)), 'Errors', args['minify'], args['path'])
    # Verbose report
    if args['verbose']:
        printErroredTracksReport(albumTesters)


# Will pre-fill the tags for tracks in the given folder
def fillTags(args):
    # Retrieve folder global information
    printRetrieveFolderInfo()
    folderInfo = FolderInfo(args['folder'])
    printRootFolderInfo(folderInfo)
    # Fill internals
    filledTracks = 0
    totalTracks = folderInfo.flacCounter + folderInfo.mp3Counter
    # Start Fill
    printFillStart(args['folder'], totalTracks)
    rootPathLength = len(args['folder'].split(os.sep))
    albumFillers = []
    # Fill progression utils
    step = 10
    percentage = step
    startTime = time.time()
    # Sort directories so they are handled in the alphabetical order
    for root, directories, files in sorted(os.walk(args['folder'])):
        files = [f for f in files if not f[0] == '.'] # Ignore hidden files
        directories[:] = [d for d in directories if not d[0] == '.'] # ignore hidden directories
        # Split root into an array of folders
        path = root.split(os.sep)
        # Mutagen needs a preserved path when using ID3() or FLAC()
        preservedPath = list(path)
        # Poping all path element that are not the root folder, the artist sub folder or the album sub sub folder
        for x in range(rootPathLength - 1):
            path.pop(0)
        # Current path is for an album directory : perform tests
        if len(path) == 2 and path[1] != '':
            albumFiller = AlbumFiller(files, preservedPath, args['verbose'], args['errors'])
            albumFillers.append(albumFiller)
            if albumFiller.hasErrors is False:
                filledTracks += albumFiller.album.totalTrack
        # Display a progress every step %
        fillPercentage = (filledTracks * 100) / totalTracks
        if totalTracks > 10 and fillPercentage >= step and filledTracks < totalTracks:
            if (filledTracks * 100) / totalTracks > percentage and percentage < 100:
                printFillProgress(percentage, filledTracks)
                percentage += step
    # Couldn't fill all track because of naming error
    if totalTracks is not filledTracks:
        printInvalidFolderStructure(filledTracks, totalTracks, 'fill')
    # In this case, ui has display a percentage progression. No need to add a line break if no progression is to be displayed
    if totalTracks > 10 and percentage != 10: # If more than 10 tracks and percentage have been displayed (if % = 10, it is its init value)
        printLineBreak()
    duration = round(time.time() - startTime, 2)
    printFillEnd(duration, filledTracks)


# Will make a JSON file with compiled results from input path that contains JSON dumps (from --dump)
def metaAnalysis(args):
    # Get JSON files in arg folder
    jsonFiles = [ file for file in os.listdir(args['folder']) if file.endswith('.json') ]
    # Start analyze
    printAnalyzeStart(args['folder'], len(jsonFiles))
    startTime = time.time()
    # Generate MetaAnalyzer object from this JSON list
    metaAnalyzer = MetaAnalyzer(sorted(jsonFiles), args['folder'])
    printAnalyzeStatus(metaAnalyzer)
    duration = round(time.time() - startTime, 2)
    printAnalyzeEnd(duration, len(jsonFiles))
    # Compute and save JSON report
    if args['dump']:
        saveReportFile(computeMetaAnalyzeReport(scriptVersion, duration, metaAnalyzer), 'Meta-Analyze', args['minify'], args['path'])


# This method will crawl an audio library and save all its main information (labels, artists, genres)
def extractStats(args):
    # Retrieve folder global information
    printRetrieveFolderInfo()
    folderInfo = FolderInfo(args['folder'])
    printRootFolderInfo(folderInfo)
    # Stat internals
    artists = []
    genres = []
    labels = []
    analyzedTracks = 0
    totalTracks = folderInfo.flacCounter + folderInfo.mp3Counter
    # Analyze progression utils
    printStatStart(args['folder'], totalTracks)
    step = 10
    percentage = step
    startTime = time.time()
    # Sort directories so they are handled in the alphabetical order
    for root, directories, files in sorted(os.walk(args['folder'])):
        files = [f for f in files if not f[0] == '.'] # Ignore hidden files
        directories[:] = [d for d in directories if not d[0] == '.'] # ignore hidden directories
        # Split root into an array of folders
        path = root.split(os.sep)
        # Mutagen needs a preserved path when using ID3() or FLAC()
        preservedPath = list(path)
        rootPathLength = len(args['folder'].split(os.sep))
        # Poping all path element that are not the root folder, the artist sub folder or the album sub sub folder
        for x in range(rootPathLength - 1):
            path.pop(0)
        # Current path is for an album directory : perform tests
        if len(path) == 2 and path[1] != '':
            albumStats = StatMaker(files, preservedPath)
            artists = insertArtistInListIfNotExisting(artists, albumStats.artistsDetails)
            genres = insertInListIfNotExisting(genres, albumStats.genres)
            labels = insertInListIfNotExisting(labels, albumStats.labels)
            analyzedTracks += len(albumStats.tracks)
        # Display a progress every step %
        fillPercentage = (analyzedTracks * 100) / totalTracks
        if totalTracks > 10 and fillPercentage >= step and analyzedTracks < totalTracks:
            if (analyzedTracks * 100) / totalTracks > percentage and percentage < 100:
                printStatProgress(percentage, analyzedTracks)
                percentage += step
    # In this case, ui has display a percentage progression. No need to add a line break if no progression is to be displayed
    if totalTracks > 10 and percentage != 10:
        printLineBreak()
    duration = round(time.time() - startTime, 2)
    printStatEnd(duration, analyzedTracks)
    # Compute and save JSON report
    if args['dump']:
        saveReportFile(computeStatReport(scriptVersion, duration, artists, genres, labels, folderInfo.folder), 'Stats', args['minify'], args['path'])
    else:
        print(artists)
        print(genres)
        print(labels)


# Thuis method will crawl the audio library and generate for each unique artist and genre a JSON file for ManaZeak assets
def generateJSON(args):
    # Retrieve folder global information
    printRetrieveFolderInfo()
    folderInfo = FolderInfo(args['folder'])
    printRootFolderInfo(folderInfo)
    # Scan internals
    totalTracks = folderInfo.flacCounter + folderInfo.mp3Counter
    rootPathLength = len(args['folder'].split(os.sep))
    parsedTracks = 0
    errorCounter = 0
    albumTesters = []

    artists = []
    artistsAlbums = {}
    genres = []
    genresAlbums = {}
    labels = []
    labelsAlbums = {}
    # Scan progression utils
    step = 10
    percentage = step
    previousLetter = '1' # Ordered folder/file parsing begins with numbers
    # Start scan
    printGenerationStart(totalTracks, args['path'])
    startTime = time.time()
    # Sort directories so they are handled in the alphabetical order
    for root, directories, files in sorted(os.walk(args['folder'])):
        files = [f for f in files if not f[0] == '.'] # Ignore hidden files
        directories[:] = [d for d in directories if not d[0] == '.'] # ignore hidden directories
        # Split root into an array of folders
        path = root.split(os.sep)
        # Mutagen needs a preserved path when using ID3() or FLAC()
        preservedPath = list(path)
        # Poping all path element that are not the root folder, the artist sub folder or the album sub sub folder
        for x in range(rootPathLength - 1):
            path.pop(0)
        # Current path is for an album directory : perform tests
        if len(path) == 2 and path[1] != '':
            albumTester = AlbumTester(files, preservedPath)
            parsedTracks += albumTester.album.totalTrack
            # Artists section
            # Append release artist if not already added
            if not albumTester.album.albumArtist in artists:
                artists.append(removeSpecialCharFromString(albumTester.album.albumArtist))
            if not albumTester.album.albumArtist in artistsAlbums:
                artistsAlbums[removeSpecialCharFromString(albumTester.album.albumArtist)] = {
                    'albumArtist': [albumTester.album],
                    'artist': [],
                    'performer': [],
                    'producer': [],
                    'composer': []
                }
            else:
                artistsAlbums[removeSpecialCharFromString(albumTester.album.albumArtist)]['albumArtist'].append(albumTester.album)
            # Label filling
            if not albumTester.album.label in labels:
                labels.append(removeSpecialCharFromString(albumTester.album.label))
            if not albumTester.album.label in labelsAlbums:
                labelsAlbums[removeSpecialCharFromString(albumTester.album.label)] = [albumTester.album]
            else:
                labelsAlbums[removeSpecialCharFromString(albumTester.album.label)].append(albumTester.album)
            # Iterate over tracks now
            for track in albumTester.tracks:
                for artist in track.track.artists:
                    if not artist in artists:
                        artists.append(removeSpecialCharFromString(artist))
                    if not artist in artistsAlbums:
                        artistsAlbums[removeSpecialCharFromString(artist)] = {
                            'albumArtist': [],
                            'artist': [albumTester.album],
                            'performer': [],
                            'producer': [],
                            'composer': []
                        }
                    else:
                        artistsAlbums[removeSpecialCharFromString(artist)]['artist'].append(albumTester.album)
                for performer in track.track.performers:
                    if not performer in artists:
                        artists.append(removeSpecialCharFromString(performer))
                    if not performer in artistsAlbums:
                        artistsAlbums[removeSpecialCharFromString(performer)] = {
                            'albumArtist': [],
                            'artist': [],
                            'performer': [albumTester.album],
                            'producer': [],
                            'composer': []
                        }
                    else:
                        artistsAlbums[removeSpecialCharFromString(performer)]['performer'].append(albumTester.album)
                for producer in track.track.producers:
                    if not producer in artists:
                        artists.append(removeSpecialCharFromString(producer))
                    if not producer in artistsAlbums:
                        artistsAlbums[removeSpecialCharFromString(producer)] = {
                            'albumArtist': [],
                            'artist': [],
                            'performer': [],
                            'producer': [albumTester.album],
                            'composer': []
                        }
                    else:
                        artistsAlbums[removeSpecialCharFromString(producer)]['producer'].append(albumTester.album)
                for composer in track.track.composers:
                    c = re.sub(r' \([^()]*\)', '', composer)
                    realName = re.search(r'\((.*?)\)', composer)
                    if not c in artists:
                        artists.append(removeSpecialCharFromString(c))
                    if not c in artistsAlbums:
                        artistsAlbums[removeSpecialCharFromString(c)] = {
                            'albumArtist': [],
                            'artist': [],
                            'performer': [],
                            'producer': [],
                            'composer': [albumTester.album]
                        }
                    else:
                        artistsAlbums[removeSpecialCharFromString(c)]['composer'].append(albumTester.album)
                    if realName != None and realName.group(1).find(',') == -1:
                        artistsAlbums[removeSpecialCharFromString(c)]['realName'] = removeSpecialCharFromString(realName.group(1))
                # Updating genre
                for genre in track.track.genres:
                    if not genre in genres:
                        genres.append(genre)
                    if not genre in genresAlbums:
                        genresAlbums[genre] = [albumTester.album]
                    else:
                        genresAlbums[genre].append(albumTester.album)
            # Display a progress every step %
            scannedPercentage = (parsedTracks * 100) / totalTracks
            if totalTracks > 10 and scannedPercentage >= step and parsedTracks < totalTracks:
                if (parsedTracks * 100) / totalTracks > percentage and percentage < 100:
                    printGenerationProgress(percentage, parsedTracks)
                    percentage += step
    # In this case, ui has display a percentage progression. No need to add a line break if no progression is to be displayed
    if totalTracks > 10 and percentage != 10:
        printLineBreak()
    duration = round(time.time() - startTime, 2)
    printGenerationEnd(duration, len(artists), len(genres))
    # Compute and save JSON report
    if args['path']:
        saveGeneratedJSONFile(artists, artistsAlbums, 'artists', args['path'])
        saveGeneratedJSONFile(genres, genresAlbums, 'genres', args['path'])
        saveGeneratedJSONFile(labels, labelsAlbums, 'labels', args['path'])
    # Perform cleaning on files (remove all not in lists)
    for filename in os.listdir(args['path'] + '/artists/txt'):
        if filename[:-5] not in artists:
            os.remove(args['path'] + '/artists/txt/' + filename)
    for filename in os.listdir(args['path'] + '/genres/txt'):
        if filename[:-5] not in genres:
            os.remove(args['path'] + '/genres/txt/' + filename)
    for filename in os.listdir(args['path'] + '/labels/txt'):
        if filename[:-5] not in labels:
            os.remove(args['path'] + '/labels/txt/' + filename)
    # Verbose report
    if args['verbose']:
        printErroredTracksReport(albumTesters)


# This method will clear ever tags in audio files for the scanned folder
def cleanTags(args):
    # Retrieve folder global information
    printRetrieveFolderInfo()
    folderInfo = FolderInfo(args['folder'])
    printRootFolderInfo(folderInfo)
    # Fill internals
    cleanedTracks = 0
    totalTracks = folderInfo.flacCounter + folderInfo.mp3Counter
    # Start Fill
    printCleanStart(args['folder'], totalTracks)
    rootPathLength = len(args['folder'].split(os.sep))
    albumCleaners = []
    # Fill progression utils
    step = 10
    percentage = step
    startTime = time.time()
    # Sort directories so they are handled in the alphabetical order
    for root, directories, files in sorted(os.walk(args['folder'])):
        files = [f for f in files if not f[0] == '.'] # Ignore hidden files
        directories[:] = [d for d in directories if not d[0] == '.'] # ignore hidden directories
        # Split root into an array of folders
        path = root.split(os.sep)
        # Mutagen needs a preserved path when using ID3() or FLAC()
        preservedPath = list(path)
        # Poping all path element that are not the root folder, the artist sub folder or the album sub sub folder
        for x in range(rootPathLength - 1):
            path.pop(0)
        # Current path is for an album directory : perform tests
        if len(path) == 2 and path[1] != '':
            albumCleaner = AlbumCleaner(files, preservedPath)
            albumCleaners.append(albumCleaner)
            cleanedTracks += albumCleaner.album.totalTrack
        # Display a progress every step %
        cleanPercentage = (cleanedTracks * 100) / totalTracks
        if totalTracks > 10 and cleanPercentage >= step:
            if (cleanedTracks * 100) / totalTracks > percentage and percentage < 100:
                printCleanProgress(percentage, cleanedTracks)
                percentage += step
    # In this case, ui has display a percentage progression. No need to add a line break if no progression is to be displayed
    if totalTracks > 10:
        printLineBreak()
    duration = round(time.time() - startTime, 2)
    printCleanEnd(duration, cleanedTracks)


# Script start point
if __name__ == '__main__':
    main()
