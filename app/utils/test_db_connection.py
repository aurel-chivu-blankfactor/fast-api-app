from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///./fastapi_app.db"

def test_connection():
    try:
        # Create an engine and connect to the database
        engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
        connection = engine.connect()
        print("Database connection successful!")
        connection.close()
    except Exception as e:
        print("Database connection failed!")
        print(f"Error: {e}")

# Run the test
test_connection()