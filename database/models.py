from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from database.database import Base


class ScanRun(Base):
    __tablename__ = "scan_runs"

    id = Column(Integer, primary_key=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), nullable=False)

    findings = relationship(
        "Finding",
        back_populates="scan",
        cascade="all, delete-orphan",
    )


class Finding(Base):
    __tablename__ = "findings"

    id = Column(Integer, primary_key=True)

    scan_id = Column(
        Integer,
        ForeignKey("scan_runs.id"),
        nullable=False,
    )

    # Raw scanner data
    service = Column(String(50), nullable=False)
    resource = Column(String(255), nullable=False)
    severity = Column(String(20), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    recommendation = Column(Text)

    # AI Analysis (Gemini)
    ai_explanation = Column(Text)
    business_impact = Column(Text)
    console_remediation = Column(Text)
    cli_remediation = Column(Text)

    scan = relationship("ScanRun", back_populates="findings")
