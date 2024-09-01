from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.clock import Clock
import mysql.connector
import random
import string
import qrcode

class BackgroundScreen(Screen):
    pass

class BackgroundScreen1(Screen):
    pass

class BackgroundScreen2(Screen):
    pass

class LoginScreen(BackgroundScreen):
    def __init__(self, **kwargs):
        super(LoginScreen,self).__init__(**kwargs)
        self.layout1=GridLayout(cols=1,pos_hint={"center_y":0.25})
        self.layout= BoxLayout(orientation="vertical",spacing=10,padding=[300])
        self.txt1=TextInput(hint_text="Username",background_color=(1,1,1,0.5))
        self.txt2= TextInput(hint_text="Password",password="True",background_color=(1,1,1,0.5))
        self.btn= Button(text="Login",on_press=self.login)
        self.btn2= Button(text="Register",on_press=self.create_account)

        self.layout.add_widget(self.txt1)
        self.layout.add_widget(self.txt2)
        self.layout.add_widget(self.btn)
        self.layout.add_widget(self.btn2)

        #self.add_widget(self.layout)
        self.layout1.add_widget(self.layout)
        self.add_widget(self.layout1)
    
    def login(self, instance):
        username = self.txt1.text
        password= self.txt2.text
        db= None
        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Jojsafari_25",
                database="credentials"
            )
            cursor=db.cursor()

            query = "SELECT * FROM log_in WHERE username=%s AND password=%s"
            values = (username, password)
            cursor.execute(query, values)
            result = cursor.fetchone()

            if result:
                self.manager.current = "display"
            else:
                raise ValueError("Invalid username or password")
        
        except Exception as e:
            popup = Popup(title='Login Failed',
                          content=Label(text=str(e)),
                          size_hint=(None, None), size=(400, 200))
            popup.open()

        finally:
            if db is not None:
                cursor.close()
                db.close()    
    def create_account(self,instance):
        self.manager.current="create_account"

class CreateaccuntScreen(BackgroundScreen1):
    def __init__(self, **kwargs):
        super(CreateaccuntScreen,self).__init__(**kwargs) 
        self.layout1=GridLayout(cols=1,pos_hint={"center_y":0.25})
        self.layout= BoxLayout(orientation="vertical",spacing=10,padding=[200])
        self.inp1=TextInput(hint_text="Enter your Name",background_color=(1,1,1,0.4))
        self.inp2=TextInput(hint_text="Enter your UID",background_color=(1,1,1,0.4))
        self.inp3=TextInput(hint_text="Enter your Section",background_color=(1,1,1,0.4))
        self.inp4=TextInput(hint_text="Enter your Username",background_color=(1,1,1,0.4))
        self.inp5=TextInput(hint_text="Enter your Password",background_color=(1,1,1,0.4))
        self.btn3=Button(text="Go Back",on_release=self.backtologin,background_color=(0,0,0,0.5))
        self.create= Button(text=" Create Account",on_press=self.register,background_color=(0,0,0,0.5))

        self.layout.add_widget(self.inp1)
        self.layout.add_widget(self.inp2)
        self.layout.add_widget(self.inp3)
        self.layout.add_widget(self.inp4)
        self.layout.add_widget(self.inp5)
        self.layout.add_widget(self.create)
        self.layout.add_widget(self.btn3)

        #self.add_widget(self.layout)
        self.layout1.add_widget(self.layout)
        self.add_widget(self.layout1)
        #self.btn3=Button(text="Go Back",size_hint=(0.2,0.2),pos_hint=(0,1),on_release=self.backtologin)

    def register(self,instance):
        name=self.inp1.text
        uid=self.inp2.text
        section=self.inp3.text
        username=self.inp4.text
        password=self.inp5.text
        db=None
        try:
            db= mysql.connector.connect(host="localhost",user="root",password="Jojsafari_25",database="credentials")
            cursor=db.cursor()

            query = "SELECT * FROM log_in WHERE username=%s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()

            if result:
                popup = Popup(title="Error",
                              content=Label(text="Username already taken."),
                              size_hint=(None, None), size=(400, 200))
                popup.open()
            else:
                
                query = "INSERT INTO log_in (Name,UID,Section,username, password) VALUES (%s, %s,%s,%s,%s)"
                values = (name,uid,section,username, password)
                cursor.execute(query, values)
                db.commit()

                popup = Popup(title='Account Created',
                              content=Label(text='Account created successfully.'),
                              size_hint=(None, None), size=(400, 200))
                popup.open()
        except Exception as e:
            popup= Popup(title="Account creation Failed",content=Label(text=str(e),size_hint=(None,None),size=(400,200)))
            popup.open
        finally:
            if db is not None:
                cursor.close()
                db.close()    

    def backtologin(self,instance):
        self.manager.current="login"


