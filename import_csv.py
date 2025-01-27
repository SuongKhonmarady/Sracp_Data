import pandas as pd
from sqlalchemy import create_engine

def import_csv_to_database(csv_file, db_host, db_user, db_name, table_name):
    """
    Import a CSV file into a MySQL database table.

    Args:
        csv_file (str): Path to the CSV file.
        db_host (str): MySQL database host (e.g., 'localhost').
        db_user (str): MySQL username.
        db_name (str): MySQL database name.
        table_name (str): Name of the database table.
    """
    try:
        # Create the database connection string (no password)
        connection_string = f"mysql+pymysql://{db_user}:@{db_host}/{db_name}"
        
        # Create a database engine
        engine = create_engine(connection_string)
        
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file)
        
        # Write the DataFrame to the database table
        df.to_sql(table_name, con=engine, if_exists='append', index=False)
        
        print(f"Data successfully imported into '{table_name}' table.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    csv_file_path = "scholarship_data_with_deadlines.csv"  # Path to your CSV file
    db_host = "localhost"       # Database host
    db_user = "root"            # Database username
    db_name = "scan-fb"   # Database name
    table_name = "posts"   # Table name in the database
    
    import_csv_to_database(csv_file_path, db_host, db_user, db_name, table_name)
