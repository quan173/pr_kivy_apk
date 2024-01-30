from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

import bluetooth
import threading

class BluetoothApp(App):
    def build(self):
        self.layout = GridLayout(cols=1)
        
        self.output_label = Label(text="Connect Bluetooth")
        self.layout.add_widget(self.output_label)

        self.input_text = TextInput(multiline=False)
        self.layout.add_widget(self.input_text)

        self.connect_button = Button(text="Connect Bluetooth")
        self.connect_button.bind(on_press=self.connect_bluetooth)
        self.layout.add_widget(self.connect_button)

        self.send_button = Button(text="Send Data")
        self.send_button.bind(on_press=self.send_data)
        self.layout.add_widget(self.send_button)

        self.receive_button = Button(text="Receive Data")
        self.receive_button.bind(on_press=self.receive_data)
        self.layout.add_widget(self.receive_button)

        return self.layout

    def connect_bluetooth(self, instance):
        threading.Thread(target=self._connect_bluetooth).start()

    def _connect_bluetooth(self):
        try:
            address = '98:DA:60:02:C1:BB'  # Thay đổi địa chỉ MAC của HC-06
            self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.sock.connect((address, 1))
            Clock.schedule_interval(self.receive_data, 1)
            self.output_label.text = "Connected to Bluetooth"
        except Exception as e:
            self.output_label.text = "Error: " + str(e)

    def send_data(self, instance):
        threading.Thread(target=self._send_data).start()

    def _send_data(self):
        try:
            data_to_send = self.input_text.text
            self.sock.send(data_to_send.encode())
            self.output_label.text = "Sent: " + data_to_send
        except Exception as e:
            self.output_label.text = "Error: " + str(e)

    def receive_data(self, dt):
        threading.Thread(target=self._receive_data).start()

    def _receive_data(self):
        try:
            received_data = self.sock.recv(1024)
            if received_data:
                self.output_label.text = "Received: " + received_data.decode()
        except Exception as e:
            self.output_label.text = "Error: " + str(e)

    def on_stop(self):
        try:
            self.sock.close()
        except:
            pass

if __name__ == "__main__":
    BluetoothApp().run()
