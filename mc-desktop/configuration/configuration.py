import sys
import os
import configparser
from helper.filehelper import FileHelper


def accessConfig():
    configDirPath = getConfigDirPathForPlatform()

    if not os.path.exists(configDirPath):
        os.makedirs(configDirPath)

    try:
        dbPath, jarPath, modelPath = readValuesFromConfigFile()

    except KeyError:
        # create configuration.ini with default values
        myConfigParser = configparser.ConfigParser()
        PROJECT_DIR = FileHelper().get_project_cwd()
        myConfigParser['paths'] = {'dbpath': os.path.join(PROJECT_DIR, 'assets', 'database', 'data.db'),
                                   'jarpath': os.path.join(PROJECT_DIR, 'assets', 'spl-wrapper', 'semanticlabler-1.0-SNAPSHOT-jar-with-dependencies.jar'),
                                   'modelpath': os.path.join(PROJECT_DIR, 'assets', 'spl-wrapper', 'random_comittee.model')}

        with open(os.path.join(configDirPath, 'configuration.ini'), 'w') as configfile:
            myConfigParser.write(configfile)

        dbPath, jarPath, modelPath = readValuesFromConfigFile()

    return dbPath, jarPath, modelPath


def readValuesFromConfigFile():
    configFilePath = os.path.join(getConfigDirPathForPlatform(), 'configuration.ini')
    myConfigParser = configparser.ConfigParser()
    myConfigParser.read(configFilePath)
    paths = myConfigParser['paths']
    dbPath = paths['dbpath']
    jarPath = paths['jarpath']
    modelPath = paths['modelpath']

    return dbPath, jarPath, modelPath


def getConfigDirPathForPlatform():
    home = os.path.expanduser("~")
    if sys.platform == "linux":
        return os.path.join(home, '.local', 'share', 'MobilityCompanionDesktop')
    if sys.platform == "win32" or sys.platform == "cygwin":
        return os.path.join(home, 'AppData', 'Local', 'MobilityCompanionDesktop')
    if sys.platform == "darwin":
        return os.path.join(home, 'Library', 'MobilityCompanionDesktop')


def updateGivenPathsInConfigFile(newPaths):
    configFilePath = os.path.join(getConfigDirPathForPlatform(), 'configuration.ini')
    myConfigParser = configparser.ConfigParser()
    myConfigParser.read(configFilePath)

    for path in newPaths:
        if path.endswith('.db'):
            myConfigParser.set('paths', 'dbpath', path)
        elif path.endswith('.jar'):
            myConfigParser.set('paths', 'jarpath', path)
        elif path.endswith('.model'):
            myConfigParser.set('paths', 'modelpath', path)

    with open(configFilePath, 'w') as configfile:
        myConfigParser.write(configfile)
