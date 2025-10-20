"""
SQLAlchemy Database Models
Maps to PostgreSQL database tables
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, JSON, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

from app.database import Base
from app.models.schemas import DeviceType, SessionType, SignalQuality, PatternType, CircadianPhase, RhythmClassification


# ============================================================================
# DATABASE MODELS
# ============================================================================

class User(Base):
    """User model for storing user information"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=True, index=True)
    full_name = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    user_metadata = Column(JSON, default={})

    # Relationships
    devices = relationship("Device", back_populates="user")
    sessions = relationship("Session", back_populates="user")


class Device(Base):
    """Device model for storing wearable device information"""
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String(100), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    device_type = Column(SQLEnum(DeviceType), nullable=False)
    firmware_version = Column(String(50), default="1.0.0")
    battery_level = Column(Float, default=100.0)
    signal_strength = Column(Integer, default=-50)
    is_connected = Column(Boolean, default=False)
    last_connected = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    device_metadata = Column(JSON, default={})

    # Relationships
    user = relationship("User", back_populates="devices")
    sessions = relationship("Session", back_populates="device")
    biosignal_readings = relationship("BiosignalReading", back_populates="device")


class Session(Base):
    """Session model for tracking monitoring sessions"""
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    session_type = Column(SQLEnum(SessionType), nullable=False)
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    end_time = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(50), default="active")
    data_points_collected = Column(Integer, default=0)
    average_wellness_score = Column(Float, nullable=True)
    summary = Column(Text, nullable=True)
    session_metadata = Column(JSON, default={})

    # Relationships
    user = relationship("User", back_populates="sessions")
    device = relationship("Device", back_populates="sessions")
    biosignal_readings = relationship("BiosignalReading", back_populates="session")
    analysis_results = relationship("AnalysisResult", back_populates="session")


class BiosignalReading(Base):
    """Raw biosignal data readings from devices"""
    __tablename__ = "biosignal_readings"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Raw biosignal values
    heart_rate = Column(Float, nullable=False)
    spo2 = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    activity = Column(Float, nullable=False)

    # Quality indicators
    signal_quality = Column(SQLEnum(SignalQuality), nullable=True)
    quality_score = Column(Float, nullable=True)

    # Relationships
    session = relationship("Session", back_populates="biosignal_readings")
    device = relationship("Device", back_populates="biosignal_readings")


class AnalysisResult(Base):
    """Processed analysis results from proprietary layers"""
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Clarity Layer Results
    clarity_quality_score = Column(Float, nullable=True)
    clarity_snr = Column(Float, nullable=True)
    clarity_noise_reduced = Column(Boolean, nullable=True)
    clarity_quality_assessment = Column(SQLEnum(SignalQuality), nullable=True)
    clarity_artifacts = Column(JSON, default=[])

    # iFRS Layer Results
    ifrs_dominant_frequency = Column(Float, nullable=True)
    ifrs_rhythm_classification = Column(SQLEnum(RhythmClassification), nullable=True)
    ifrs_respiratory_rate = Column(Float, nullable=True)
    ifrs_hrv_score = Column(Float, nullable=True)
    ifrs_frequency_bands = Column(JSON, nullable=True)  # Store FrequencyBands as JSON
    ifrs_hrv_features = Column(JSON, nullable=True)     # Store HRVFeatures as JSON

    # Timesystems Layer Results
    timesystems_pattern_type = Column(SQLEnum(PatternType), nullable=True)
    timesystems_circadian_phase = Column(SQLEnum(CircadianPhase), nullable=True)
    timesystems_temporal_consistency = Column(Float, nullable=True)
    timesystems_rhythm_score = Column(Float, nullable=True)
    timesystems_pattern_recognition = Column(JSON, nullable=True)
    timesystems_circadian_alignment = Column(JSON, nullable=True)

    # LIA Insights
    lia_condition = Column(String(100), nullable=True)
    lia_confidence = Column(Float, nullable=True)
    lia_wellness_score = Column(Float, nullable=True)
    lia_probabilities = Column(JSON, nullable=True)
    lia_recommendation = Column(Text, nullable=True)
    lia_wellness_assessment = Column(JSON, nullable=True)
    lia_risk_factors = Column(JSON, default=[])
    lia_positive_indicators = Column(JSON, default=[])

    # Relationships
    session = relationship("Session", back_populates="analysis_results")


class ProcessingLog(Base):
    """Logs for processing operations and system events"""
    __tablename__ = "processing_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    layer = Column(String(50), nullable=False, index=True)
    level = Column(String(20), nullable=False)  # INFO, WARNING, ERROR
    message = Column(Text, nullable=False)
    data = Column(JSON, nullable=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=True)


class SystemMetric(Base):
    """System performance and health metrics"""
    __tablename__ = "system_metrics"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    metric_name = Column(String(100), nullable=False, index=True)
    metric_value = Column(Float, nullable=False)
    metric_unit = Column(String(50), nullable=True)
    metric_metadata = Column(JSON, default={})
