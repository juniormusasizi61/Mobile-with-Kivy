# screens/editor_screen.py
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp

class EditorScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_note = None
        self.setup_ui()
    
    def setup_ui(self):
        # Create main layout
        layout = MDBoxLayout(
            orientation='vertical',
            spacing="10dp",
            padding="16dp"
        )
        
        # Title field
        self.title_field = MDTextField(
            hint_text="Note Title",
            mode="rectangle",
            size_hint_y=None,
            height="48dp"
        )
        layout.add_widget(self.title_field)
        
        # Content field
        self.content_field = MDTextField(
            hint_text="Note Content",
            mode="rectangle",
            multiline=True,
            size_hint_y=None,
            height="300dp"  # Adjust this value as needed
        )
        layout.add_widget(self.content_field)
        
        # Buttons layout
        button_layout = MDBoxLayout(
            orientation='horizontal',
            spacing="10dp",
            size_hint_y=None,
            height="48dp",
            padding=["0dp", "20dp", "0dp", "0dp"]  # top padding for spacing
        )
        
        # Save button
        save_button = MDButton(
            text="Save",
            style="filled",
            size_hint_x=0.5
        )
        save_button.bind(on_press=self.save_note)
        
        # Cancel button
        cancel_button = MDButton(
            text="Cancel",
            style="outlined",
            size_hint_x=0.5
        )
        cancel_button.bind(on_press=self.cancel_edit)
        
        # Add buttons to button layout
        button_layout.add_widget(cancel_button)
        button_layout.add_widget(save_button)
        
        # Add button layout to main layout
        layout.add_widget(button_layout)
        
        # Add main layout to screen
        self.add_widget(layout)
    
    def save_note(self, instance):
        from models.note import Note
        
        note = Note(
            title=self.title_field.text,
            content=self.content_field.text,
            id=self.current_note.id if self.current_note else None
        )
        
        app = MDApp.get_running_app()
        app.storage.save_note(note)
        
        # Try to upload to cloud if available
        try:
            app.cloud.upload_note(note)
        except:
            pass  # Handle cloud upload failure gracefully
        
        self.clear_fields()
        self.parent.current = 'home'
        self.parent.get_screen('home').refresh_notes()
    
    def cancel_edit(self, instance):
        self.clear_fields()
        self.parent.current = 'home'
    
    def clear_fields(self):
        self.title_field.text = ""
        self.content_field.text = ""
        self.current_note = None
    
    def on_pre_enter(self):
        """Called before the screen is displayed"""
        if self.current_note:
            self.title_field.text = self.current_note.title
            self.content_field.text = self.current_note.content