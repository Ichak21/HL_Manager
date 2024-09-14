from database import queries, database, schemas
from sqlalchemy.orm import Session
from datetime import datetime

def add_offline_RM6(rm6: schemas.RM6Create, db : Session = database.SessionLocal()):
    return queries.create_rm6(rm6=rm6, db=db)

def del_offline_RM6(rm6_serial: str, db : Session = database.SessionLocal()):
    db_rm6 = queries.get_rm6(serial=rm6_serial, db=db)
    db_rm6.date_out = datetime.now()
    
    return queries.update_rm6(serial=rm6_serial, rm6_update=db_rm6, db=db)

def find_RM6(rm6_serial: str, db : Session = database.SessionLocal()):
    return queries.get_rm6(serial=rm6_serial, db=db)








# def main():
#     database.init_db()
    
#     my_rm6 = schemas.RM6Create(
#         serial="1234",
#         cause = "reparation",
#         storage="area1",
#         date_in=datetime.now(),
#         date_out=None
#         )

#     add_offline_RM6(my_rm6)
#     db_rm6 = find_RM6(my_rm6.serial)
#     print(f'{db_rm6.serial}|{db_rm6.serial}|{db_rm6.cause}|{db_rm6.storage}|{db_rm6.date_in}|{db_rm6.date_out}|')
#     del_offline_RM6(my_rm6.serial)
#     print(f'{db_rm6.serial}|{db_rm6.serial}|{db_rm6.cause}|{db_rm6.storage}|{db_rm6.date_in}|{db_rm6.date_out}|')
    
# # Point d'entrée du programme
# if __name__ == "__main__":
#     main()