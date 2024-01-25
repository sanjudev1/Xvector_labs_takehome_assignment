# Project Name

Data Application - Visualization and Analysis

## Project Overview

This project aims to create a simple data application where users can upload datasets, view a list of uploaded datasets, and perform visualizations and analyses on the data. The application is built using the Flask framework, PostgreSQL as the data store, and Plotly.js for creating interactive plots.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
- [API Endpoints](#api-endpoints)
- [Technologies Used](#technologies-used)
- [Issues Faced](#issues-faced)
- [Contact](#contact)

## Features

1. **Upload Data:**
   - Users can upload CSV files with a user-provided name for the dataset.
   - Uploaded data is stored as a table in a PostgreSQL database.

2. **View Uploaded Data:**
   - Users can view the list of all stored datasets.

3. **Compute Operations:**
   - Users can perform computations on the data, such as finding the minimum, maximum, or sum of a selected column.
   - Input: Data name, column name, operation (min, max, sum).
   - Output: Result of the selected operation on the chosen column.

4. **Create Plots:**
   - Users can create plots of the data using Plotly.js.
   - Input: Data name, two columns of the selected data.
   - Output: Plot of selected column values against X and Y axes.


## Getting Started

To run the project locally, follow these steps:

1. Clone the repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Set up a PostgreSQL database and update the configuration in the `config.py` file.
4. Run the application using `python run.py`.
5. Access the application in your browser at `http://localhost:5000`.

## API Endpoints

1. **POST /dataset:**
   - Stores a CSV file with user-provided data name as a table in the database.

2. **GET /dataset:**
   - Gives the list of stored datasets.

3. **POST /dataset/:id/compute:**
   - Computes operations on the data.
   - Fields: [column name, operation (min, max, sum)].

4. **GET /dataset/:id/plot:**
   - Generates a plot of the data.
   - Fields: [column1, column2].

## Technologies Used

- Flask
- PostgreSQL
- Plotly.js

## Issues Faced

# Example of using app_context() to handle database connections
# Utilize the internal database URL during deployment on the Render platform.

## Contact

For any questions or inquiries, feel free to reach out at [sanjeevch.131.@gmail.com].

Happy Coding!

