import os
from helper.filehelper import FileHelper


class StylesheetParser:
    def __init__(self):
        PROJECT_DIR = FileHelper().get_project_cwd()

        locationMarkerPath = os.path.join(PROJECT_DIR, 'res', 'location_marker.svg')
        locationSplitMarkerPath = os.path.join(PROJECT_DIR, 'res', 'location_marker_split.svg')
        dropDownArrowPath = os.path.join(PROJECT_DIR, 'res', 'ei-chevron-down.svg')

        self.replacements = {
            'primaryColor': '#87A6C9',
            'primaryDarkColor': '#507EB1',
            'selectionColor': '#96D4A1', #96D4A1
            'confirmedColor': '#C7C7C7',
            'notConfirmedColor': '#6192C9',
            'errorColor': '#ae2323',

            'notificationNoDetectionColor': '#A6A6A6',
            'notificationFullyLabeledColor': '#66C978',
            'notificationPartiallyLabeledColor': '#FFCB3B',

            'grayLightColor': '#e6e6e6',
            'grayMediumColor': '#d3d3d3',
            'grayDarkColor': '#808080',

            'locationMarkerPath': str(locationMarkerPath),
            'locationSplitMarkerPath': str(locationSplitMarkerPath),
            'dropDownArrowPath': str(dropDownArrowPath)
        }

    def preprocessStylesheet(self, stylesheetFilename):
        """ preprocess stylesheet file by replacing variables by their values as definied in replacements{}
        :return: path to processed stylesheet
        :rtype: str
        """
        PROJECT_DIR = FileHelper().get_project_cwd()
        processedfilePath = os.path.join(PROJECT_DIR, 'gui', 'style', ('processed' + stylesheetFilename))

        with open(os.path.join(PROJECT_DIR, 'gui', 'style', stylesheetFilename)) as originalfile,\
                open(processedfilePath, 'w') as processedfile:
            for line in originalfile:
                for src, target in self.replacements.items():
                    line = line.replace(src, target)
                processedfile.write(line)

        return processedfilePath


    def setProcessedStyleSheet(self, stylesheetFilename, element):
        """ sets the preprocessed version of the given stylesheet as the elements stylesheet """
        PROJECT_DIR = FileHelper().get_project_cwd()
        processedfilePath = self.preprocessStylesheet(stylesheetFilename)

        with open(os.path.join(PROJECT_DIR, 'gui', 'style', processedfilePath), 'r', encoding='utf-8') as file:
            stylesheet = file.read()
            element.setStyleSheet(stylesheet)

        return True





