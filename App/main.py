#  1. Main Application Entry Point (main.py)
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.lang import Builder
from screens.home_screen import HomeScreen
from screens.editor_screen import EditorScreen
from screens.settings_screen import SettingsScreen
from screens.share_screen import ShareScreen
from utils.database import DatabaseManager
from services.cloud_service import GoogleDriveService
from services.storage_service import StorageService

class NotesApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        
        # Initialize services
        self.db = DatabaseManager()
        self.storage = StorageService(self.db)
        self.cloud = GoogleDriveService()
        
        # Create screen manager
        self.sm = ScreenManager()
        
        # Add screens
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(EditorScreen(name='editor'))
        self.sm.add_widget(SettingsScreen(name='settings'))
        self.sm.add_widget(ShareScreen(name='share'))
        
        return self.sm

    def on_start(self):
        # Initialize database
        self.db.create_tables()
        # Sync with cloud if possible
        self.cloud.sync_notes()

if __name__ == '__main__':
    NotesApp().run()