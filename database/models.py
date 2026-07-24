from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from database.database import Base


class ScanRun(Base):
    __tablename__ = "scan_runs"

    id = Column(Integer, primary_key=True)

    scan_mode = Column(String(30))

    started_at = Column(DateTime, default=datetime.utcnow)

    status = Column(String(20))

    findings = relationship("Finding", back_populates="scan")


class Resource(Base):

    __tablename__ = "resources"

    id = Column(Integer, primary_key=True)

    service = Column(String(20))

    resource_id = Column(String(255))

    resource_name = Column(String(255))

    region = Column(String(50))


class Finding(Base):

    __tablename__ = "findings"

    id = Column(Integer, primary_key=True)

    scan_id = Column(Integer, ForeignKey("scan_runs.id"))

    service = Column(String(30))

    resource_name = Column(String(255))

    severity = Column(String(20))

    title = Column(String(255))

    description = Column(Text)

    recommendation = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

    scan = relationship("ScanRun", back_populates="findings")
