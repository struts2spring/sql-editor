'''
Created on 21-Jan-2019

@author: vijay
'''

from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


def startHelpWeb():
    app.run(debug='DEBUG', host='localhost', port=5000)


if __name__ == '__main__':
    startHelpWeb()
