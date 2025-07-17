from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex
import webbrowser

class VolumeControl(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 15
        self.padding = 20

        # Heading
        heading = Label(text="PKTW THINKING", font_size='28sp',
                        color=get_color_from_hex("#FFFFFF"), size_hint=(1, 0.2))
        self.add_widget(heading)

        # Instagram link button
        insta_btn = Button(text="Created by - ig_gap_", size_hint=(1, 0.1),
                           background_color=get_color_from_hex("#1DA1F2"),
                           color=get_color_from_hex("#FFFFFF"))
        insta_btn.bind(on_release=lambda x: webbrowser.open("https://instagram.com/ig_gap_"))
        self.add_widget(insta_btn)

        # Volume sliders
        self.add_widget(self.create_slider("Media Volume"))
        self.add_widget(self.create_slider("Ringtone Volume"))
        self.add_widget(self.create_slider("Alarm Volume"))
        self.add_widget(self.create_slider("Notification Volume"))

    def create_slider(self, label_text):
        box = BoxLayout(orientation='horizontal', size_hint=(1, 0.2), spacing=10)
        lbl = Label(text=label_text, color=get_color_from_hex("#FFFFFF"), size_hint=(0.4, 1))
        sld = Slider(min=0, max=100, value=50, size_hint=(0.6, 1))
        box.add_widget(lbl)
        box.add_widget(sld)
        return box

class VolumeApp(App):
    def build(self):
        self.title = "MyKivyVolumeApp"
        from kivy.core.window import Window
        Window.clearcolor = get_color_from_hex("#222222")
        return VolumeControl()

if __name__ == "__main__":
    VolumeApp().run()
