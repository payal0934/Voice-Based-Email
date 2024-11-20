import threading
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.clock import Clock
import warnings
from text_speech import *
from login_page import activity_area
from login_page import login_area
from kivy.core.window import Window
import sys
print(sys.path)
# warnings.filterwarnings('ignore', category='FutureWarnings')
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)
# warnings.filterwarnings('ignore', category='UserWarning')
# warnings.simplefilter(action='ignore', category=UserWarning)  # Ignore UserWarning
# Your code that might raise a UserWarning
# warnings.resetwarnings()  # Recover from ignoring UserWarning

Window.size = (310, 500)

Builder.load_string("""
<ComposeScreen>
    name: "compose"
    Screen:
        MDNavigationLayout:
            ScreenManager:
                Screen:
                    BoxLayout:
                        orientation: "vertical"
                        MDTopAppBar:
                            
                            elevation: 2
                        Widget:
                            MDNavigationDrawer:
                                id: nav_drawer
        MDRoundFlatButton:
            text: "Sender Email"
            font_size: "20sp"
            size_hint: (.6, .02)
            pos_hint: {"center_x": .5,"center_y": .25}
            theme_text_color: "Custom"
            text_color: [1, 1, 1, 1]
            md_bg_color: (0, 0, 1, 1) 
        MDRoundFlatButton:
            text: "Subject"
            font_size: "20sp"
            size_hint: (.6, .02)
            pos_hint: {"center_x": .5,"center_y": .25}
            theme_text_color: "Custom"
            text_color: [1, 1, 1, 1]
            md_bg_color: (0, 0, 1, 1) 
        MDRoundFlatButton:
            text: "Body of the Mail"
            font_size: "20sp"
            size_hint: (.6, .02)
            pos_hint: {"center_x": .5,"center_y": .25}
            theme_text_color: "Custom"
            text_color: [1, 1, 1, 1]
            md_bg_color: (0, 0, 1, 1) 

<loginScreen>
    name: "login"
   
    MDFloatLayout:
        md_bg_color: 1,1,1,1
        
        MDLabel:
            text: "W E L C O M E !"
           
            font_size: "26sp"
            pos_hint_x: .5
            pos_hint: { 'center_x': .48,'center_y': .90}
            halign: "center"
            color: rgba(0, 0, 59, 255)
        
        Image: 
            source: "eye.jpg"
            pos_hint: {'center_x': .53, 'center_y': .60}
            size_hint: .9, .9

        MDRoundFlatButton:
            text: "Email"
            font_size: "20sp"
            size_hint: (.4, .05)
            pos_hint: {"center_x": .5,"center_y": .30}
        MDRoundFlatButton:
            text: "Password"
            font_size: "20sp"
            pos_hint: {"center_x": .5,"center_y": .20}
        
               
<MainScreen>:
    name: "main"
    Screen:
        MDNavigationLayout:
            ScreenManager:
                Screen:
                    BoxLayout:
                        orientation: "vertical"
                        MDTopAppBar:
                            
                            elevation: 2
                        Widget:
                            MDNavigationDrawer:
                                id: nav_drawer
               
        MDLabel:
            text: "Menu Page"
            font_size: "23sp"
            pos_hint: {'center_y': .80}
            halign: "center"
            color: rgba(10, 40, 30, 255)                        
        MDRoundFlatButton:
            text: "Compose"
            font_size: "20sp"
            size_hint: (.5, .05)
            pos_hint: {"center_x": .5,"center_y": .65}
            theme_text_color: "Custom"
            text_color: [1, 1, 1, 1]
            md_bg_color: (0, 0, 1, 1 )
        MDRoundFlatButton:
            text: "Inbox"
            font_size: "20sp"
            size_hint: (.5, .05)
            pos_hint: {"center_x": .5,"center_y": .55}
            theme_text_color: "Custom"
            text_color: [1, 1, 1, 1]
            md_bg_color: (0, 0, 1, 1)
        MDRoundFlatButton:
            text: "Sent"
            font_size: "20sp"
            size_hint: (.5, .02)
            pos_hint: {"center_x": .5,"center_y": .45}
            theme_text_color: "Custom"
            text_color: [1, 1, 1, 1]
            md_bg_color: (0, 0, 1, 1) 
        MDRoundFlatButton:
            text: "Trash"
            font_size: "20sp"
            size_hint: (.5, .02)
            pos_hint: {"center_x": .5,"center_y": .35}
            theme_text_color: "Custom"
            text_color: [1, 1, 1, 1]
            md_bg_color: (0, 0, 1, 1)
        MDRoundFlatButton:
            text: "Logout"
            font_size: "20sp"
            size_hint: (.5, .02)
            pos_hint: {"center_x": .5,"center_y": .25}
            theme_text_color: "Custom"
            text_color: [1, 1, 1, 1]
            md_bg_color: (0, 0, 1, 1) 
            
""")

sm = ScreenManager()

        
class MainScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.speak_text, 0)
        

    def speak_text(self, dt):
        activity_area()

    def on_touch_down(self, touch):
        # Create and switch to the next screen
        app = MDApp.get_running_app()
        app.root.switch_to(LoginScreen()) 
    

class LoginScreen(Screen):
    def on_enter(self):
        self.t = threading.Thread(target=self.speak_text)
        self.t.start()

    def speak_text(self):
        login_area()
        

    def on_touch_down(self, touch):
        # Create and switch to the next screen
        app = MDApp.get_running_app()
        app.root.switch_to(MainScreen())
    


class VoiceApp(MDApp):
    def build(self):
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))
        return sm




if __name__ == '__main__':
    VoiceApp().run()
