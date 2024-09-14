from sqlalchemy.orm import Session
import database.models as models
import database.schemas as schemas

def get_rm6(serial: str, db: Session):
    return db.query(models.Rm6).filter(models.Rm6.serial == serial).first()

def create_rm6(rm6: schemas.RM6Create, db: Session):
    db_rm6 = models.Rm6(
        serial=rm6.serial,
        date_in=rm6.date_in,
        cause=rm6.cause,
        storage=rm6.storage
    )
    db.add(db_rm6)
    db.commit()
    db.refresh(db_rm6)
    return db_rm6

def update_rm6(serial: str, rm6_update: schemas.RM6, db: Session):
    db_rm6 = db.query(models.Rm6).filter(models.Rm6.serial == serial).first()
    
    if not db_rm6:
        return None

    db_rm6.date_in = rm6_update.date_in
    db_rm6.date_out = rm6_update.date_out
    db_rm6.cause = rm6_update.cause
    db_rm6.storage = rm6_update.storage

    db.commit()
    db.refresh(db_rm6)
    
    return db_rm6

