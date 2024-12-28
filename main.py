from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen

from kivymd.icon_definitions import md_icons
from kivymd.app import MDApp, App
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivymd.uix.list import OneLineIconListItem
from random import choice

Builder.load_string(
    '''
#:import images_path kivymd.images_path


<CustomOneLineIconListItem>

    IconLeftWidget:
        icon: root.icon


<PreviousMDIcons>

    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        padding: dp(20)

        MDBoxLayout:
            adaptive_height: True

            MDIconButton:
                icon: 'magnify'

            MDTextField:
                id: search_field
                hint_text: 'Search icon'
                on_text: root.set_list_md_icons(self.text, True)
        MDBoxLayout:
            size_hint_y:None
            height:dp(56)
            MDLabel:
                id:tag_label
                font_size:dp(36)
                theme_text_color:'Custom'
                text_color:[0,0.5,0.2,0.8]     

        RecycleView:
            id: rv
            key_viewclass: 'viewclass'
            key_size: 'height'

            CustomRecycleBoxLayout:
                padding: dp(10)
                default_size: None, dp(48)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
'''
)
class CustomRecycleBoxLayout(RecycleBoxLayout):
    def set_visible_views(self, indices, data, viewport):
        app = App.get_running_app()
        if indices:
            current = data[indices[0]]
            app.root.ids.tag_label.text = current['text'][0].upper()
            
        return super().set_visible_views(indices, data, viewport)
        

class CustomOneLineIconListItem(OneLineIconListItem):
    icon = StringProperty()


class PreviousMDIcons(Screen):

    def set_list_md_icons(self, text="", search=False):
        '''Builds a list of icons for the screen MDIcons.'''

        def add_icon_item(name_icon):
            self.ids.rv.data.append(
                {
                    "viewclass": "CustomOneLineIconListItem",
                    "icon": name_icon,
                    "text": name_icon,
                    "callback": lambda x: x,
                }
            )

        self.ids.rv.data = []
        for name_icon in md_icons.keys():
            if search:
                if text in name_icon:
                    add_icon_item(name_icon)
            else:
                add_icon_item(name_icon)


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = PreviousMDIcons()

    def build(self):
        return self.screen

    def on_start(self):
        self.screen.set_list_md_icons()


MainApp().run()