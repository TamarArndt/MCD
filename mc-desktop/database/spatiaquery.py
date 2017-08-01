import os, subprocess, json
import configuration.configuration as conf
from helper.filehelper import FileHelper


def spatiaQuery(query_string):
    """ this calls the python2-script python2subprocess.py """
    DB_PATH, JAR_PATH, MODEL_PATH = conf.readValuesFromConfigFile()
    response = subprocess.run(['python',
                               os.path.join(FileHelper().get_project_cwd(), 'database', 'python2subprocess.py'),
                               query_string,
                               DB_PATH,
                               'True'],
                               stdout=subprocess.PIPE)
    response_str = response.stdout[:-1].decode("utf-8");
    # make json object from string
    return json.loads(response_str)


def spatiaUpdate(query_string):
    """ this calls the python2-script python2subprocess.py """
    DB_PATH, JAR_PATH, MODEL_PATH = conf.readValuesFromConfigFile()
    subprocess.run(['python',
                    os.path.join(FileHelper().get_project_cwd(), 'database', 'python2subprocess.py'),
                    query_string,
                    DB_PATH,
                    'False'])
    return True
