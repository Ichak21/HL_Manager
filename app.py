from database import queries, database, schemas
from modules import exceptions
from rich.text import Text
import json
import os
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Footer, Header, Static, Input, ProgressBar, Label
from textual.containers import Center, VerticalScroll
from sqlalchemy.orm import Session
from datetime import datetime

PATH_SETTING = f'{os.getcwd()}\Setting.json'
PATH_LOCAL = f'{os.getcwd()}\Local.json'
PATH_STYLE_OFFLINE_MANAGER = f'{os.getcwd()}\styles\offline_manager.css'

CAUSE_DICT = {}
STORAGE_DICT = {}

def init_configuration():
    with open(PATH_SETTING, 'r') as file:
        setting_json  = json.load(file)
        
    global CAUSE_DICT
    global STORAGE_DICT
    
    CAUSE_DICT = {cause["name"]: cause["color"] for cause in setting_json ["settings"]["causes"]}
    STORAGE_DICT = {storage["area"]: storage["secteur"] for storage in setting_json ["settings"]["storage"]}


def find_RM6(rm6_id: int, db : Session = database.SessionLocal()):
    return queries.get_rm6(rm6_id=rm6_id, db=db)

def find_all_RM6_offline(db : Session =database.SessionLocal()):
    return queries.get_rm6_sans_date_out(db=db)

def add_offline_RM6(rm6: schemas.RM6Create, db : Session = database.SessionLocal()):
    lock_double = queries.get_rm6_via_sn_sans_out(serial=rm6.serial, db=db)
    
    if lock_double is not None:
        raise exceptions.ErreurRM6Existe(f'{lock_double.serial} | {lock_double.storage}')
    
    return queries.create_rm6(rm6=rm6, db=db)

def del_offline_RM6(rm6_serial: str, db : Session = database.SessionLocal()):
    db_rm6 = queries.get_rm6_via_sn_sans_out(serial=rm6_serial, db=db)
    db_rm6.date_out = datetime.now()
    return queries.update_rm6(id=db_rm6.id, rm6_update=db_rm6, db=db)

def _create_table_display_dataset():
    datas_rows = []
    headers = ("SERIAL", "CAUSE", "STORAGE", "DATE_IN", "DATE_OUT")
    datas_rows.append(headers)
    all_rm6_off_line = find_all_RM6_offline()
    
    for rm6_found in all_rm6_off_line:
        datas_rows.append(rm6_found.display_row_table())
    
    return datas_rows

class MyProgressBar(Static):
    
    def __init__(self, area: str):
        self.area = area
        super().__init__()
    
    def compose(self):
        yield Label(self.area, classes="bar_label")
        yield ProgressBar(name=self.area, classes="bars", show_eta=False)
            
class AreaProgressBars_Display(Static):
    def compose(self):
        for area in STORAGE_DICT:
            yield MyProgressBar(area=area)

class Head_Display(Static):
    def compose(self):
        yield Input()
        yield AreaProgressBars_Display()
        

class OffLine_ManagerApp(App):
    
    CSS_PATH = PATH_STYLE_OFFLINE_MANAGER
    
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Head_Display()
        yield DataTable()


    def on_mount(self) -> None:
        ROWS = _create_table_display_dataset()
        table = self.query_one(DataTable)
        table.cursor_type = "none"
        table.zebra_stripes = True

        table.add_columns(*ROWS[0])
        # table.add_rows(ROWS[1:])
        for row in ROWS[1:]:
            # Adding styled and justified `Text` objects instead of plain strings.
            styled_row = [
                Text(str(cell), style="#EA9544", justify="center") for cell in row
            ]
            table.add_row(*styled_row)


app = OffLine_ManagerApp()
if __name__ == "__main__":
    init_configuration()
    app.run()


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