from flask import Flask, request
from os import environ
from manager import CDMX

app = Flask(__name__)
cdmx = CDMX()


@app.route('/alcaldias', methods=['GET'])
def alcaldias_info():
    return cdmx.get_alcaldias_info(request.args)


@app.route('/metrobus', methods=['GET'])
def metrobus_info():
    return cdmx.get_lineas_info(request.args)


if __name__ == '__main__':
    _debug = environ.get('FLASK_ENV') in ['dev', 'development']
    app.run(debug=_debug, host='0.0.0.0')

