import os, sys


locationMarkerPath = os.path.join('res', 'location_marker.svg')
locationSplitMarkerPath = os.path.join('res', 'location_marker_split.svg')  # TODO absolute path?
dropDownArrowPath = os.path.join('res', 'ei-chevron-down.svg')


replacements = {
    'primaryColor': '#2196F3',
    'primaryDarkColor': '#1976D2',
    'accentYellowColor': '#FBC02D',
    'accentYellowDarkColor': '#ffb600',
    'accentGreenColor': '#008000',
    'confirmedColor': '#8CCF76',  #?
    'notconfirmedColor': '#E04848', #?
    'errorColor': '#ae2323',
    'notificationNoDetectionColor': '#A6A6A6',
    'notificationFullyLabeledColor': '#7ECC92',
    'notificationPartiallyLabeledColor': '#96B4D6',
    'grayLightColor': '#e6e6e6',
    'grayMediumColor': '#d3d3d3',
    'grayDarkColor': '#808080',

    'locationMarkerPath': str(locationMarkerPath),
    'locationSplitMarkerPath': str(locationSplitMarkerPath),
    'dropDownArrowPath': str(dropDownArrowPath)
}


def preprocessStylesheet(stylesheetFilename):
    """ create a processed stylesheet file where variable names are replaces by their values """
    MAIN_DIR = os.path.dirname(sys.modules['__main__'].__file__)  # TODO MAIN_DIR replace
    processedfilePath = os.path.join(MAIN_DIR, 'gui', 'style', ('processed' + stylesheetFilename))

    # TODO if it takes too much time, check if processed file already exists and already do replacement if not
    with open(os.path.join(MAIN_DIR, 'gui', 'style', stylesheetFilename)) as originalfile,\
            open(processedfilePath, 'w') as processedfile:
        for line in originalfile:
            for src, target in replacements.items():
                line = line.replace(src, target)
            processedfile.write(line)

    return processedfilePath

    # set main stylesheet
    # TODO check if this prohibits style polish and update
    # with open(os.path.join(MAIN_DIR , 'gui', 'style', ('processed' + stylesheetfile)), 'r', encoding='utf-8') as file:
    #     stylesheet = file.read()
    #     element.setStyleSheet(stylesheet)


