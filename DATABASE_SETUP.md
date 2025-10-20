# Database Setup Guide

## Overview
This guide documents the PostgreSQL database integration for the Wearable Biosignal Analysis Backend.

## Database Configuration

### Connection Details
The database connection is configured via environment variables in the `.env` file:

```env
DB_NAME=wearable
DB_USER=avnadmin
DB_PASSWORD=your_database_password_here
DB_HOST=your-database-host.aivencloud.com
DB_PORT=28565
```

### Database URL
The connection string is automatically constructed in `app/database.py`:
```
postgresql://avnadmin:PASSWORD@your-database-host.aivencloud.com:28565/wearable
```

## Database Schema

### Tables Created

1. **users** - User information
   - id, user_id, email, full_name
   - created_at, updated_at, is_active
   - user_metadata (JSON)

2. **devices** - Wearable device information
   - id, device_id, user_id (FK)
   - device_type, firmware_version
   - battery_level, signal_strength, is_connected
   - last_connected, created_at, updated_at
   - device_metadata (JSON)

3. **sessions** - Monitoring sessions
   - id, session_id, user_id (FK), device_id (FK)
   - session_type, start_time, end_time, status
   - data_points_collected, average_wellness_score
   - summary, session_metadata (JSON)

4. **biosignal_readings** - Raw biosignal data
   - id, session_id (FK), device_id (FK), timestamp
   - heart_rate, spo2, temperature, activity
   - signal_quality, quality_score

5. **analysis_results** - Processed analysis from proprietary layers
   - id, session_id (FK), timestamp
   - **Clarity Layer**: quality_score, snr, noise_reduced, quality_assessment, artifacts
   - **iFRS Layer**: dominant_frequency, rhythm_classification, respiratory_rate, hrv_score, frequency_bands, hrv_features
   - **Timesystems Layer**: pattern_type, circadian_phase, temporal_consistency, rhythm_score, pattern_recognition, circadian_alignment
   - **LIA Insights**: condition, confidence, wellness_score, probabilities, recommendation, wellness_assessment, risk_factors, positive_indicators

6. **processing_logs** - System logs
   - id, timestamp, layer, level, message
   - data (JSON), session_id (FK)

7. **system_metrics** - Performance metrics
   - id, timestamp, metric_name, metric_value
   - metric_unit, metric_metadata (JSON)

8. **alembic_version** - Migration tracking (managed by Alembic)

## Installation & Setup

### 1. Install Dependencies
```bash
pip install sqlalchemy==2.0.23 psycopg2-binary==2.9.9 alembic==1.13.0 python-dotenv==1.0.0
```

Or install from requirements.txt:
```bash
pip install -r requirements.txt
```

### 2. Verify Database Connection
```bash
python3 -c "from app.database import test_connection; test_connection()"
```

Expected output:
```
✅ Database connection successful!
```

### 3. Initialize Database (Already Done)
The database tables have already been created using Alembic migrations.

### 4. Verify Tables
```bash
python3 verify_database.py
```

## Database Migrations with Alembic

### Current Migration Status
```bash
python3 -m alembic current
```

Output:
```
31dd9183b1bf (head)
```

### Create New Migration
When you modify models in `app/models/db_models.py`:

```bash
python3 -m alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations
```bash
python3 -m alembic upgrade head
```

### Rollback Migration
```bash
# Rollback one migration
python3 -m alembic downgrade -1

# Rollback to specific version
python3 -m alembic downgrade <revision_id>

# Rollback all migrations
python3 -m alembic downgrade base
```

### View Migration History
```bash
python3 -m alembic history
```

## Using the Database in Code

### Import Database Components
```python
from sqlalchemy.orm import Session
from app.database import SessionLocal, get_db
from app.models import db_models
```

### Create Database Session
```python
# Method 1: Using context manager
from app.database import SessionLocal

