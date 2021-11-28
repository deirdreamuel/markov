from flask import Flask
import logging

app = Flask(__name__)
logging.basicConfig(filename='debug.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s - thread %(threadName)s : %(message)s')