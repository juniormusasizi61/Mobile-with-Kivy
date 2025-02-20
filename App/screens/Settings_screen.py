# screens/settings_screen.py

# Import necessary KivyMD components for building the UI
from kivymd.uix.screen import MDScreen  # Base screen class
from kivymd.uix.list import MDList      # Container for list items
from kivymd.uix.card import MDCard      # Material Design card component
from kivymd.uix.boxlayout import MDBoxLayout  # Layout manager for arranging widgets
from kivymd.uix.button import MDButton  # Material Design button
from kivymd.uix.label import MDLabel    # Text display widget
from kivymd.app import MDApp            # Main application class

class SettingsItem(MDCard):
    """
    Custom widget for each settings option. We use MDCard instead of the older
    OneLineIconListItem for better customization and modern Material Design appearance.
    
    Each settings item is a card that contains:
    - Text label for the setting name
    - Touch functionality for interaction
    - Consistent styling with elevation and rounded corners
    """
    def __init__(self, icon_name, text, on_press=None, **kwargs):
        # Call parent class constructor
        super().__init__(**kwargs)
        
        # Configure the card's appearance
        self.size_hint_y = None         # Don't expand to fill vertical space
        self.height = "60dp"            # Fixed height for consistency
        self.padding = "8dp"            # Internal padding for content
        self.md_bg_color = [1, 1, 1, 1] # White background
        self.radius = [8]               # Rounded corners
        self.elevation = 1              # Subtle shadow for depth
        
        # Create a horizontal layout to arrange the contents
        layout = MDBoxLayout(
            orientation="horizontal",    # Arrange items left to right
            spacing="12dp",             # Space between items
            padding="8dp"               # Padding around contents
        )
        
        # Create the text label for this setting
        label = MDLabel(
            text=text,                  # The setting name
            theme_text_color="Primary"  # Use the theme's primary text color
        )
        
        # Add the label to our horizontal layout
        layout.add_widget(label)
        
        # Add the completed layout to our card
        self.add_widget(layout)
        
        # Set up the touch handler if one was provided
        if on_press:
            self.bind(on_press=on_press)

class SettingsScreen(MDScreen):
    """
    The main settings screen of the application. This screen provides various
    configuration options for the user, including theme selection, cloud sync,
    and other preferences.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()  # Initialize the user interface
    
    def setup_ui(self):
        """
        Creates and arranges all the UI elements for the settings screen.
        Uses a vertical layout to stack elements from top to bottom.
        """
        # Create the main container for all our settings elements
        main_layout = MDBoxLayout(
            orientation="vertical",      # Stack items top to bottom
            spacing="16dp",             # Space between items
            padding="16dp"              # Padding around all content
        )
        
        # Add a title at the top of the screen
        title = MDLabel(
            text="Settings",
            font_style="H5",            # Large, prominent text
            size_hint_y=None,           # Fixed height
            height="48dp"
        )
        main_layout.add_widget(title)
        
        # Create a scrollable list to hold our settings items
        settings_list = MDList(
            spacing="8dp",              # Space between settings items
            size_hint_y=None            # Height will be set by contents
        )
        # Make the list scrollable by binding its minimum height
        settings_list.bind(minimum_height=settings_list.setter('height'))
        
        # Add theme toggle setting
        theme_item = SettingsItem(
            icon_name="theme-light-dark",
            text="Toggle Dark/Light Theme",
            on_press=self.toggle_theme  # Function to call when pressed
        )
        settings_list.add_widget(theme_item)
        
        # Add cloud sync setting
        sync_item = SettingsItem(
            icon_name="cloud-sync",
            text="Sync with Cloud",
            on_press=self.sync_with_cloud
        )
        settings_list.add_widget(sync_item)
        
        # Add cloud account management setting
        account_item = SettingsItem(
            icon_name="account",
            text="Cloud Account Settings",
            on_press=self.manage_cloud_account
        )
        settings_list.add_widget(account_item)
        
        # Add notification preferences setting
        notifications_item = SettingsItem(
            icon_name="bell",
            text="Notification Settings",
            on_press=self.manage_notifications
        )
        settings_list.add_widget(notifications_item)
        
        # Add the completed settings list to the main layout
        main_layout.add_widget(settings_list)
        
        # Add a back button at the bottom of the screen
        back_button = MDButton(
            text="Back to Home",
            style="outlined",           # Outlined style for secondary action
            size_hint_x=0.8,           # 80% of screen width
            pos_hint={'center_x': 0.5}  # Center horizontally
        )
        back_button.bind(on_press=self.go_back)
        main_layout.add_widget(back_button)
        
        # Add the completed main layout to the screen
        self.add_widget(main_layout)
    
    def toggle_theme(self, instance):
        """
        Switches between light and dark theme for the entire application.
        This change is immediate and affects all screens.
        """
        app = MDApp.get_running_app()
        # If current theme is Light, switch to Dark, and vice versa
        app.theme_cls.theme_style = (
            "Dark" if app.theme_cls.theme_style == "Light" else "Light"
        )
    
    def sync_with_cloud(self, instance):
        """
        Initiates synchronization with the cloud service.
        Shows success or error message based on the result.
        """
        app = MDApp.get_running_app()
        try:
            app.cloud.sync_notes()
            self.show_message("Sync completed successfully!")
            # Update the home screen to show any changes from sync
            self.parent.get_screen('home').refresh_notes()
        except Exception as e:
            self.show_message(f"Sync failed: {str(e)}", is_error=True)
    
    def manage_cloud_account(self, instance):
        """
        Placeholder for cloud account management functionality.
        Currently just shows a message about future implementation.
        """
        self.show_message("Cloud account management coming soon!")
    
    def manage_notifications(self, instance):
        """
        Placeholder for notification settings functionality.
        Currently just shows a message about future implementation.
        """
        self.show_message("Notification settings coming soon!")
    
    def show_message(self, text, is_error=False):
        """
        Displays a dialog box with a message to the user.
        Used for both success and error messages.
        
        Args:
            text (str): The message to display
            is_error (bool): Whether this is an error message (affects title)
        """
        from kivymd.uix.dialog import MDDialog
        
        dialog = MDDialog(
            title="Error" if is_error else "Success",
            text=text,
            buttons=[
                MDButton(
                    text="OK",
                    style="text",
                    on_press=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()
    
    def go_back(self, instance):
        """
        Returns to the home screen when the back button is pressed.
        """
        self.parent.current = 'home'