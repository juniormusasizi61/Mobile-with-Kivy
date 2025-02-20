# screens/home_screen.py
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList
from kivymd.uix.button import MDFabButton
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp

class NoteListItem(MDCard):
    def __init__(self, note, **kwargs):
        super().__init__(**kwargs)
        self.note = note
        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = "100dp"
        self.padding = "8dp"
        self.md_bg_color = [1, 1, 1, 1]  # white
        self.radius = [8]
        self.elevation = 1
        
        # Create layout for content
        box = MDBoxLayout(
            orientation="vertical",
            spacing="4dp",
            padding="8dp"
        )
        
        # Add title
        title = MDLabel(
            text=note.title,
            bold=True,
            font_style="H6",
            size_hint_y=None,
            height="24dp"
        )
        
        # Add content preview
        content = MDLabel(
            text=note.content[:50] + "..." if len(note.content) > 50 else note.content,
            size_hint_y=None,
            height="24dp"
        )
        
        # Add date
        date = MDLabel(
            text=note.updated_at.strftime("%Y-%m-%d %H:%M"),
            theme_text_color="Secondary",
            size_hint_y=None,
            height="20dp"
        )
        
        # Add all elements to box layout
        box.add_widget(title)
        box.add_widget(content)
        box.add_widget(date)
        
        # Add box layout to card
        self.add_widget(box)

class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()
    
    def setup_ui(self):
        # Create main layout
        self.layout = MDBoxLayout(
            orientation="vertical",
            spacing="8dp",
            padding="8dp"
        )
        
        # Create notes list with scrolling
        self.notes_list = MDList(
            spacing="8dp",
            padding="8dp",
            size_hint_y=None
        )
        self.notes_list.bind(minimum_height=self.notes_list.setter('height'))
        
        # Add list to layout
        self.layout.add_widget(self.notes_list)
        
        # Add layout to screen
        self.add_widget(self.layout)
        
        # Add FAB for new note
        fab = MDFabButton(
            icon="plus",
            pos_hint={'right': 0.95, 'bottom': 0.05}
        )
        fab.bind(on_press=self.new_note)
        self.add_widget(fab)
    
    def new_note(self, instance):
        self.parent.current = 'editor'
    
    def refresh_notes(self):
        self.notes_list.clear_widgets()
        app = MDApp.get_running_app()
        notes = app.storage.get_all_notes()
        for note in notes:
            item = NoteListItem(note)
            item.bind(on_press=lambda x, note=note: self.open_note(note))
            self.notes_list.add_widget(item)
    
    def open_note(self, note):
        editor_screen = self.parent.get_screen('editor')
        editor_screen.current_note = note
        editor_screen.title_field.text = note.title
        editor_screen.content_field.text = note.content
        self.parent.current = 'editor'