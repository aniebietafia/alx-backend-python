# Creating and Populating Database with Data from a CSV File
This setup uses sets up a MySQL database and populates it with data from a CSV file using Python.

## Prerequisites
- MySQL server installed and running.
- Python installed

## Setup Instructions
1. **Clone the repository**:
    ```bash
    git clone git@github.com:aniebietafia/alx-backend-python.git
    cd alx-backend-python/0x00-python-hello_world
    ```
2. **Install Dependencies from the requirements.txt file**:
    ```bash
    pip install -r requirements.txt
    ```
3. **Create a MySQL Database**:
    - Log in to your MySQL server:
      ```bash
      mysql -u root -p
      ```

## Database Setup
Run the following Python script to create the database and table, and populate it with data from the CSV file.

```bash
python 0-main.py
```

## Files
- `seed.py`: Script to create the database and table and populate it with data from the csv file.
- `0-main.py`: Main script to execute the database setup and population on your machine.
```bash
python 0-main.py
```
- `requirements.txt`: Contains the necessary Python packages.
- `1-batch_processing.py`: Script to create a generator that streams rows from an SQL database one by one. 
- Run it using:
```bash
python 1-main.py
```
- `2-lazy_paginate.py`: Script to create a generator that yields an iterable of rows from the database, paginated.
- Run it using:
```bash
python 3-main.py
```
- `4-stream_ages.py`: Script to use a generator to compute a memory-efficient aggregate function i.e average age for a large dataset
- Run it using:
```bash
python 4-stream_ages.py
```
