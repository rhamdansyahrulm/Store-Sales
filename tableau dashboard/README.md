# [Ecuador's Store Dashboard](https://public.tableau.com/views/EcuadorsStoreSales/products?:language=en-US&:display_count=n&:origin=viz_share_link)

<b>Ecuador's Store Dashboard</b> It is a data visualization depicting product sales at a store in Ecuador. The images below represent views from this dashboard, displaying various data available from the dataset..

<div align="center">
  <a href="https://public.tableau.com/views/EcuadorsStoreSales/products?:language=en-US&:display_count=n&:origin=viz_share_link">
    <img src="https://github.com/rhamdansyahrulm/Store-Sales/assets/141615487/d497de75-6d5f-4aa4-b498-a965350bd561" alt="Ecuador's Store Dashboard" width="45%">
  </a>
  <a href="https://public.tableau.com/views/EcuadorsStoreSales/products?:language=en-US&:display_count=n&:origin=viz_share_link">
    <img src="https://github.com/rhamdansyahrulm/Store-Sales/assets/141615487/75025239-9d79-4493-856e-3436ea424874" alt="Ecuador's Store Dashboard" width="45%">
  </a>
</div>

## Dashboard Description

### Home

The "Home" dashboard is designed to provide a comprehensive overview of the overall performance of all stores. This dashboard serves as a tool for monitoring the business's overall performance at a glance. By presenting relevant data in the form of charts and figures, it allows stakeholders to quickly assess whether the business is meeting its targets. Some of the key charts included on this dashboard are:

- **Revenue**: This chart displays the total revenue generated.
- **Total Transactions**: It presents the total number of transactions.
- **Total Promotions**: This chart shows the overall promotional activity.
- **Sales Distribution**: A visual representation of sales distribution.
- **Top Sales by City and State**: It highlights the top-performing cities and states.
- **Total Sales by Store Type**: This chart breaks down sales by store type.

### Products

The "Products" dashboard is designed to display sales results based on product groups. This dashboard can be used to plan more effective sales and promotional strategies. It provides insights into when and how to promote specific products based on sales trends within each product group. Some of the key charts included on this dashboard are:

- **Value Trending**: This chart visualizes the trending of values.
- **Top Sales on Each Product Group**: It identifies the top-selling products within each product group.
- **Top Promotional Products**: This chart showcases the most successful promotional products.

# Data Pipeline (Monthly Store Sales Prediction)

This project implements a Directed Acyclic Graph (DAG) using Apache Airflow to perform daily store sales prediction for the upcoming month in Ecuador. The DAG is designed to run automatically at 00:00 on the 1st day of each month. Here is the DAG workflow built using Apache Airflow.
<div align="center">
    <img src="https://github.com/rhamdansyahrulm/Store-Sales/assets/141615487/d5d70cf2-3fc9-4d0e-964e-a1527885c31b" alt="Ecuador's Store Dashboard" width="65%">
</div>

This data pipeline is used to predict revenue for a retail store chain. The pipeline consists of the following steps:

1. **Data retrieval:**
   The pipeline retrieves all the datasets that will be used from BigQuery (revenue, oil prices, events, and stores).
3. **Data merging:**
   The pipeline merges the datasets based on store number and date.
5. **Data preprocessing:**
   The pipeline performs data preprocessing, including data normalization, labeling, and stopword removal. Additionally, the pipeline adds feature columns by performing windowed dataset.
7. **Prediction:**
   The pipeline performs prediction using a machine learning model.

**Notes:**
- All the files required for scaling, labeling, and prediction are stored in Google Cloud Storage.
Data retrieval
- The pipeline retrieves all the datasets that will be used from BigQuery. The datasets are stored in the following tables:
  `revenue`: This table contains the historical revenue data for each store.
  `oil_prices`: This table contains the historical oil prices.
  `events`: This table contains the historical events that may affect revenue, such as holidays and promotions.
  `stores`: This table contains information about each store, such as location and size.
