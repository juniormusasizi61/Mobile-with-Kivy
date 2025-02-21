# utils/database.py

import sqlite3
from datetime import datetime
import os

class DatabaseManager:
    """
    Handles all database operations for the Notes application.
    Uses SQLite as the backend database engine for local storage.
    
    The database stores notes with their metadata and user settings.
    """
    def __init__(self):
        """
        Initializes the database connection and ensures the database directory exists.
        Creates a new database file if it doesn't exist.
        """
        # Create the data directory if it doesn't exist
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        os.makedirs(data_dir, exist_ok=True)
        
        # Set up the database file path
        self.db_path = os.path.join(data_dir, 'notes.db')
        
        # Initialize the database connection
        self.connection = None
        self.cursor = None
        
        # Establish the initial connection
        self.connect()

    def connect(self):
        """
        Establishes a connection to the SQLite database.
        Creates a new connection if one doesn't exist.
        """
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            raise Exception(f"Failed to connect to database: {str(e)}")

    def create_tables(self):
        """
        Creates all necessary database tables if they don't exist.
        This includes tables for notes, settings, and sync metadata.
        """
        try:
            # Create the notes table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_deleted BOOLEAN DEFAULT 0,
                    sync_status TEXT DEFAULT 'not_synced'
                )
            ''')
            
            # Create the settings table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create the sync_metadata table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS sync_metadata (
                    note_id INTEGER PRIMARY KEY,
                    cloud_id TEXT,
                    last_synced TIMESTAMP,
                    FOREIGN KEY (note_id) REFERENCES notes (id)
                )
            ''')
            
            self.connection.commit()
        except sqlite3.Error as e:
            raise Exception(f"Failed to create database tables: {str(e)}")

    def save_note(self, title, content, note_id=None):
        """
        Saves a note to the database. Creates a new note if note_id is None,
        otherwise updates the existing note.
        
        Args:
            title (str): The title of the note
            content (str): The content of the note
            note_id (int, optional): The ID of the note to update
            
        Returns:
            int: The ID of the saved note
        """
        try:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            if note_id is None:
                # Create new note
                self.cursor.execute('''
                    INSERT INTO notes (title, content, created_at, updated_at)
                    VALUES (?, ?, ?, ?)
                ''', (title, content, current_time, current_time))
                note_id = self.cursor.lastrowid
            else:
                # Update existing note
                self.cursor.execute('''
                    UPDATE notes
                    SET title = ?, content = ?, updated_at = ?
                    WHERE id = ?
                ''', (title, content, current_time, note_id))
            
            self.connection.commit()
            return note_id
        except sqlite3.Error as e:
            raise Exception(f"Failed to save note: {str(e)}")

    def get_note(self, note_id):
        """
        Retrieves a specific note from the database.
        
        Args:
            note_id (int): The ID of the note to retrieve
            
        Returns:
            dict: The note data or None if not found
        """
        try:
            self.cursor.execute('''
                SELECT id, title, content, created_at, updated_at
                FROM notes
                WHERE id = ? AND is_deleted = 0
            ''', (note_id,))
            
            row = self.cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'title': row[1],
                    'content': row[2],
                    'created_at': row[3],
                    'updated_at': row[4]
                }
            return None
        except sqlite3.Error as e:
            raise Exception(f"Failed to retrieve note: {str(e)}")

    def get_all_notes(self):
        """
        Retrieves all non-deleted notes from the database.
        
        Returns:
            list: List of dictionaries containing note data
        """
        try:
            self.cursor.execute('''
                SELECT id, title, content, created_at, updated_at
                FROM notes
                WHERE is_deleted = 0
                ORDER BY updated_at DESC
            ''')
            
            notes = []
            for row in self.cursor.fetchall():
                notes.append({
                    'id': row[0],
                    'title': row[1],
                    'content': row[2],
                    'created_at': row[3],
                    'updated_at': row[4]
                })
            return notes
        except sqlite3.Error as e:
            raise Exception(f"Failed to retrieve notes: {str(e)}")

    def delete_note(self, note_id):
        """
        Soft deletes a note by marking it as deleted in the database.
        
        Args:
            note_id (int): The ID of the note to delete
        """
        try:
            self.cursor.execute('''
                UPDATE notes
                SET is_deleted = 1, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (note_id,))
            self.connection.commit()
        except sqlite3.Error as e:
            raise Exception(f"Failed to delete note: {str(e)}")

    def get_setting(self, key):
        """
        Retrieves a setting value from the database.
        
        Args:
            key (str): The setting key to retrieve
            
        Returns:
            str: The setting value or None if not found
        """
        try:
            self.cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            raise Exception(f"Failed to retrieve setting: {str(e)}")

    def save_setting(self, key, value):
        """
        Saves a setting to the database.
        
        Args:
            key (str): The setting key
            value (str): The setting value
        """
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO settings (key, value, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            ''', (key, value))
            self.connection.commit()
        except sqlite3.Error as e:
            raise Exception(f"Failed to save setting: {str(e)}")

    def __del__(self):
        """
        Ensures the database connection is properly closed when the object is destroyed.
        """
        if self.connection:
            self.connection.close()