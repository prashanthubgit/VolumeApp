from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex
from kivy.uix.popup import Popup

# Try to import pyjnius for Android volume control
try:
    from jnius import autoclass
    Context = autoclass('android.content.Context')
    AudioManager = autoclass('android.media.AudioManager')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Intent = autoclass('android.content.Intent')
    Uri = autoclass('android.net.Uri')
    HAS_PYJNIUS = True
except ImportError:
    HAS_PYJNIUS = False

class VolumeControl(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 15
        self.padding = 20
        
        # Audio manager for Android
        self.audio_manager = None
        self.activity = None
        if HAS_PYJNIUS:
            try:
                self.activity = PythonActivity.mActivity
                self.audio_manager = self.activity.getSystemService(Context.AUDIO_SERVICE)
            except Exception as e:
                print(f"Error initializing AudioManager: {e}")

        # Heading
        heading = Label(text="🔊 PKTW THINKING 🔊", font_size='28sp',
                        color=get_color_from_hex("#FFFFFF"), size_hint=(1, 0.12), bold=True)
        self.add_widget(heading)

        # Instagram link button
        insta_btn = Button(text="👤 Created by - ig_gap_", size_hint=(1, 0.08),
                           background_color=get_color_from_hex("#E1306C"),
                           color=get_color_from_hex("#FFFFFF"), font_size='14sp')
        insta_btn.bind(on_release=self.open_instagram)
        self.add_widget(insta_btn)

        # Volume sliders with labels
        self.volume_sliders = {}
        self.add_widget(self.create_slider("🎵 Media Volume", AudioManager.STREAM_MUSIC if HAS_PYJNIUS else 3))
        self.add_widget(self.create_slider("📞 Ringtone Volume", AudioManager.STREAM_RING if HAS_PYJNIUS else 2))
        self.add_widget(self.create_slider("⏰ Alarm Volume", AudioManager.STREAM_ALARM if HAS_PYJNIUS else 4))
        self.add_widget(self.create_slider("🔔 Notification Volume", AudioManager.STREAM_NOTIFICATION if HAS_PYJNIUS else 5))

        # Mute/Unmute button
        mute_btn = Button(text="🔇 Mute All", size_hint=(1, 0.08),
                          background_color=get_color_from_hex("#FF6B6B"),
                          color=get_color_from_hex("#FFFFFF"), font_size='14sp')
        mute_btn.bind(on_release=self.mute_all_volumes)
        self.add_widget(mute_btn)

        # Unmute button
        unmute_btn = Button(text="🔊 Unmute All", size_hint=(1, 0.08),
                            background_color=get_color_from_hex("#51CF66"),
                            color=get_color_from_hex("#FFFFFF"), font_size='14sp')
        unmute_btn.bind(on_release=self.unmute_all_volumes)
        self.add_widget(unmute_btn)

    def open_instagram(self, instance):
        """Open Instagram profile using Android Intent"""
        if HAS_PYJNIUS:
            try:
                if self.activity:
                    intent = Intent()
                    intent.setAction(Intent.ACTION_VIEW)
                    intent.setData(Uri.parse("https://instagram.com/ig_gap_"))
                    self.activity.startActivity(intent)
            except Exception as e:
                print(f"Error opening Instagram: {e}")
                self.show_popup("Instagram", "Could not open Instagram.\nPlease visit: https://instagram.com/ig_gap_")
        else:
            self.show_popup("Instagram", "Visit: https://instagram.com/ig_gap_")

    def show_popup(self, title, message):
        """Show information popup"""
        popup = Popup(title=title, size_hint=(0.85, 0.35))
        content = BoxLayout(orientation='vertical', padding=15, spacing=10)
        content.add_widget(Label(text=message, color=get_color_from_hex("#000000")))
        close_btn = Button(text='Close', size_hint=(1, 0.3), background_color=get_color_from_hex("#1DA1F2"))
        close_btn.bind(on_press=popup.dismiss)
        content.add_widget(close_btn)
        popup.content = content
        popup.open()

    def create_slider(self, label_text, stream_type=None):
        """Create a volume slider with label and value display"""
        box = BoxLayout(orientation='horizontal', size_hint=(1, 0.11), spacing=10)
        
        lbl = Label(text=label_text, color=get_color_from_hex("#FFFFFF"), size_hint=(0.3, 1), bold=True)
        
        # Get current volume if possible
        current_vol = 50
        if self.audio_manager and stream_type is not None:
            try:
                current_vol = (self.audio_manager.getStreamVolume(stream_type) / 
                              self.audio_manager.getStreamMaxVolume(stream_type)) * 100
            except:
                pass
        
        sld = Slider(min=0, max=100, value=current_vol, size_hint=(0.5, 1))
        val_lbl = Label(text=f"{int(current_vol)}%", color=get_color_from_hex("#1DA1F2"), 
                       size_hint=(0.2, 1), bold=True, font_size='14sp')
        
        # Store slider info for volume control
        self.volume_sliders[label_text] = {
            'slider': sld,
            'label': val_lbl,
            'stream_type': stream_type,
            'label_text': label_text
        }
        
        # Bind slider to value update and volume control
        sld.bind(value=lambda s, v: self.update_volume(label_text, v))
        
        box.add_widget(lbl)
        box.add_widget(sld)
        box.add_widget(val_lbl)
        return box

    def update_volume(self, slider_name, value):
        """Update volume label and set system volume"""
        if slider_name not in self.volume_sliders:
            return
            
        slider_info = self.volume_sliders[slider_name]
        slider_info['label'].text = f"{int(value)}%"
        
        # Set Android system volume if available
        if self.audio_manager and slider_info['stream_type'] is not None:
            try:
                max_volume = self.audio_manager.getStreamMaxVolume(slider_info['stream_type'])
                target_volume = int((value / 100) * max_volume)
                self.audio_manager.setStreamVolume(slider_info['stream_type'], target_volume, 0)
            except Exception as e:
                print(f"Error setting volume for {slider_name}: {e}")

    def mute_all_volumes(self, instance):
        """Mute all volume streams"""
        if self.audio_manager:
            for slider_name, slider_info in self.volume_sliders.items():
                try:
                    slider_info['slider'].value = 0
                    self.update_volume(slider_name, 0)
                except Exception as e:
                    print(f"Error muting {slider_name}: {e}")
        else:
            for slider_name, slider_info in self.volume_sliders.items():
                slider_info['slider'].value = 0
        
        self.show_popup("Muted", "✅ All volumes muted!")

    def unmute_all_volumes(self, instance):
        """Unmute all volume streams to 70%"""
        default_volume = 70
        if self.audio_manager:
            for slider_name, slider_info in self.volume_sliders.items():
                try:
                    slider_info['slider'].value = default_volume
                    self.update_volume(slider_name, default_volume)
                except Exception as e:
                    print(f"Error unmuting {slider_name}: {e}")
        else:
            for slider_name, slider_info in self.volume_sliders.items():
                slider_info['slider'].value = default_volume
        
        self.show_popup("Unmuted", f"✅ All volumes set to {default_volume}%!")

class VolumeApp(App):
    def build(self):
        self.title = "MyKivyVolumeApp"
        from kivy.core.window import Window
        Window.clearcolor = get_color_from_hex("#1a1a1a")
        Window.size = (400, 800)
        
        if not HAS_PYJNIUS:
            print("⚠️ Warning: pyjnius not available. Volume control will not work on Android.")
            print("✓ This is normal for desktop testing.")
        else:
            print("✅ pyjnius loaded successfully. Volume control is active!")
        
        return VolumeControl()

if __name__ == "__main__":
    VolumeApp().run()
