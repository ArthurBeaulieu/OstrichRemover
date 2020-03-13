# Python imports
import os
import json


class MetaAnalyzer:
    def __init__(self, files, path):
        self.files = files
        self.path = path
        self.dumps = []
        self.metaAnalysis = {}
        self._extractInfoFromFiles()
        self._buildMetaAnalysisData()


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
    def _buildMetaAnalysisData(self):
        first = self.dumps[0]['folderInfo']
        last = self.dumps[len(self.dumps) - 1]['folderInfo']
        # Fill begin and end date range from dumps
        self.metaAnalysis['folderPath'] = self.path
        self.metaAnalysis['dateFrom'] = self.dumps[0]['date']
        self.metaAnalysis['dateTo'] = self.dumps[len(self.dumps) - 1]['date']
        self.metaAnalysis['sizeDelta'] = last['size'] - first['size']
        self.metaAnalysis['filesDelta'] = last['files'] - first['files']
        self.metaAnalysis['foldersDelta'] = last['folders'] - first['folders']
        # File variation
        self.metaAnalysis['flacDelta'] = last['flacCount'] - first['flacCount']
        self.metaAnalysis['mp3Delta'] = last['mp3Count'] - first['mp3Count']
        self.metaAnalysis['jpgDelta'] = last['jpgCount'] - first['jpgCount']
        self.metaAnalysis['pngDelta'] = last['pngCount'] - first['pngCount']
        # Proportion variations
        self.metaAnalysis['flacPercentageDelta'] = last['flacPercentage'] - first['flacPercentage']
        self.metaAnalysis['mp3PercentageDelta'] = last['mp3Percentage'] - first['mp3Percentage']
        self.metaAnalysis['jpgPercentageDelta'] = last['jpgPercentage'] - first['jpgPercentage']
        self.metaAnalysis['pngPercentageDelta'] = last['pngPercentage'] - first['pngPercentage']
        # Library variation
        self.metaAnalysis['artistsDelta'] = last['artistsCount'] - first['artistsCount']
        self.metaAnalysis['albumsDelta'] = last['albumsCount'] - first['albumsCount']
        self.metaAnalysis['tracksDelta'] = last['tracksCount'] - first['tracksCount']
        self.metaAnalysis['coversDelta'] = last['coversCount'] - first['coversCount']
        # Errors variation
        self.metaAnalysis['errorsDelta'] = last['errorsCount'] - first['errorsCount']
        self.metaAnalysis['possibleErrorsDelta'] = last['possibleErrors'] - first['possibleErrors']
        self.metaAnalysis['purityDelta'] = last['purity'] - first['purity']
