from sqlalchemy.orm import Session
from app.database.db import SessionLocal
from app.database.models import ClaimHistory


def save_claim(claim, verdict, confidence, explanation):
    db: Session = SessionLocal()

    record = ClaimHistory(
        claim=claim,
        verdict=verdict,
        confidence=confidence,
        explanation=explanation,
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    db.close()

    return record


def get_claim_history():
    db: Session = SessionLocal()

    history = (
        db.query(ClaimHistory)
        .order_by(ClaimHistory.id.desc())
        .all()
    )

    result = []

    for item in history:
        result.append({
            "id": item.id,
            "claim": item.claim,
            "verdict": item.verdict,
            "confidence": item.confidence,
            "explanation": item.explanation,
        })

    db.close()

    return result


def get_statistics():
    db: Session = SessionLocal()

    total = db.query(ClaimHistory).count()

    supported = (
        db.query(ClaimHistory)
        .filter(ClaimHistory.verdict == "SUPPORTED")
        .count()
    )

    contradicted = (
        db.query(ClaimHistory)
        .filter(ClaimHistory.verdict == "CONTRADICTED")
        .count()
    )

    insufficient = (
        db.query(ClaimHistory)
        .filter(ClaimHistory.verdict == "INSUFFICIENT_EVIDENCE")
        .count()
    )

    db.close()

    return {
        "total_claims": total,
        "supported": supported,
        "contradicted": contradicted,
        "insufficient_evidence": insufficient,
    }


def delete_history():
    db: Session = SessionLocal()

    db.query(ClaimHistory).delete()

    db.commit()

    db.close()

    return {"message": "History deleted successfully"}