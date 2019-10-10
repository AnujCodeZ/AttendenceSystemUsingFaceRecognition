from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import face

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
df = pd.DataFrame()

from FlaskWeb import routes