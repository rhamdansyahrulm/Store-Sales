import os
from google.cloud import bigquery, storage
import re
import pickle
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta
import calendar
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import warnings
warnings.filterwarnings("ignore")


# Initialize the Google Cloud Storage client and get the blob
client = storage.Client()
bucket = client.get_bucket("store_sales_ecuador")
blob = bucket.blob('voltaic-reducer-399714-e176465ceed7.json')

# Download the JSON data as a string
json_data = blob.download_as_text()

# Write the JSON data to a file
with open('service_account_key.json', 'w') as json_file:
    json_file.write(json_data)

# Set the JSON file path as the GOOGLE_APPLICATION_CREDENTIALS environment variable
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service_account_key.json'
project_id = 'voltaic-reducer-399714'
dataset_id = 'store_sales_ecuador'

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.datetime(2023, 9, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 5,
    'retry_delay': datetime.timedelta(minutes=5),
}

# Function to read data from a BigQuery table using a SQL query
def read_bigquery_table(sql_query):
    # Initialize the BigQuery client
    client = bigquery.Client()
    
    # Run the SQL query
    query_job = client.query(sql_query)
    
    # Get the query results
    results = query_job.result()
    
    # Initialize a list to store query results in the form of dictionaries
    query_results = []
    
    # Loop through the query results and convert each row into a dictionary
    for row in results:
        row_dict = dict(row.items())
        query_results.append(row_dict)
    
    return query_results

# Function to import a pickle (.pkl) file from Google Cloud Storage
def import_pkl_file(filename, bucket_name="store_sales_ecuador"):
    # Initialize the Google Cloud Storage client
    client = storage.Client()
    
    # Get the specified bucket
    bucket = client.get_bucket(bucket_name)
    
    # Get the blob (object) with the given filename
    blob = bucket.blob(filename)
    
    # Download the pickle data as a string
    pickle_data = blob.download_as_string()
    
    # Deserialize the pickle data into a Python object
    data = pickle.loads(pickle_data)

    return data

# Function to process a text description by removing certain words and finding specific keywords
def process_description(text):
    # List of words to remove from the text
    words_to_remove = ['puente', 'recupero', 'traslado']
    
    # List of words to find in the text
    words_to_find = ['fundacion', 'provincializacion', 'terremoto manabi', 'mundial de futbol brasil', 'fundacion', 'cantonizacion', 'primer dia del ano', 'independencia', 'navidad', 'dia de la madre']
    
    # Convert the text to lowercase for case-insensitive matching
    text_lower = text.lower()
    
    # Initialize a dictionary to store the processed information
    description_dict = {
        'original_text': text,
        'processed_text': text_lower,
        'matched_word': None
    }

    # Remove specific words from the processed text using regular expressions
    for word in words_to_remove:
        description_dict['processed_text'] = re.sub(r'\b' + re.escape(word) + r'\b', '', description_dict['processed_text'])

    # Search for specific words in the processed text
    for word in words_to_find:
        match = re.search(word, description_dict['processed_text'])
        if match:
            description_dict['matched_word'] = word
            break
    
    return description_dict

def create_windowed_data_dict(data, i, window_size, stride):
    # Extract a window of sales values starting from index 'i'
    windowed_list = data["sales"][i:i+window_size].values.tolist()
    
    # Create a dictionary with keys like 'sales_1', 'sales_2', ...
    windowed_dict = {f'sales_{i}': windowed_list[i] for i in range(1, window_size + 1)}
    
    return windowed_dict



# Function to fetch revenue data for a given date
def revenue(ds):
    # Convert the input string to a datetime object
    ds_date = datetime.datetime.strptime(ds, '%Y-%m-%d')
    
    year = ds_date.year
    month = ds_date.month + 1
    start = datetime.datetime(year, month, 1) - datetime.timedelta(days=6)
    end = datetime.datetime(year, month, calendar.monthrange(year, month)[1])

    # Define the BigQuery table and query for revenue data
    table_revenue = 'data_sept'
    query_revenue = f"SELECT * FROM `{project_id}.{dataset_id}.{table_revenue}` ORDER BY store_nbr, date ASC"

    client = bigquery.Client()
    query_job = client.query(query_revenue)
    results = query_job.result()

    revenue_data = []

    for row in results:
        row_dict = dict(row.items())
        row_dict['date'] = row_dict['date'].strftime('%Y-%m-%d')  # Convert date to string
        revenue_data.append(row_dict)

    # Filter data based on date range
    filtered_data = [row for row in revenue_data if start <= datetime.datetime.strptime(row['date'], '%Y-%m-%d') <= end]

    return filtered_data

