from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import relationship
from datetime import datetime

from database.database import Base


class ScanRun(Base):
    __tablename__ = "scan_runs"

    id = Column(Integer, primary_key=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50))

    findings = relationship("Finding", back_populates="scan")


class Finding(Base):
    __tablename__ = "findings"

    id = Column(Integer, primary_key=True)

    scan_id = Column(Integer, ForeignKey("scan_runs.id"))

    service = Column(String(50))
    resource = Column(String(255))
    severity = Column(String(20))
    title = Column(String(255))
    description = Column(Text)
    recommendation = Column(Text)

    scan = relationship("ScanRun", back_populates="findings")
