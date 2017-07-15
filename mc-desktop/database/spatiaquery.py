import os, sys, subprocess, json
import configuration.configuration as conf


def spatiaQuery(query_string):
    """ this calls the python2-script python2subprocess.py """
    DB_PATH, JAR_PATH, MODEL_PATH = conf.readValuesFromConfigFile()
    response = subprocess.run(['python',
                               os.path.join(os.path.dirname(sys.modules['__main__'].__file__), './database/python2subprocess.py'),
                               query_string,
                               DB_PATH,
                               'True',
                               '/dev/null'],
                              stdout=subprocess.PIPE)
    response_str = response.stdout[:-1].decode("utf-8");
    # make json object from string
    return json.loads(response_str)


def spatiaUpdate(query_string):
    """ this calls the python2-script python2subprocess.py """
    DB_PATH, JAR_PATH, MODEL_PATH = conf.readValuesFromConfigFile()
    subprocess.run(['python',
                    os.path.join(os.path.dirname(sys.modules['__main__'].__file__), './database/python2subprocess.py'),
                    query_string,
                    DB_PATH,
                    'False',
                    '/dev/null'])
    return True