# Function to fetch store location data
def stores():
    table_store = 'stores_location'
    query_store = f"SELECT * FROM `{project_id}.{dataset_id}.{table_store}`"

    client = bigquery.Client()
    query_job = client.query(query_store)
    results = query_job.result()

    stores_data = []

    for row in results:
        row_dict = dict(row.items())
        stores_data.append(row_dict)

    return stores_data

# Function to fetch oil price data
def oil_prices():
    table_oil = 'oil_prices'
    query_oil = f"SELECT * FROM `{project_id}.{dataset_id}.{table_oil}` ORDER BY date ASC"

    client = bigquery.Client()
    query_job = client.query(query_oil)
    results = query_job.result()

    oil_prices_data = []

    for row in results:
        row_dict = dict(row.items())
        row_dict['date'] = row_dict['date'].strftime('%Y-%m-%d')  # Convert date to string
        oil_prices_data.append(row_dict)

    return oil_prices_data

# Function to fetch event data for a given date
def events(ds):
    ds_date = datetime.datetime.strptime(ds, '%Y-%m-%d')
    table_events = 'events'
    query_events = f"SELECT * FROM `{project_id}.{dataset_id}.{table_events}` ORDER BY date ASC"

    client = bigquery.Client()
    query_job = client.query(query_events)
    results = query_job.result()

    events_data = []

    for row in results:
        row_dict = dict(row.items())
        # Convert date to datetime
        row_dict['date'] = datetime.datetime.combine(row_dict['date'], datetime.datetime.min.time())
        events_data.append(row_dict)

    # Filter data based on date range and transferred flag
    filtered_data = [row for row in events_data if ds_date <= row['date'] <= datetime.datetime(ds.year, ds.month, calendar.monthrange(ds.year, ds.month)[1]) and not row['transferred']]

    return filtered_data


# Function to merge various datasets into a single dataset
def merge_dataset(ti):
    # Pull data from XComs of different tasks
    revenue_data = ti.xcoms_pull(task_ids="revenue")
    stores_data = ti.xcoms_pull(task_ids="stores")
    oil_prices_data = ti.xcoms_pull(task_ids="oil_prices")
    events_data = ti.xcoms_pull(task_ids="events")
    
    merge_data_list = []
    
    for index, revenue_row in revenue_data.iterrows():
        store_nbr = int(revenue_row['store_nbr'])
        
        # Fetch store information based on store number
        store_info = stores_data[(stores_data['store_nbr'] == store_nbr)]
        
        # Fetch oil price data for the same date as revenue data
        oil_price_row = oil_prices_data[(oil_prices_data['date'] == revenue_row['date'])]
        
        merge_dict = {
            'store_nbr': store_nbr,
            'date': revenue_row['date'],
            'sales': revenue_row['sales'],
            'onpromotion': revenue_row['onpromotion'],
            'city': store_info['city'].values[0],
            'state': store_info['state'].values[0],
            'diesel': oil_price_row['diesel'].values[0],
            'gasoline': oil_price_row['gasoline'].values[0],
            'case_Local': None,
            'description_Local': None,
            'case_Regional': None,
            'description_Regional': None,
            'case_National': None,
            'description_National': None,
        }
        
        merge_data_list.append(merge_dict)
    
    for event_row in events_data.iterrows():
        event_row = event_row[1]
        
        # Check if the event is not transferred
        if not event_row['transferred']:
            scales = {"Local": "Local", "Regional": "Regional"}
            desc = process_description(event_row['description'])
            
            for key_scale, value_scale in scales.items():
                if event_row['scale'] == key_scale:
                    for merge_dict in merge_data_list:
                        if (merge_dict['city'] == event_row['locale'] or merge_dict['state'] == event_row['locale']) and merge_dict['date'] == event_row['date']:
                            merge_dict[f'case_{value_scale}'] = event_row['event_type']
                            merge_dict[f'description_{value_scale}'] = desc
                elif event_row['scale'] == "National":
                    for merge_dict in merge_data_list:
                        if merge_dict['date'] == event_row['date']:
                            merge_dict['case'] = event_row['event_type']
                            merge_dict['description'] = desc
    
    # Handle missing values by filling them with "Work Day"
    for merge_dict in merge_data_list:
        case_columns = ["case_National", "case_Local", "case_Regional"]
        description_columns = ["description_National", "description_Local", "description_Regional"]
        
        for case_column in case_columns:
            if merge_dict[case_column] is None:
                merge_dict[case_column] = "Work Day"
        
        for description_column in description_columns:
            if merge_dict[description_column] is None:
                merge_dict[description_column] = "Work Day"
    
    return merge_data_list

