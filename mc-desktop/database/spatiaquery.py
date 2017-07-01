import os, sys, subprocess, json

def spatiaQuery(query_string):
    ''' this calls the python2-script python2subprocess.py '''
    response = subprocess.run(['python', os.path.join(os.path.dirname(sys.modules['__main__'].__file__), './database/python2subprocess.py'), query_string, '/dev/null'], stdout=subprocess.PIPE)
    response_str = response.stdout[:-1].decode("utf-8");
    # make json object from string
    return json.loads(response_str)

