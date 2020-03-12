# Python imports
import os
import json


class MetaAnalyzer:
    def __init__(self, files, path):
        self.files = files
        self.path = path
        self.dumps = []
        self.metaAnalyzis = {}
        self._extractInfoFromFiles()
        self._buildMetaAnalyzisData()


    # Extract information from each json file in order to process them later on
    def _extractInfoFromFiles(self):
        for index, fileName in enumerate(self.files):
            dump = {}
            with open(os.path.join(self.path, fileName)) as jsonFile:
                jsonText = json.load(jsonFile)
                dump['date'] = jsonText['date']
                dump['version'] = jsonText['version']
                dump['elapsedSeconds'] = jsonText['elapsedSeconds']
                dump['folderInfo'] = jsonText['folderInfo']
                jsonFile.close()
            self.dumps.append(dump)


    # We compare first dump with last to extract global variation of values
    def _buildMetaAnalyzisData(self):
        first = self.dumps[0]['folderInfo']
        last = self.dumps[len(self.dumps) - 1]['folderInfo']  
        self.metaAnalyzis['sizeDelta'] = last['size'] - first['size']
        self.metaAnalyzis['filesDelta'] = last['files'] - first['files']
        self.metaAnalyzis['foldersDelta'] = last['folders'] - first['folders']
        # File variation
        self.metaAnalyzis['flacDelta'] = last['flacCount'] - first['flacCount']
        self.metaAnalyzis['mp3Delta'] = last['mp3Count'] - first['mp3Count']
        self.metaAnalyzis['jpgDelta'] = last['jpgCount'] - first['jpgCount']
        self.metaAnalyzis['pngDelta'] = last['pngCount'] - first['pngCount']
        # Proportion variations
        self.metaAnalyzis['flacPercentageDelta'] = last['flacPercentage'] - first['flacPercentage']
        self.metaAnalyzis['mp3PercentageDelta'] = last['mp3Percentage'] - first['mp3Percentage']
        self.metaAnalyzis['jpgPercentageDelta'] = last['jpgPercentage'] - first['jpgPercentage']
        self.metaAnalyzis['pngPercentageDelta'] = last['pngPercentage'] - first['pngPercentage']        
        # Library variation
        self.metaAnalyzis['artistsDelta'] = last['artistsCount'] - first['artistsCount']
        self.metaAnalyzis['albumsDelta'] = last['albumsCount'] - first['albumsCount']
        self.metaAnalyzis['tracksDelta'] = last['tracksCount'] - first['tracksCount']
        self.metaAnalyzis['coversDelta'] = last['coversCount'] - first['coversCount']
        # Errors variation
        self.metaAnalyzis['errorsDelta'] = last['errorsCount'] - first['errorsCount']
        self.metaAnalyzis['possibleErrorsDelta'] = last['possibleErrors'] - first['possibleErrors']
        self.metaAnalyzis['purityDelta'] = last['purity'] - first['purity']