# Function to preprocess the merged dataset
def preprocessing(ti):
    data = ti.xcoms_pull(task_ids="merge_dataset")
    transformed_data_list = []
    encode_columns = ['case_National', 'case_Local', 'case_Regional', 'description_Local', 'description_Regional', 'description_National']
    
    # Load label encoders and scalers from pickle files
    label_encoders = import_pkl_file("label_encoders.pkl")
    scalers = import_pkl_file("scaler.pkl")
    
    for encode_column in encode_columns:
        # Transform categorical data using label encoders
        data[encode_column] = label_encoders[encode_column if encode_column.split("_")[0] != "case" else "case"].transform(data[encode_column])
    
    for index, row in enumerate(data):
        store_key = f"store_{int(row['store_nbr'])}"
        scaler = scalers[store_key]
        transformed_data = scaler.transform(row['sales':].values.reshape(1, -1))
        
        transformed_dict = {
            'store_nbr': row['store_nbr'],
            'date': row['date'],
            'sales': row['sales'],
            'onpromotion': row['onpromotion'],
        }
        
        for i, feature_name in enumerate(data.columns[4:]):
            transformed_dict[feature_name] = transformed_data[0][i]
        
        transformed_data_list.append(transformed_dict)

    return transformed_data_list

# Function to make predictions
def predict(ds, ti):
    # Pull preprocessed data from XComs
    data = ti.xcoms_pull(task_ids="preprocessing")
    
    # Create a copy of the data for modification
    new_datas = data.copy()
    
    # Extract dates and remove the 'date' column for prediction
    dates = new_datas["date"]
    new_datas.drop("date", axis=1, inplace=True)
    
    # Define the folder where regression models and scalers are stored
    foldername = "reg_models/"
    
    # Load scalers from a pickle file
    scalers = import_pkl_file("scaler.pkl")
    
    # Initialize a list to store rows for merging
    merging_rows = []
    
    # Iterate over unique store numbers in the data
    for store_nbr in data["store_nbr"].unique():
        store_key = f"store_{int(store_nbr)}"
        
        # Retrieve the scaler for the current store
        scaler = scalers[store_key]
        
        # Construct the file path for the regression model of the store
        filepath = os.path.join(foldername, f"reg_store_{int(store_nbr)}.pkl")
        
        # Load the regression model from the file
        model = import_pkl_file(filepath)
        
        # Extract data specific to the current store
        data_store = new_datas[new_datas["store_nbr"] == store_nbr]
        
        # Calculate the total number of days to make predictions
        total_days = len(data_store) - 6
        
        # Iterate over the days to make predictions
        for i in range(total_days):
            index = int(((total_days + 6) * (store_nbr - 1)) + i)
            
            # Create a windowed data dictionary for the current day
            windowed_data = create_windowed_data_dict(new_datas, index, 6, 1)
            
            merging_row = {
                'store_nbr': data_store.iloc[i + 6:i + 7]['store_nbr'].values[0],
                'date': data_store.iloc[i + 6:i + 7]['date'].values,
                'sales': data_store.iloc[i + 6:i + 7]['sales'].values[0],
                'onpromotion': data_store.iloc[i + 6:i + 7]['onpromotion'].values[0],
            }
            
            # Add windowed data to the merging row
            for feature_name, feature_value in windowed_data.items():
                merging_row[feature_name] = feature_value
            
            # Prepare the features for prediction
            prediction_features = np.array([list(merging_row.values())[3:]])  # Exclude store_nbr, date, sales, onpromotion
            
            # Make the prediction using the loaded regression model
            prediction = model.predict(prediction_features)
            
            # Update the "sales" column in the current row with the prediction
            new_datas.at[index + 6, "sales"] = prediction[0]
        
        # Identify the rows to be inverse-transformed
        rows_to_inverse_transform = new_datas[new_datas["store_nbr"] == store_nbr].index
        
        # Inverse transform the sales data back to its original scale
        new_datas.loc[rows_to_inverse_transform, new_datas.columns != "store_nbr"] = scaler.inverse_transform(new_datas.loc[rows_to_inverse_transform, new_datas.columns != "store_nbr"])
    
    # Re-insert the "date" column
    new_datas.insert(1, "date", dates)
    
    # Print a success message
    print("predict Success")
    
    # Filter data for the next month based on the input date
    return new_datas[new_datas["date"] >= (ds + relativedelta(months=1))].iloc[:, :4]

