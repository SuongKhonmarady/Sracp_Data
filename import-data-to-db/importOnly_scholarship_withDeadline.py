import pandas as pd
from sqlalchemy import create_engine

def import_csv_to_database(csv_file, db_host, db_user, db_name, table_name, description_column, link_column):
    """
    Import a CSV file into a MySQL database table, but only rows with valid 'post_at' and 'deadline' and 
    avoid inserting duplicates based on the combination of 'description' and 'link'.
    """
    try:
        # Create the database connection string (no password)
        connection_string = f"mysql+pymysql://{db_user}:@{db_host}/{db_name}"
        
        # Create a database engine
        engine = create_engine(connection_string)
        
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file)
        
        # Print column names for debugging
        print("CSV Columns:", df.columns)
        
        # Clean column names (strip spaces and make lowercase)
        df.columns = df.columns.str.strip().str.lower()
        
        # Ensure 'deadline' and 'post_at' are strings and filter out invalid rows
        df['deadline'] = df['deadline'].astype(str)
        df['post_at'] = df['post_at'].astype(str)

        # Filter out rows where 'deadline' or 'post_at' are 'null', empty, or contain only spaces
        df_filtered = df[
            df['deadline'].notna() & (df['deadline'].str.strip() != '') & (df['deadline'].str.lower() != 'null') &
            df['post_at'].notna() & (df['post_at'].str.strip() != '') & (df['post_at'].str.lower() != 'null')
        ]
        
        # Further filter out rows where 'link' is None or empty
        df_filtered = df_filtered[df_filtered['link'].notna() & (df_filtered['link'].astype(str).str.strip() != '')]

        # Establish a connection to the database
        with engine.connect() as conn:
            # Skip link validation if the foreign key table is not available
            # Get existing data from the table based on description and link columns
            query = f"SELECT {description_column}, {link_column} FROM {table_name}"
            existing_data = pd.read_sql(query, conn)
            
            # Convert rows to tuples and check for matching (description, link) pairs
            existing_tuples = existing_data.apply(tuple, axis=1).tolist()
            
            # Filter out rows in the CSV that already exist in the database based on description and link
            new_data = df_filtered[~df_filtered[[description_column, link_column]].apply(tuple, axis=1).isin(existing_tuples)]
            
            # Check how many rows will be inserted after filtering by link
            print(f"Inserting {len(new_data)} rows into the database.")
            
            # Write the new unique data to the database table
            new_data.to_sql(table_name, con=engine, if_exists='append', index=False)
        
        print(f"Data successfully imported into '{table_name}' table with valid deadlines, post_at, and links.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    csv_file_path = "Feature_Programs_data_modified.csv"  # Path to your CSV file
    db_host = "localhost"       # Database host
    db_user = "root"            # Database username
    db_name = "mydb"            # Database name
    table_name = "scholarships" # Table name in the database
    description_column = "description"  # Column for description (check for case sensitivity)
    link_column = "link"  # Column for link
    
    import_csv_to_database(csv_file_path, db_host, db_user, db_name, table_name, description_column, link_column)
