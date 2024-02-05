from data_analytics_app import app 
from flask import render_template,url_for,request,redirect,jsonify
import pandas as pd 
import json 
import os
import csv
from io import TextIOWrapper
from flask_sqlalchemy import SQLAlchemy
from io import StringIO
from sqlalchemy import inspect
from dotenv import load_dotenv
import os
from numpy import int64
import logging
from sqlalchemy import text
load_dotenv()

#database configuration 
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)
logging.basicConfig(filename='app.log',level=logging.DEBUG)

#Currently it Supports csv files
ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx', 'pdf'}


class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    data = db.Column(db.Text, nullable=False)

#it gives list of all files in the db
@app.route("/compute")
def compute():
    inspector=inspect(db.engine)
    table_names=inspector.get_table_names()
    app.logger.info(table_names)
    table_names = [table for table in table_names if table != 'dataset']
    return render_template("compute.html",title="uploadAsserts",datasets=table_names)


def get_integer_columns(table_name):
    app.logger.info(f"Getting number columns for table: {table_name}")
    inspector = db.inspect(db.engine)
    columns = inspector.get_columns(table_name)
    #log the columns to the give given table_name
    app.logger.info(columns)
    numeric_types = {'INT', 'BIGINT', 'SMALLINT', 'FLOAT', 'DOUBLE', 'NUMERIC','DOUBLE PRECISION'}

    number_columns = [column['name'] for column in columns if str(column['type']).upper() in numeric_types or 'NUMERIC' in str(column['type']).upper()]

    return number_columns

@app.route("/graph")
def graph():
    inspector=inspect(db.engine)
    table_names=inspector.get_table_names()
    table_names = [table for table in table_names if table != 'dataset']
    return render_template("visualization.html",title="graph",datasets=table_names)

#home page 
@app.route('/')
def home():
    return render_template('Home.html')


#compute for filtered integer columns
@app.route('/dataset/<string:tablename>/compute', methods=['GET'])
def compute_dataset(tablename):
    try:
        integer_columns= get_integer_columns(tablename)
        response_data = {'integer_columns': integer_columns}
        return jsonify(response_data)

    except Exception as e:
        # Log the error for debugging purposes
        print(f"An error occurred: {str(e)}")
        return jsonify({'error': 'An error occurred on the server'}), 500

# Get up to 30 columns from the db
@app.route('/dataset/<string:tablename>/plot', methods=['GET'])
def perform_plot(tablename):
    
    selected_column1 = request.args.get('selected_column1')
    selected_column2 = request.args.get('selected_column2')
    
    query_1 = text(f'SELECT "{selected_column1}" FROM "{tablename}" LIMIT 30')
    query_2 = text(f'SELECT "{selected_column2}" FROM "{tablename}" LIMIT 30')
    
    result_1 = db.session.execute(query_1).fetchall()
    result_2 = db.session.execute(query_2).fetchall()
    
    values_column1 = [row[0] for row in result_1]
    values_column2=[row[0] for row in result_2]
    
    response_data = {'values_column1': values_column1,'values_column2':values_column2,'selected_column1':selected_column1,'selected_column2':selected_column2}
    return jsonify(response_data)
    

#compute operations sum or min or max of selected column
@app.route('/dataset/<string:tablename>/compute', methods=['POST'])
def perform_compute(tablename):

    selected_column = request.form.get('selected_column')
    selected_operation = request.form.get('operation')
    
    if selected_operation == 'sum':
        query = text(f'SELECT SUM("{tablename}"."{selected_column}") FROM "{tablename}"')
        result = db.session.execute(query).scalar()
        
    elif selected_operation == 'min':
        query = text(f'SELECT MIN("{tablename}"."{selected_column}") FROM "{tablename}"')
        result = db.session.execute(query).scalar()
        
    elif selected_operation == 'max':
        query = text(f'SELECT MAX("{tablename}"."{selected_column}") FROM "{tablename}"')
        result = db.session.execute(query).scalar()
        
    else:
        result = None
   
    return {'result':result}
    

#upload the dataset to the database (postgres)
@app.route('/dataset', methods=['POST'])
def dataset():
    
    if 'file' not in request.files:
        return "No file provided"

    file = request.files['file']
    filename = request.form['filename']
    
    if filename == '':
        return "No file selected"
    
    if file:
        df=pd.read_csv(file)
        #log the data frame for debugging 
        app.logger.info(df)
       # If the table already exists, replace it with the new data
        df.to_sql(filename,con=db.engine,if_exists='replace',index=False)
        return redirect(url_for('compute'))
    
  
#app_context will handle to create db
app.app_context().push()
db.create_all()