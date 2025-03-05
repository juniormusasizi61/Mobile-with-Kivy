"""
NotesApp - A cross-platform note-taking application built with KivyMD

This package initializes the NotesApp application and its components.
The application provides note creation, editing, sharing, and cloud synchronization.
"""

__version__ = '1.0.0'
__author__ = 'Your Name'

# Import main application class for easy access
from .main import NotesApp

# Import screens for direct access
from .screens.home_screen import HomeScreen
from .screens.editor_screen import EditorScreen
from .screens.settings_screen import SettingsScreen
from .screens.share_screen import ShareScreen

# Import utility and service modules
from .utils.database import DatabaseManager
from .services.cloud_service import GoogleDriveService
from .services.storage_service import StorageService

# Setup package-level logging configuration
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())

# Define what gets imported with "from notesapp import *"
__all__ = [
    'NotesApp',
    'HomeScreen',
    'EditorScreen',
    'SettingsScreen',
    'ShareScreen',
    'DatabaseManager',
    'GoogleDriveService',
    'StorageService',
]
