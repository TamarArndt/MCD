import logging, sys
import subprocess, json
import configuration.configuration as conf

logger = logging.getLogger()

def getLabelConfidencesForStopId(stopId):
    DB_PATH, JAR_PATH, MODEL_PATH = conf.readValuesFromConfigFile()
    STOPID = str(stopId)

    try:
        response = subprocess.Popen(['java', '-jar', JAR_PATH, '-model', MODEL_PATH, '-stopid', STOPID, '-db',  DB_PATH], stdout=subprocess.PIPE)
        return json.loads(response.stdout.readlines()[1].decode("utf-8"))
    except:
        logger.error(" Error: {}".format(sys.exc_info()))
        return False
