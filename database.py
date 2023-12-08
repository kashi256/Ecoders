import sqlite3
from flask import g

def connectToDatabase():
    sql = sqlite3.connect("H:/diabetic_prediction/diabetic_prediciton_app/diabetes.db")
    sql.row_factory = sqlite3.Row
    return sql

def getDatabase():
    if not hasattr(g, 'diabetes_db'):
        g.diabetes_db = connectToDatabase()
    return g.diabetes_db