# screens/share_screen.py
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import button
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp

class ShareScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_note = None
        self.dialog = None
        self.setup_ui()
    
    def setup_ui(self):
        # Create main layout
        layout = MDBoxLayout(
            orientation='vertical',
            spacing="20dp",
            padding="16dp"
        )
        
        # Social media sharing buttons
        facebook_btn = button(
            text="Share to Facebook",
            style="filled",
            size_hint_x=0.8,
            pos_hint={'center_x': 0.5}
        )
        facebook_btn.bind(on_press=self.share_to_facebook)
        
        twitter_btn = button(
            text="Share to X (Twitter)",
            style="filled",
            size_hint_x=0.8,
            pos_hint={'center_x': 0.5}
        )
        twitter_btn.bind(on_press=self.share_to_twitter)
        
        instagram_btn = button(
            text="Share to Instagram",
            style="filled",
            size_hint_x=0.8,
            pos_hint={'center_x': 0.5}
        )
        instagram_btn.bind(on_press=self.share_to_instagram)
        
        # Back button
        back_btn = button(
            text="Back",
            style="outlined",
            size_hint_x=0.8,
            pos_hint={'center_x': 0.5}
        )
        back_btn.bind(on_press=self.go_back)
        
        # Add buttons to layout
        layout.add_widget(MDBoxLayout(size_hint_y=0.3))  # Spacing at top
        layout.add_widget(facebook_btn)
        layout.add_widget(twitter_btn)
        layout.add_widget(instagram_btn)
        layout.add_widget(MDBoxLayout(size_hint_y=0.3))  # Spacing in middle
        layout.add_widget(back_btn)
        
        # Add layout to screen
        self.add_widget(layout)
    
    def share_to_facebook(self, instance):
        if not self.current_note:
            self.show_error_dialog("No note selected")
            return
        
        app = MDApp.get_running_app()
        try:
            app.social.share_to_facebook(self.current_note)
            self.show_success_dialog("Shared to Facebook successfully!")
        except Exception as e:
            self.show_error_dialog(str(e))
    
    def share_to_twitter(self, instance):
        if not self.current_note:
            self.show_error_dialog("No note selected")
            return
        
        app = MDApp.get_running_app()
        try:
            app.social.share_to_twitter(self.current_note)
            self.show_success_dialog("Shared to X (Twitter) successfully!")
        except Exception as e:
            self.show_error_dialog(str(e))
    
    def share_to_instagram(self, instance):
        if not self.current_note:
            self.show_error_dialog("No note selected")
            return
        
        app = MDApp.get_running_app()
        try:
            app.social.share_to_instagram(self.current_note)
            self.show_success_dialog("Shared to Instagram successfully!")
        except Exception as e:
            self.show_error_dialog(str(e))
    
    def show_success_dialog(self, message):
        if self.dialog:
            self.dialog.dismiss()
        
        self.dialog = MDDialog(
            title="Success",
            text=message,
            buttons=[
                button(
                    text="OK",
                    style="text",
                    on_press=lambda x: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()
    
    def show_error_dialog(self, message):
        if self.dialog:
            self.dialog.dismiss()
        
        self.dialog = MDDialog(
            title="Error",
            text=message,
            buttons=[
                button(
                    text="OK",
                    style="text",
                    on_press=lambda x: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()
    
    def go_back(self, instance):
        self.parent.current = 'home'