def save_predict(ti):
    data = ti.xcoms_pull(task_ids="preprocessing")
    table_id = "predict_data"
    # Define the schema for the table
    schema = [
        bigquery.SchemaField('store_nbr', 'INTEGER'),
        bigquery.SchemaField('date', 'TIMESTAMP'),
        bigquery.SchemaField('sales', 'FLOAT'),
        bigquery.SchemaField('onpromotion', 'FLOAT')
    ]
    
    client = bigquery.Client(project=project_id)
    table_ref = client.dataset(dataset_id).table(table_id)
    table = bigquery.Table(table_ref, schema=schema)
    
    try:
        client.create_table(table)
        print(f'Table {table_id} created successfully in dataset {dataset_id}.')
    except Exception as e:
        print(f'Error creating table: {str(e)}')
        
    data_dict_list = data.to_dict(orient='records')
    
    # Create a list to hold BigQuery rows
    rows_to_insert = []
    
    # Iterate over the data and format it for BigQuery
    for row in data_dict_list:
        formatted_row = {
            'store_nbr': int(row['store_nbr']),
            'date': row['date'].strftime('%Y-%m-%d %H:%M:%S'),
            'sales': float(row['sales']),
            'onpromotion': float(row['onpromotion'])
        }
        rows_to_insert.append(formatted_row)
    
    # Create the BigQuery table reference
    table_ref = client.dataset(dataset_id).table(table_id)
    
    # Insert data into the table
    try:
        insert_job = client.insert_rows_json(table_ref, rows_to_insert)
        print(f'{len(rows_to_insert)} rows inserted into {table_id} successfully.')
    except Exception as e:
        print(f'Error inserting data into table: {str(e)}')

    
dag = DAG(
    dag_id='store_sales_ecuador',
    description='airflow for store sales in Ecuador',
    default_args=default_args,
    start_date=datetime.datetime(2023, 1, 1),
    schedule_interval='@monthly',
)

task1 = PythonOperator(
    task_id='revenue',
    python_callable=revenue,
    dag=dag,
)

task2 = PythonOperator(
    task_id='stores',
    python_callable=stores,
    dag=dag,
)

task3 = PythonOperator(
    task_id='oil_prices',
    python_callable=oil_prices,
    dag=dag,
)

task4 = PythonOperator(
    task_id='events',
    python_callable=events,
    dag=dag,
)

task5 = PythonOperator(
    task_id='merge_dataset',
    python_callable=merge_dataset,
    dag=dag,
)

task6 = PythonOperator(
    task_id='preprocessing',
    python_callable=preprocessing,
    dag=dag,
)

task7 = PythonOperator(
    task_id='predict',
    python_callable=predict,
    dag=dag,
)
task8 = PythonOperator(
    task_id='save_predict',
    python_callable=save_predict,
    dag=dag,
)

[task1, task2, task3, task4] >> task5 >> task6 >> task7 >> task8