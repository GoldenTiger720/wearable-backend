#!/usr/bin/env python3
"""
Verify database tables and connection
"""

from sqlalchemy import inspect
from app.database import engine, test_connection

def verify_database():
    """Verify database connection and list all tables"""
    print("=" * 80)
    print(" DATABASE VERIFICATION")
    print("=" * 80)
    print()

    # Test connection
    print("1. Testing database connection...")
    if not test_connection():
        print("❌ Connection failed. Exiting.")
        return False
    print()

    # List all tables
    print("2. Listing all tables in the database:")
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    if not tables:
        print("❌ No tables found in database")
        return False

    print(f"✅ Found {len(tables)} tables:")
    for i, table in enumerate(tables, 1):
        print(f"   {i}. {table}")

        # Get columns for each table
        columns = inspector.get_columns(table)
        print(f"      Columns: {', '.join([col['name'] for col in columns[:5]])}")
        if len(columns) > 5:
            print(f"               ...and {len(columns) - 5} more columns")
    print()

    # Check for expected tables
    print("3. Verifying expected tables...")
    expected_tables = [
        'users',
        'devices',
        'sessions',
        'biosignal_readings',
        'analysis_results',
        'processing_logs',
        'system_metrics',
        'alembic_version'
    ]

    missing_tables = [t for t in expected_tables if t not in tables]
    if missing_tables:
        print(f"⚠️  Missing tables: {', '.join(missing_tables)}")
    else:
        print("✅ All expected tables are present!")
    print()

    print("=" * 80)
    print(" DATABASE SETUP COMPLETE!")
    print("=" * 80)
    print()
    print("You can now:")
    print("1. Start the FastAPI server: python3 -m uvicorn app.main:app")
    print("2. Access the API documentation: http://localhost:8000/docs")
    print("3. Use the API endpoints to store and retrieve data")
    print()

    return True

if __name__ == "__main__":
    verify_database()
