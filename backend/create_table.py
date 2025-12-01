import os
import psycopg2
from urllib.parse import urlparse

# Database URL from your Render PostgreSQL instance
DATABASE_URL = "postgresql://healthmate_db:xMTEBZVV79F6Ts9iEnUh75VYbQbjOmUS@dpg-d4mjtd2li9vc73esoaf0-a.singapore-postgres.render.com/healthmate_db_aejf"

def create_table():
    try:
        # Parse the DATABASE_URL
        result = urlparse(DATABASE_URL)
        connection = psycopg2.connect(
            database=result.path.lstrip('/'),
            user=result.username,
            password=result.password,
            host=result.hostname,
            port=result.port
        )

        cursor = connection.cursor()

        # SQL statement to create a new table (customize as needed)
        create_table_query = """
        CREATE TABLE IF NOT EXISTS example_table (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

        # Execute the query
        cursor.execute(create_table_query)
        connection.commit()

        print("Table 'example_table' created successfully!")

        # Optional: Verify the table exists
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'example_table';")
        if cursor.fetchone():
            print("Verification: Table exists.")
        else:
            print("Verification: Table does not exist.")

    except Exception as error:
        print(f"Error creating table: {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    create_table()
