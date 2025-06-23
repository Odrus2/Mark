from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen

Window.softinput_mode = "pan"

KV = '''
<MessageCard>:
    padding: dp(10)
    radius: [12, 12, 0, 12] if self.sender else [12, 12, 12, 0]
    size_hint: None, None
    md_bg_color: (0.1, 0.6, 1, 1) if self.sender else (0.9, 0.9, 0.9, 1)
    pos_hint: {"right": 1} if self.sender else {"x": 0}

    MDLabel:
        id: message_label
        text: root.text
        halign: "left"
        theme_text_color: "Custom"
        text_color: (1, 1, 1, 1) if root.sender else (0, 0, 0, 1)
        size_hint_y: None
        height: self.texture_size[1]
        text_size: (None, None)

# Main customer care GUI screen
<CustomerCareScreen>:
    BoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "@Globo"
            left_action_items: [["message-outline"]]
            right_action_items: [["chat-outline"], ["dots-vertical"]]
            elevation: 4

        ScrollView:
            id: scrollview
            scroll_y: 0 

            MDBoxLayout:
                id: messages_box
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                padding: dp(10)
                spacing: dp(8)

        MDBoxLayout:
            size_hint_y: None
            height: self.minimum_height
            padding: dp(10)
            spacing: dp(10)
            md_bg_color: app.theme_cls.bg_light

            MDIconButton:
                icon: "plus"

            MDTextField:
                id: input_field
                hint_text: "Type a message..."
                mode: "round"
                size_hint_x: 1
                multiline: False
                on_text_validate: app.send_message()

            MDIconButton:
                icon: "send"
                on_release: app.send_message()
'''

class SplashScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.switch_to_main, 4)  # show image for 4 seconds

    def switch_to_main(self, *args):
        self.manager.current = 'customer_care_gui'

class CustomerCareScreen(Screen):
    pass

class MessageCard(MDCard):
    text = ""
    sender = False

    def __init__(self, text, sender, **kwargs):
        self.text = text
        self.sender = sender
        super().__init__(**kwargs)
        Clock.schedule_once(self.set_card_size)

    def set_card_size(self, *args):
        if not self.parent:
            return
        max_width = self.parent.width * 0.7
        label = self.ids.message_label
        label.text_size = (max_width - dp(20), None)
        label.texture_update()
        self.width = label.texture_size[0] + dp(20)
        self.height = label.texture_size[1] + dp(20)

class MyApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"

        Builder.load_string(KV)

        sm = ScreenManager()

        # Splash screen with image
        splash = SplashScreen(name='splash')
        splash.add_widget(Image(source='1234.jpg', allow_stretch=True, keep_ratio=True))
        sm.add_widget(splash)

        # Main customer care screen
        main_screen = CustomerCareScreen(name='customer_care_gui')
        sm.add_widget(main_screen)

        return sm

    def send_message(self):
        input_field = self.root.get_screen('customer_care_gui').ids.input_field
        text = input_field.text.strip()
        if text:
            self.add_message(text, sender=True)
            input_field.text = ""
            Clock.schedule_once(lambda dt: self.add_message("response", sender=False), 1)

    def add_message(self, text, sender):
        message_card = MessageCard(text=text, sender=sender)
        self.root.get_screen('customer_care_gui').ids.messages_box.add_widget(message_card)
        self.scroll_to_bottom()

    def scroll_to_bottom(self):
        Clock.schedule_once(lambda dt: setattr(self.root.get_screen('customer_care_gui').ids.scrollview, 'scroll_y', 0), 0.1)

if __name__ == "__main__":
    MyApp().run()