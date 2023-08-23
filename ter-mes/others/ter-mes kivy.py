from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.togglebutton import ToggleButton
import threading
import socket

class SimpleChatClientGUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.server_frame = GridLayout(cols=7, size_hint_y=None, height=40)
        self.server_frame.bind(minimum_height=self.server_frame.setter('height'))

        self.server_ip_label = Label(text="Server IP:")
        self.server_frame.add_widget(self.server_ip_label)

        self.server_ip_entry = TextInput()
        self.server_frame.add_widget(self.server_ip_entry)

        self.server_port_label = Label(text="Server Port:")
        self.server_frame.add_widget(self.server_port_label)

        self.server_port_entry = TextInput()
        self.server_frame.add_widget(self.server_port_entry)

        self.connect_button = Button(text="Connect")
        self.connect_button.bind(on_press=self.connect_to_server)
        self.server_frame.add_widget(self.connect_button)

        self.disconnect_button = Button(text="Disconnect")
        self.disconnect_button.bind(on_press=self.disconnect_from_server)
        self.server_frame.add_widget(self.disconnect_button)

        self.settings_button = Button(text="Settings")
        self.settings_button.bind(on_press=self.open_settings_window)
        self.server_frame.add_widget(self.settings_button)

        self.add_widget(self.server_frame)

        self.chat_text = ScrollView(size_hint=(1, 0.75))
        self.chat_text_box = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.chat_text_box.bind(minimum_height=self.chat_text_box.setter('height'))
        self.chat_text.add_widget(self.chat_text_box)
        self.add_widget(self.chat_text)

        self.message_entry = TextInput(size_hint_y=None, height=40, multiline=False)
        self.message_entry.bind(on_text_validate=self.send_message_event)
        self.add_widget(self.message_entry)

        self.send_button = Button(text="Send")
        self.send_button.bind(on_press=self.send_message)
        self.add_widget(self.send_button)

        self.selected_name = socket.gethostname()

        self.client_socket = None
        self.receive_thread = None

    def connect_to_server(self, instance):
        server_ip = self.server_ip_entry.text
        server_port = int(self.server_port_entry.text)

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((server_ip, server_port))
        except Exception as e:
            self.show_popup("Connection Error", f"Failed to connect to the server:\n{str(e)}")
            return

        self.connect_button.disabled = True
        self.disconnect_button.disabled = False
        self.send_button.disabled = False

        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

    def disconnect_from_server(self, instance):
        if self.client_socket:
            self.client_socket.close()

        self.connect_button.disabled = False
        self.disconnect_button.disabled = True
        self.send_button.disabled = True

    def open_settings_window(self, instance):
        content = BoxLayout(orientation='vertical')
        self.name_input = TextInput(hint_text='Enter a new name for the communicator')
        content.add_widget(self.name_input)

        popup = Popup(title='Change Name', content=content, size_hint=(None, None), size=(300, 150))
        popup.open_button = Button(text='Change')
        popup.open_button.bind(on_press=self.change_name)
        content.add_widget(popup.open_button)

        popup.open()

    def change_name(self, instance):
        new_name = self.name_input.text
        if new_name:
            self.selected_name = new_name
            instance.parent.parent.dismiss()

    def send_message(self, instance):
        message = self.message_entry.text.strip()
        if message:
            message_with_name = f"{self.selected_name}: {message}"
            self.client_socket.send(message_with_name.encode('utf-8'))
            self.message_entry.text = ''
        self.update_send_button_state()

    def send_message_event(self, instance):
        self.send_message(None)

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                self.chat_text_box.add_widget(Label(text=message))
            except:
                break

    def update_send_button_state(self):
        if self.client_socket:
            message = self.message_entry.text.strip()
            if message:
                self.send_button.disabled = False
            else:
                self.send_button.disabled = True
        else:
            self.send_button.disabled = True

    def show_popup(self, title, content):
        popup = Popup(title=title, content=Label(text=content), size_hint=(None, None), size=(300, 150))
        popup.open_button = Button(text='OK')
        popup.open_button.bind(on_press=popup.dismiss)
        popup.content.add_widget(popup.open_button)
        popup.open()

class SimpleChatApp(App):
    def build(self):
        return SimpleChatClientGUI()

if __name__ == '__main__':
    SimpleChatApp().run()
