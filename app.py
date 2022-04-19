from flask import Flask
from src import manager

app = Flask(__name__)
cdmx = manager.CDMX()


@app.route('/')
def hello_world():  # put application's code here
    return {
        'alcaldias': cdmx.get_alcadias_name(),
        'lineas': cdmx.get_lineas_full_name(),
    }


if __name__ == '__main__':
    app.run()
