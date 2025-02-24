# main.py

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDButton
from kivymd.uix.button import MDFlatButton
# Import screen classes
from screens.home_screen import HomeScreen
from screens.editor_screen import EditorScreen
from screens.settings_screen import SettingsScreen
from screens.share_screen import ShareScreen

# Import services
from utils.database import DatabaseManager
from services.cloud_service import GoogleDriveService
from services.storage_service import StorageService

import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


# Remove or comment out the global initialization:
# storage = StorageService()

class NotesApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = None
        self.db = None
        self.storage = None
        self.cloud = None
        Window.size = (400, 600)
        Window.minimum_width = 300
        Window.minimum_height = 400

    def initialize_services(self):
        try:
            self.db = DatabaseManager()
            self.storage = StorageService(self.db)  # Pass the database instance here
            self.cloud = GoogleDriveService()
        except Exception as e:
            raise Exception(f"Failed to initialize services: {str(e)}")


class NotesApp(MDApp):
    """
    Main application class that handles initialization and lifecycle management.
    This enhanced version includes proper error handling and screen management.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize class variables
        self.sm = None
        self.db = None
        self.storage = None
        self.cloud = None
        
        # Set initial window size and minimum dimensions
        Window.size = (400, 600)  # Default size for mobile-like experience
        Window.minimum_width = 300
        Window.minimum_height = 400

    def build(self):
        """
        Builds and returns the application's root widget.
        Includes error handling for service initialization.
        """
        try:
            # Set theme properties
            self.theme_cls.primary_palette = "Blue"
            self.theme_cls.theme_style = "Light"
            self.theme_cls.accent_palette = "Teal"
            
            # Initialize services with error handling
            self.initialize_services()
            
            # Create and configure screen manager
            self.sm = ScreenManager()
            self.load_screens()
            
            # Schedule a check for first-time setup
            Clock.schedule_once(self.check_first_time_setup, 0)
            
            return self.sm
            
        except Exception as e:
            self.show_error_dialog(f"Error during app initialization: {str(e)}")
            return ScreenManager()  # Return empty manager to prevent crash

    def initialize_services(self):
        """
        Initializes all required services with proper error handling.
        """
        try:
            self.db = DatabaseManager()
            self.storage = StorageService(self.db)
            self.cloud = GoogleDriveService()
        except Exception as e:
            raise Exception(f"Failed to initialize services: {str(e)}")

    def load_screens(self):
        """
        Adds all application screens to the screen manager.
        Uses try-except to handle potential import or initialization errors.
        """
        screens = {
            'home': HomeScreen,
            'editor': EditorScreen,
            'settings': SettingsScreen,
            'share': ShareScreen
        }
        
        for name, screen_class in screens.items():
            try:
                screen = screen_class(name=name)
                self.sm.add_widget(screen)
            except Exception as e:
                self.show_error_dialog(f"Error loading {name} screen: {str(e)}")

    def on_start(self):
        """
        Handles initialization tasks after the application window is displayed.
        Includes database setup and initial cloud sync.
        """
        try:
            # Create database tables if they don't exist
            self.db.create_tables()
            
            # Attempt cloud sync in a separate thread to prevent UI freezing
            Clock.schedule_once(self.delayed_cloud_sync, 1)
        except Exception as e:
            self.show_error_dialog(f"Error during startup: {str(e)}")

    def delayed_cloud_sync(self, dt):
        """
        Performs cloud synchronization after a delay to ensure smooth startup.
        """
        try:
            self.cloud.sync_notes()
        except Exception as e:
            self.show_error_dialog(f"Cloud sync failed: {str(e)}")

    def check_first_time_setup(self, dt):
        """
        Checks if this is the first time running the app and shows setup dialog if needed.
        """
        if not self.storage.get_setting('first_time_setup_complete'):
            self.show_welcome_dialog()
            self.storage.save_setting('first_time_setup_complete', True)

    def show_welcome_dialog(self):
        """
        Displays a welcome dialog for first-time users.
        """
        dialog = MDDialog(
            title="Welcome to Notes App!",
            text="Thank you for installing Notes App. Would you like to take a quick tour?",
            buttons=[
                MDButton(
                    text="Skip",
                    on_press=lambda x: dialog.dismiss()
                ),
                MDButton(
                    text="Take Tour",
                    on_press=lambda x: self.start_app_tour()
                )
            ]
        )
        dialog.open()

    def show_error_dialog(self, message):
        """
        Displays an error dialog with the given message.
        """
        dialog = MDDialog(
            title="Error",
            text=message,
            buttons=[
                MDButton(
                    text="OK",
                    on_press=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def start_app_tour(self):
        """
        Initiates the application tour for new users.
        """
        # Switch to home screen and start the tour
        self.sm.current = 'home'
        if hasattr(self.sm.get_screen('home'), 'start_tour'):
            self.sm.get_screen('home').start_tour()

if __name__ == '__main__':
    NotesApp().run()