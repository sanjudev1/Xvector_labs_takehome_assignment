from data_analytics_app import app 
from flask import render_template,url_for,request,redirect,jsonify
import pandas as pd 
import json 
import  plotly 
import plotly.express as px 
import os
import csv
from io import TextIOWrapper
from flask_sqlalchemy import SQLAlchemy
from io import StringIO
from dotenv import load_dotenv
import os
from numpy import int64

load_dotenv()

#database configuration 
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

#Currently it Supports csv files
ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx', 'pdf'}


class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    data = db.Column(db.Text, nullable=False)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#it gives list of all files in the db
@app.route("/compute")
def compute():
    datasets = Dataset.query.all()
    #serve the db data to the home page
    return render_template("compute.html",title="uploadAsserts",datasets=datasets)

@app.route("/graph")
def graph():
    datasets = Dataset.query.all()
    #serve the db data to the home page
    return render_template("visualization.html",title="graph",datasets=datasets)
#home page 
@app.route('/')
def home():
    return render_template('Home.html')

#check the delimiters for edge cases
def read_dataframe_from_dataset(selected_dataset):
    # Define a list of potential delimiters to try
    potential_delimiters = [',',';','/']  # Add more delimiters if needed

    for delimiter in potential_delimiters:
        try:
            # Attempt to read the DataFrame using the current delimiter
            df = pd.read_csv(StringIO(selected_dataset.data), delimiter=delimiter)
            if(len(list(df.columns))>2):
                return df  # Return the DataFrame if successful
        except pd.errors.ParserError:
            # If reading fails with the current delimiter, try the next one
            continue

    # If none of the delimiters work, handle the error or return an indication of failure
    raise ValueError("Unable to determine the delimiter for the dataset")


#compute for filtered integer columns

@app.route('/dataset/<int:id>/compute', methods=['GET'])
def compute_dataset(id):
    try:
        # Fetch the dataset from the database using the provided id
        selected_dataset = Dataset.query.get_or_404(id)

        # Convert the CSV data string to a DataFrame
        df = read_dataframe_from_dataset(selected_dataset)
        integer_columns = df.select_dtypes(include='number').columns

        # Check if the request is an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # If it's an AJAX request, return JSON
            response_data = {'integer_columns': list(integer_columns)}
            print('Response Data:', response_data)  # Add this line for debugging
            return jsonify(response_data)
        else:
            # If it's not an AJAX request, render the template
            column_names = list(df.columns)
            return render_template('compute_visualize.html', dataset=selected_dataset, column_names=integer_columns)
    except Exception as e:
        # Log the error for debugging purposes
        print(f"An error occurred: {str(e)}")
        return jsonify({'error': 'An error occurred on the server'}), 500

# Get up to 30 columns from the db
@app.route('/dataset/<int:id>/plot', methods=['GET'])
def perform_plot(id):
      # Fetch the dataset from the database using the provided id
    selected_dataset = Dataset.query.get_or_404(id)

    # Convert the CSV data string to a DataFrame using semicolon as the delimiter
    df = read_dataframe_from_dataset(selected_dataset)
    column_names = list(df.columns)
    integer_columns = df.select_dtypes(include='number').columns
    # Get the selected column and operation from the form submission
    selected_column1 = request.args.get('selected_column1')
    selected_column2 = request.args.get('selected_column2')
    values_column1 = df[selected_column1].head(30).tolist()
    values_column2 = df[selected_column2].head(30).tolist()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # If it's an AJAX request, return JSON
            response_data = {'values_column1': values_column1,'values_column2':values_column2,'selected_column1':selected_column1,'selected_column2':selected_column2}
            return jsonify(response_data)
    # Perform the operation based on user input
    
    return render_template('compute_visualize.html', dataset=selected_dataset, values_column1=values_column1,values_column2=values_column2,column_names=integer_columns,selected_column1=selected_column1,selected_column2=selected_column2)

#compute operations sum or min or max of selected column
@app.route('/dataset/<int:id>/compute', methods=['POST'])
def perform_compute(id):
    # Fetch the dataset from the database using the provided id
    selected_dataset = Dataset.query.get_or_404(id)

    # Convert the CSV data string to a DataFrame using semicolon as the delimiter
    df =  read_dataframe_from_dataset(selected_dataset)

    # Get the selected column and operation from the form submission
    selected_column = request.form.get('selected_column')
    selected_operation = request.form.get('operation')
    column_names = list(df.columns)
    integer_columns = df.select_dtypes(include='number').columns

    # Perform the operation based on user input
    
    if selected_operation == 'sum':
        result = df[selected_column].sum()
    elif selected_operation == 'min':
        result = df[selected_column].min()
    elif selected_operation == 'max':
        result = df[selected_column].max()
    else:
        result = None  # Handle invalid operation gracefully
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if isinstance(result, int64):
            # Convert numpy int64 to Python int
            result = int(result)
        return jsonify({'result': result})
    
    return render_template('compute_visualize.html', dataset=selected_dataset, column_name=selected_column, operation=selected_operation, result=result,column_names=integer_columns)

#upload the dataset to the database (postgres)
@app.route('/dataset', methods=['POST'])
def dataset():
    if 'file' not in request.files:
        return "No file provided"

    file = request.files['file']
    
    if file.filename == '':
        return "No file selected"
    filename = request.form['filename']
    save_uploaded_file(file, filename)
    return redirect(url_for('compute'))
      
def read_csv(csv_file):
    # Wrap the file in TextIOWrapper to ensure it's opened in text mode
    csv_file_wrapper = TextIOWrapper(csv_file, encoding='utf-8')
    csv_reader = csv.DictReader(csv_file_wrapper, delimiter=';')
    data = [row for row in csv_reader]
    return data

# Helper functions
def save_uploaded_file(file, filename):
    try:
        # Check if the filename already exists in the database
        existing_dataset = Dataset.query.filter_by(name=filename).first()

        if existing_dataset:
            return "File with the same name already exists. Choose a different filename."

        # If the filename is unique, proceed with saving the file
        csv_data = file.read().decode('utf-8')
        new_dataset = Dataset(name=filename, data=csv_data)
        db.session.add(new_dataset)
        db.session.commit()

        return "File saved successfully."

    except Exception as e:
        # Handle exceptions, log, or provide user-friendly error messages
        print(f"Error saving file: {e}")
        db.session.rollback()
        return "Error saving file"       
        
        
#this is testing purpose to plot 3 dimensional graph
@app.route("/plot")
def plot():
    df=px.data.iris()
    fig2=px.scatter_3d(df, x="sepal_length",y='sepal_width',z="petal_width",color="species",title='Iris Dataset')
    graph2_json=json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("Plot.html",title="Home",graph2_json=graph2_json)

#app_context will handle to create db
app.app_context().push()
db.create_all()