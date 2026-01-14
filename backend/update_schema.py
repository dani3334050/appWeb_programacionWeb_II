from app import create_app, db
from sqlalchemy import text

def update_schema():
    app = create_app()
    with app.app_context():
        try:
            # 1. Add user_id column to clients table
            print("Attempting to add user_id column to clients table...")
            with db.engine.connect() as connection:
                # Use a transaction
                with connection.begin():
                    # Check if column exists first to avoid error if run multiple times
                    # This is a bit postgres specific
                    connection.execute(text("""
                        DO $$ 
                        BEGIN 
                            IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                                           WHERE table_name='clients' AND column_name='user_id') THEN 
                                ALTER TABLE clients ADD COLUMN user_id INTEGER REFERENCES users(id); 
                            END IF; 
                        END $$;
                    """))
            print("Successfully added user_id column (if it didn't exist).")

            # 2. Ensure new tables (like CarListing) are created
            print("Ensuring all tables exist...")
            db.create_all()
            print("Tables verification complete.")
            
        except Exception as e:
            print(f"Error updating schema: {e}")

if __name__ == "__main__":
    update_schema()