db = SessionLocal()
try:
    # Your database operations here
    user = db_models.User(
        user_id="user_123",
        email="user@example.com",
        full_name="John Doe"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
finally:
    db.close()
```

### Using with FastAPI Dependency Injection
```python
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db

@app.post("/users/")
def create_user(user_data: dict, db: Session = Depends(get_db)):
    user = db_models.User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
```

## Example Operations

### Create User
```python
from app.database import SessionLocal
from app.models import db_models

db = SessionLocal()

user = db_models.User(
    user_id="user_001",
    email="john@example.com",
    full_name="John Doe",
    is_active=True,
    user_metadata={"preferences": {"theme": "dark"}}
)

db.add(user)
db.commit()
db.refresh(user)

print(f"Created user: {user.user_id}")
db.close()
```

### Create Device
```python
from app.models.schemas import DeviceType

device = db_models.Device(
    device_id="device_001",
    user_id=user.id,  # Reference to user.id (integer)
    device_type=DeviceType.BRACELET,
    firmware_version="1.0.0",
    battery_level=95.0,
    signal_strength=-45,
    is_connected=True,
    device_metadata={"color": "black", "size": "M"}
)

db.add(device)
db.commit()
```

### Create Session
```python
from app.models.schemas import SessionType

session = db_models.Session(
    session_id="session_001",
    user_id=user.id,
    device_id=device.id,
    session_type=SessionType.WORKOUT,
    status="active",
    session_metadata={"location": "gym", "temperature": 22.5}
)

db.add(session)
db.commit()
```

### Store Biosignal Reading
```python
from app.models.schemas import SignalQuality

reading = db_models.BiosignalReading(
    session_id=session.id,
    device_id=device.id,
    heart_rate=75.5,
    spo2=98.2,
    temperature=36.7,
    activity=12.5,
    signal_quality=SignalQuality.GOOD,
    quality_score=0.92
)

db.add(reading)
db.commit()
```

### Store Analysis Result
```python
from app.models.schemas import PatternType, CircadianPhase, RhythmClassification

analysis = db_models.AnalysisResult(
    session_id=session.id,
    clarity_quality_score=0.92,
    clarity_snr=38.5,
    clarity_noise_reduced=False,
    clarity_quality_assessment=SignalQuality.EXCELLENT,
    ifrs_dominant_frequency=1.25,
    ifrs_rhythm_classification=RhythmClassification.NORMAL_SINUS,
    ifrs_respiratory_rate=16.0,
    ifrs_hrv_score=75.0,
    timesystems_pattern_type=PatternType.STABLE,
    timesystems_circadian_phase=CircadianPhase.AFTERNOON,
    timesystems_temporal_consistency=0.88,
    timesystems_rhythm_score=82.0,
    lia_condition="Normal Resting",
    lia_confidence=0.92,
    lia_wellness_score=85.3,
    lia_probabilities={"Normal Resting": 0.92, "Light Activity": 0.05},
    lia_recommendation="Maintain current activity levels",
    lia_wellness_assessment={
        "cardiovascular_health": 85.0,
        "respiratory_health": 90.0,
        "activity_level": 75.0,
        "stress_level": 70.0,
        "overall_wellness": 82.5
    }
)

db.add(analysis)
db.commit()
```

### Query Data
```python
# Get user by user_id
user = db.query(db_models.User).filter(
    db_models.User.user_id == "user_001"
).first()

# Get all active sessions for a user
sessions = db.query(db_models.Session).filter(
    db_models.Session.user_id == user.id,
    db_models.Session.status == "active"
).all()

# Get recent biosignal readings
from sqlalchemy import desc

readings = db.query(db_models.BiosignalReading).filter(
    db_models.BiosignalReading.session_id == session.id
).order_by(desc(db_models.BiosignalReading.timestamp)).limit(100).all()

# Get analysis results with wellness score above 80
high_wellness = db.query(db_models.AnalysisResult).filter(
    db_models.AnalysisResult.lia_wellness_score > 80
).all()
```

## Deployment Considerations

### Environment Variables
Ensure the `.env` file is:
- ✅ Added to `.gitignore` (already done)
- ✅ Never committed to version control
- ✅ Set up in Render.com environment variables

### Render.com Database Setup
When deploying to Render.com:

1. **Option 1: Use Existing Aiven Database**
   - Add environment variables in Render dashboard:
     ```
     DB_NAME=wearable
     DB_USER=avnadmin
     DB_PASSWORD=your_database_password_here
     DB_HOST=your-database-host.aivencloud.com
     DB_PORT=28565
     ```

2. **Option 2: Create Render PostgreSQL**
   - Create PostgreSQL database in Render
   - Render provides `DATABASE_URL` automatically
   - Update `app/database.py` to use `DATABASE_URL` if available

### Running Migrations on Render

Add to `render.yaml`:
```yaml
services:
  - type: web
    name: wearable-biosignal-backend
    buildCommand: |
      pip install -r requirements.txt
      python3 -m alembic upgrade head
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Or add to `build.sh`:
```bash
# Run migrations
echo "Running database migrations..."
python3 -m alembic upgrade head
```

## Database Backup & Restore

### Backup Database
```bash
pg_dump -h your-database-host.aivencloud.com -p 28565 -U avnadmin -d wearable -F c -f backup.dump
```

### Restore Database
```bash
pg_restore -h your-database-host.aivencloud.com -p 28565 -U avnadmin -d wearable backup.dump
```

## Monitoring & Maintenance

### Check Database Size
```python
from app.database import engine

with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT
            pg_size_pretty(pg_database_size('wearable')) as size,
            pg_database_size('wearable') as bytes
    """))
    print(result.fetchone())
```

### Check Table Sizes
```python
with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT
            schemaname,
            tablename,
            pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size,
            pg_total_relation_size(schemaname||'.'||tablename) AS bytes
        FROM pg_tables
        WHERE schemaname = 'public'
        ORDER BY bytes DESC
    """))
    for row in result:
        print(f"{row.tablename}: {row.size}")
```

### Vacuum Database
```python
from sqlalchemy import text

with engine.connect() as conn:
    conn.execution_options(isolation_level="AUTOCOMMIT")
    conn.execute(text("VACUUM ANALYZE"))
```

## Troubleshooting

### Connection Issues

**Problem**: `connection refused` or `timeout`
```
Solution:
- Check .env file exists and has correct credentials
- Verify network connectivity to Aiven
- Check firewall rules
- Ensure database is running
```

**Problem**: `password authentication failed`
```
Solution:
- Verify DB_PASSWORD in .env
- Check username is correct (avnadmin)
- Reset password in Aiven console if needed
```

### Migration Issues

**Problem**: `Target database is not up to date`
```bash
# Check current version
python3 -m alembic current

# Apply pending migrations
python3 -m alembic upgrade head
```

**Problem**: `Can't locate revision identified by '<rev_id>'`
```bash
# Remove alembic_version table entry
# Then re-run migrations
python3 -m alembic upgrade head
```

### Model Changes Not Detected

**Problem**: Autogenerate doesn't detect model changes
```
Solution:
- Ensure models are imported in alembic/env.py
- Verify Base.metadata includes all models
- Check for syntax errors in model definitions
```

## Security Best Practices

1. **Never commit .env file**
   - Always in .gitignore
   - Use Render environment variables in production

2. **Use connection pooling**
   - Already configured in app/database.py
   - pool_size=10, max_overflow=20

3. **Enable SSL**
   - Aiven enforces SSL by default
   - Add `?sslmode=require` to connection string if needed

4. **Use parameterized queries**
   - SQLAlchemy ORM handles this automatically
   - Prevents SQL injection

5. **Regular backups**
   - Schedule automated backups
   - Test restore procedures

6. **Monitor slow queries**
   - Enable query logging
   - Add indexes for frequently queried columns

## Resources

- **SQLAlchemy Documentation**: https://docs.sqlalchemy.org/
- **Alembic Documentation**: https://alembic.sqlalchemy.org/
- **PostgreSQL Documentation**: https://www.postgresql.org/docs/
- **Aiven PostgreSQL**: https://aiven.io/postgresql

## Summary

✅ **Database Connection**: Configured and tested
✅ **8 Tables Created**:
  - users, devices, sessions
  - biosignal_readings, analysis_results
  - processing_logs, system_metrics
  - alembic_version

✅ **Migrations**: Alembic configured and initial migration applied
✅ **Models**: SQLAlchemy models created for all tables
✅ **Ready for Use**: Can now store and retrieve data via API

---

**Next Steps:**
1. Integrate database operations into existing API endpoints
2. Add CRUD operations for users, devices, and sessions
3. Store biosignal readings and analysis results
4. Add data retrieval endpoints
5. Implement data export functionality
