from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Button, Footer, Header, Label, Input, OptionList, Select, DataTable
from textual.widgets.option_list import Option, Separator
from textual import on
from rich.text import Text
import os

class OutputPopUpScreen(ModalScreen):
    CSS_PATH = f'{os.getcwd()}\styles\popups.css'
    
    def __init__(self, serial:str, storage:str) -> None:
        self.serial = serial
        self.storage = storage
        super().__init__(classes="popup")
    
    def compose(self) -> ComposeResult:
        yield Grid(
            Label(f'Confirmez vous la sortie du RM6 [bold #DC143C]{self.serial}[/bold #DC143C] de la zone [bold #DC143C]{self.storage}[/bold #DC143C] ?', id="OUTquestion"),
            Button("Annuler", variant="error", id="b_OUTcancel"),
            Button("Confirmer", variant="success", id="b_OUTconfirm"),
            id="OUT_dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "b_OUTconfirm":
            self.app.exit() # --> vers sortie du RM6 dans la base
        else:
            self.app.pop_screen() # --> Annule le dernier scan

class InputPopUpScreen(ModalScreen):
    CSS_PATH = f'{os.getcwd()}\styles\popups.css'
    
    def __init__(self, serial:str, storage:str, causes:list) -> None:
        self.serial = serial
        self.storage = storage
        self.causes = causes
        super().__init__(classes="popup")
    
    def compose(self) -> ComposeResult:
        yield Grid(
            Label(f'Souhaitez vous ajout : [bold #DC143C]{self.serial}[/bold #DC143C] a la zone : [bold #DC143C]{self.storage}[/bold #DC143C]', id="INtitle"),
            Label("Causes : ", classes="INlabel"),
            Label("Commentaire :", classes='INlabel'),
            Select(((cause, cause) for cause in self.causes), classes="INinput"),
            Input(classes="INinput"),
            Button("Annuler", variant="error", id="b_cancel"),
            Button("Confirmer", variant="success", id="b_confirm"),
            id="IN_dialog"
        )
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "b_confirm":
            self.app.exit() # --> vers sortie du RM6 dans la base
        else:
            self.app.pop_screen() # --> Annule le dernier scan



TEXT = """I must not fear.
Fear is the mind-killer.
Fear is the little-death that brings total obliteration.
I will face my fear.
I will permit it to pass over me and through me.
And when it has gone past, I will turn the inner eye to see its path.
Where the fear has gone there will be nothing. Only I will remain."""

ROWS = [
    ("lane", "swimmer", "country", "time"),
    (4, "Joseph Schooling", "Singapore", 50.39),
    (2, "Michael Phelps", "United States", 51.14),
    (5, "Chad le Clos", "South Africa", 51.14),
    (6, "László Cseh", "Hungary", 51.14),
    (3, "Li Zhuhao", "China", 51.26),
    (8, "Mehdy Metella", "France", 51.58),
    (7, "Tom Shields", "United States", 51.73),
    (1, "Aleksandr Sadovnikov", "Russia", 51.84),
    (10, "Darren Burns", "Scotland", 51.84),
]


class ModalApp(App):
    """An app with a modal dialog."""

    CSS_PATH = f'{os.getcwd()}\styles\main.css'
    BINDINGS = [("q", "request_quit", "Quit"),("a", "request_ok", "ok")]
    optionValue = ""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Grid(
            Grid(
                Label("[bold #90EE90]Scan your RM6 :[/bold #90EE90]", id="MainTitle"),
                Input(),
                id="scanner"
            ),
            Label("lool", id="testing"),
            DataTable(),
            id="main"
        )
        yield Footer()
        
    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.cursor_type = "none"
        table.zebra_stripes = True

        for col in ROWS[0]:
            table.add_column(Text(str(col), justify="center"))
        
        # table.add_rows(ROWS[1:])
        for row in ROWS[1:]:
            # Adding styled and justified `Text` objects instead of plain strings.
            styled_row = [
                Text(str(cell), style="#008000", justify="left") for cell in row
            ]
            table.add_row(*styled_row)

    @on(OptionList.OptionSelected)
    def update_option_value(self, event : OptionList.OptionSelected) -> None:
        self.optionValue = str(event.option_id)

    def action_request_quit(self):
        """Action to display the quit dialog."""
        self.push_screen(OutputPopUpScreen(self.optionValue, "storage1"))
        
    def action_request_ok(self) -> None:
        """Action to display the quit dialog."""
        self.push_screen(InputPopUpScreen(self.optionValue, "storage1", ["c1","c2","c3"]))

if __name__ == "__main__":
    app = ModalApp()
    app.run()
    
    
    
    
    
    
    
    
    
    
    
    
    
#     # Written with Textual 0.44.1

# from textual import on
# from textual.app import App, ComposeResult
# from textual.screen import Screen
# from textual.widgets import Button, Label


# class ScreenA(Screen):
#     def compose(self) -> ComposeResult:
#         yield Label("This is screen A")
#         yield Button("Push A", id="a")
#         yield Button("Push B", id="b")
#         yield Button("Pop", id="pop")
#         yield Button("Switch to B", id="switch")


# class ScreenB(Screen):
#     def compose(self) -> ComposeResult:
#         yield Label("This is screen B")
#         yield Button("Push A", id="a")
#         yield Button("Push B", id="b")
#         yield Button("Pop", id="pop")


# class ScreensApp(App[None]):
#     SCREENS = {
#         "a": ScreenA(),
#         "b": ScreenB(),
#     }

#     def compose(self) -> ComposeResult:
#         yield Label("This is the base screen!")
#         yield Button("Push A", id="a")
#         yield Button("Push B", id="b")

#     @on(Button.Pressed, "#pop")
#     def pop_top_screen(self) -> None:
#         self.pop_screen()
#         print(self.screen_stack)

#     @on(Button.Pressed, "#a, #b")
#     def push(self, event: Button.Pressed) -> None:
#         self.push_screen(event.button.id)
#         print(self.screen_stack)

#     @on(Button.Pressed, "#switch")
#     def switch(self) -> None:
#         self.switch_screen("b")
#         print(self.screen_stack)


# app = ScreensApp()
# if __name__ == "__main__":
#     app.run()