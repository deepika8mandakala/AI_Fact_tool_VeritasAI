from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from app.database.db import Base


class ClaimHistory(Base):
    __tablename__ = "claim_history"

    id = Column(Integer, primary_key=True, index=True)

    claim = Column(String)

    verdict = Column(String)

    confidence = Column(Float)

    explanation = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)