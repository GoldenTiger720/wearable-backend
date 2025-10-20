#!/usr/bin/env python3
"""
Test database operations and demonstrate CRUD functionality
"""

from datetime import datetime
from sqlalchemy.orm import Session
from app.database import SessionLocal, test_connection
from app.models import db_models
from app.models.schemas import (
    DeviceType, SessionType, SignalQuality,
    PatternType, CircadianPhase, RhythmClassification
)

def test_database_operations():
    """Test basic database CRUD operations"""
    print("=" * 80)
    print(" DATABASE OPERATIONS TEST")
    print("=" * 80)
    print()

    # Test connection
    print("1. Testing database connection...")
    if not test_connection():
        print("❌ Connection failed. Exiting.")
        return
    print()

    db = SessionLocal()
    try:
        # Create User
        print("2. Creating test user...")
        user = db_models.User(
            user_id=f"test_user_{int(datetime.now().timestamp())}",
            email=f"testuser{int(datetime.now().timestamp())}@example.com",
            full_name="Test User",
            is_active=True,
            user_metadata={"test": True, "created_by": "test_script"}
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"✅ Created user: {user.user_id} (ID: {user.id})")
        print()

        # Create Device
        print("3. Creating test device...")
        device = db_models.Device(
            device_id=f"test_device_{int(datetime.now().timestamp())}",
            user_id=user.id,
            device_type=DeviceType.BRACELET,
            firmware_version="1.0.0",
            battery_level=95.0,
            signal_strength=-45,
            is_connected=True,
            device_metadata={"color": "black", "test": True}
        )
        db.add(device)
        db.commit()
        db.refresh(device)
        print(f"✅ Created device: {device.device_id} (ID: {device.id})")
        print()

        # Create Session
        print("4. Creating test session...")
        session = db_models.Session(
            session_id=f"test_session_{int(datetime.now().timestamp())}",
            user_id=user.id,
            device_id=device.id,
            session_type=SessionType.WORKOUT,
            status="active",
            session_metadata={"test": True, "location": "test_lab"}
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        print(f"✅ Created session: {session.session_id} (ID: {session.id})")
        print()

        # Create Biosignal Reading
        print("5. Creating biosignal reading...")
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
        db.refresh(reading)
        print(f"✅ Created biosignal reading (ID: {reading.id})")
        print(f"   Heart Rate: {reading.heart_rate} BPM")
        print(f"   SpO2: {reading.spo2}%")
        print(f"   Temperature: {reading.temperature}°C")
        print()

        # Create Analysis Result
        print("6. Creating analysis result...")
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
            ifrs_frequency_bands={"vlf": 45.0, "lf": 35.0, "hf": 20.0, "lf_hf_ratio": 1.75},
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
        db.refresh(analysis)
        print(f"✅ Created analysis result (ID: {analysis.id})")
        print(f"   Condition: {analysis.lia_condition}")
        print(f"   Wellness Score: {analysis.lia_wellness_score}")
        print(f"   Confidence: {analysis.lia_confidence}")
        print()

        # Query Data
        print("7. Querying data...")

        # Count records
        user_count = db.query(db_models.User).count()
        device_count = db.query(db_models.Device).count()
        session_count = db.query(db_models.Session).count()
        reading_count = db.query(db_models.BiosignalReading).count()
        analysis_count = db.query(db_models.AnalysisResult).count()

        print(f"✅ Database Statistics:")
        print(f"   Users: {user_count}")
        print(f"   Devices: {device_count}")
        print(f"   Sessions: {session_count}")
        print(f"   Biosignal Readings: {reading_count}")
        print(f"   Analysis Results: {analysis_count}")
        print()

        # Query specific data
        print("8. Testing relationships...")

        # Get user with devices
        user_with_devices = db.query(db_models.User).filter(
            db_models.User.id == user.id
        ).first()
        print(f"✅ User '{user_with_devices.user_id}' has {len(user_with_devices.devices)} device(s)")

        # Get device with sessions
        device_with_sessions = db.query(db_models.Device).filter(
            db_models.Device.id == device.id
        ).first()
        print(f"✅ Device '{device_with_sessions.device_id}' has {len(device_with_sessions.sessions)} session(s)")

        # Get session with readings
        session_with_data = db.query(db_models.Session).filter(
            db_models.Session.id == session.id
        ).first()
        print(f"✅ Session '{session_with_data.session_id}' has:")
        print(f"   - {len(session_with_data.biosignal_readings)} biosignal reading(s)")
        print(f"   - {len(session_with_data.analysis_results)} analysis result(s)")
        print()

        print("=" * 80)
        print(" ALL DATABASE TESTS PASSED! ✅")
        print("=" * 80)
        print()
        print("Database is fully operational and ready to use!")
        print()
        print("Created test records:")
        print(f"  - User: {user.user_id}")
        print(f"  - Device: {device.device_id}")
        print(f"  - Session: {session.session_id}")
        print(f"  - Biosignal Reading ID: {reading.id}")
        print(f"  - Analysis Result ID: {analysis.id}")
        print()

    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    test_database_operations()