class CreateQrScreen(BackgroundScreen2):
    def __init__(self, **kwargs):
        super(CreateQrScreen,self).__init__(**kwargs)
        self.layout2=GridLayout(cols=1,spacing=2,padding=250)
        self.layout1=BoxLayout(orientation="vertical",spacing=10,padding=280)
        self.layout=GridLayout(cols=1,spacing=10)
        #self.inptxt=TextInput(hint_text="Enter your Name",background_color=(1,1,1,0.4))
        self.qr_button= Button(text="Generate Qr Code", on_press=self.generate_qr_code)
        self.layout.add_widget(self.qr_button)
        
        
        self.layout1.add_widget(self.layout)
        self.add_widget(self.layout1)
        self.add_widget(self.layout2)

        self.qr_image = Image()
    
    def generate_random_string(self, length):
        characters = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(length))

        return random_string
    
    def generate_qr_code(self,instance):
        username = self.manager.get_screen('login').txt1.text

        # Fetch additional data from the database based on the username
        db = None
        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Jojsafari_25",
                database="credentials"
            )
            cursor = db.cursor()

            query = "SELECT Name, UID, Section FROM log_in WHERE username=%s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()

            if not result:
                raise ValueError("Username not found in the database")

            Name,UID,Section = result

        except Exception as e:
            # Handle database errors here
            Name = "Error fetching name from the database"
            UID = "Error fetching uid from the database"
            Section="Error fetching section from the database"
        finally:
            if db is not None:
                cursor.close()
                db.close()
        random_string = self.generate_random_string(15)
        get_data=f"Name:{Name}\nUID:{UID}\nSection:{Section}\n{random_string}"
        
        self.lbl= Label(text=random_string,color="white",font_size='20sp')
        qr = qrcode.QRCode(version=1, box_size=100, border=2)
        qr.add_data(get_data)
        qr.make(fit=True)
        qr_image = qr.make_image(fill="black", back_color="white")
        
        
        qr_image_path = "qr_code.png"
        qr_image.save(qr_image_path)
        self.layout.remove_widget(self.qr_button)  
        qr_image_widget = Image(source=qr_image_path)
        self.layout2.add_widget(qr_image_widget)
        self.qr_image = qr_image_widget 
        self.layout2.add_widget(self.lbl)


        Clock.schedule_once(self.clear_qr_code, 30)

        self.login_button=Button(text="Go Back to Login Page",size_hint=(None,None),size=(200, 100),
                          pos_hint={"center_x": 0.5},
                          on_press=self.go_to_login)

    def clear_qr_code(self,dt):
        self.layout2.remove_widget(self.qr_image)
        self.layout2.remove_widget(self.lbl)
        self.layout1.add_widget(self.login_button)
        
    def go_to_login(self, instance):
        self.manager.get_screen("login").txt1.text = ""  
        self.manager.get_screen("login").txt2.text = ""  
        self.manager.current = "login"


        
            
            
class AttendanceApp(App):
    def build(self):
         
        sm = ScreenManager(transition=FadeTransition())
        
        
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(CreateaccuntScreen(name="create_account"))
        sm.add_widget(CreateQrScreen(name="display"))
        
        return sm

if __name__ == "__main__":
    AttendanceApp().run()         