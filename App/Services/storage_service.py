# services/storage_service.py
import json
import os
from datetime import datetime

class StorageService:
    def __init__(self, db):
        self.db = db
        # Initialize with a base directory for storing data
        self.base_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        self.ensure_storage_directory()
    
    def ensure_storage_directory(self):
        """Creates the storage directory if it doesn't exist"""
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)
    
    def store_data(self, key, data):
        """
        Stores data in a JSON file with the given key
        Args:
            key (str): Identifier for the data
            data (dict): Data to store
        """
        # Add metadata to track when the data was stored
        data_with_metadata = {
            'timestamp': datetime.now().isoformat(),
            'content': data
        }
        
        file_path = os.path.join(self.base_dir, f"{key}.json")
        with open(file_path, 'w') as f:
            json.dump(data_with_metadata, f, indent=4)
            
    def retrieve_data(self, key):
        """
        Retrieves data stored under the given key
        Args:
            key (str): Identifier for the data
        Returns:
            dict: The stored data, or None if not found
        """
        file_path = os.path.join(self.base_dir, f"{key}.json")
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                return data['content']
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            return None
            
    def list_stored_items(self):
        """Returns a list of all stored item keys"""
        files = os.listdir(self.base_dir)
        return [os.path.splitext(f)[0] for f in files if f.endswith('.json')]
        
    def delete_data(self, key):
        """
        Deletes data stored under the given key
        Args:
            key (str): Identifier for the data to delete
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        file_path = os.path.join(self.base_dir, f"{key}.json")
        try:
            os.remove(file_path)
            return True
        except FileNotFoundError:
            return False