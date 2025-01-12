from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy_garden.qrcode import QRCodeWidget
from kivy.storage.jsonstore import JsonStore

# Конфигурационный файл для сохранения данных
CONFIG_FILE = "config.json"
store = JsonStore(CONFIG_FILE)

# Словари для хранения данных
user_credentials = {
    "user1": "password1",
    "user2": "password2",
}
user_data = {
    "user1": "User 1 data",
    "user2": "User 2 data",
}

# Экран для входа
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.username_input = TextInput(hint_text='Логин', multiline=False)
        self.password_input = TextInput(hint_text='Пароль', password=True, multiline=False)

        self.message_label = Label(size_hint=(1, 0.2))

        login_button = Button(text='Войти', size_hint=(1, 0.3))
        login_button.bind(on_press=self.verify_credentials)

        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(self.message_label)
        layout.add_widget(login_button)

        self.add_widget(layout)

    def verify_credentials(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        if username in user_credentials and user_credentials[username] == password:
            # Сохранение последнего пользователя в конфиг
            store.put("last_user", username=username)
            self.manager.current = 'qr_screen'
            self.manager.get_screen('qr_screen').generate_qr(username)
        else:
            self.message_label.text = 'Неверный логин или пароль'

# Экран с QR-кодом
class QRScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.qr_widget = QRCodeWidget(size_hint=(1, 0.8))
        back_button = Button(text='Назад', size_hint=(1, 0.2))
        back_button.bind(on_press=self.go_back)

        layout.add_widget(self.qr_widget)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def generate_qr(self, username):
        if username in user_data:
            data = user_data[username]
            self.qr_widget.data = data

    def go_back(self, instance):
        self.manager.current = 'login_screen'

# Менеджер экранов
class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login_screen'))
        sm.add_widget(QRScreen(name='qr_screen'))

        # Загрузка конфигурации
        if store.exists("last_user"):
            last_user = store.get("last_user")["username"]
            if last_user and last_user in user_data:
                sm.current = 'qr_screen'
                sm.get_screen('qr_screen').generate_qr(last_user)

        return sm

if __name__ == '__main__':
    MyApp().run()
