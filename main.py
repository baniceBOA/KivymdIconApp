from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.uix.screenmanager import Screen

from kivymd.icon_definitions import md_icons
from kivymd.app import MDApp, App
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.menu import MDDropdownMenu
from random import choice
import itertools
import string
from string import ascii_uppercase

Builder.load_string(
    '''
#:import images_path kivymd.images_path

<CustomGridItem>:
    orientation:'vertical'
    padding:dp(20)
    spacing:dp(10)
    size_hint_y:None
    height:dp(200)
    MDIcon:
        icon:root.icon
        pos_hint:{'center_x':0.5}
        font_size:dp(25)
    MDLabel:
        text:root.text
        halign:'center'
<CustomOneLineIconListItemWithLetter>:
    size_hint_y:None
    height:list_item.height
    MDLabel:
        halign:'center'
        size_hint_x:None
        width:dp(10)
        text:root.letter
        theme_text_color:'Custom'
        text_color:app.theme_cls.accent_color
        font_size:dp(15)
    OneLineIconListItem:
        id:list_item
        text:root.text
        IconLeftWidget:
            icon: root.icon

<CustomOneLineIconListItem>:
    IconLeftWidget:
        icon:root.icon

<PreviousMDIcons>

    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        padding: dp(14)

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
            md_bg_color:app.theme_cls.bg_dark
            MDLabel:
                id:tag_label
                font_size:dp(36)
                theme_text_color:'Custom'
                text_color:app.theme_cls.accent_color
            MDIconButton:
                id:menu_button
                icon:'dots-vertical'
                on_release:app.open_dropdown()   

        RecycleView:
            id: rv
            key_viewclass: 'viewclass'
            key_size: 'height'
            bar_inactive_color:app.theme_cls.primary_light
            bar_color:app.theme_cls.primary_dark
            bar_width:dp(10)

            CustomRecycleBoxLayout:
                padding: dp(10)
                default_size: None, dp(48)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                cols:1
                #orientation: 'vertical'
'''
)

class CustomGridItem(MDBoxLayout):
    icon = StringProperty()
    text = StringProperty()
    
class CustomRecycleBoxLayout(RecycleGridLayout):
   
    def set_visible_views(self, indices, data, viewport):
        app = App.get_running_app()
        if indices:
           if isinstance(indices, range):
               current = data[indices[0]]
               letter = current['text'][0].upper()
               app.root.ids.tag_label.text = letter
           else:
               for chain in indices:
                   current = data[chain]
                   letter = current['text'][0].upper()
                   app.root.ids.tag_label.text = letter
                   break
                   
            
                
        return super().set_visible_views(indices, data, viewport)
    
        
        
class CustomOneLineIconListItem(OneLineIconListItem):
    icon =StringProperty()
    
class CustomOneLineIconListItemWithLetter(MDBoxLayout):
    letter = StringProperty()
    text = StringProperty()
    icon = StringProperty()


class PreviousMDIcons(Screen):
    

    def set_list_md_icons(self, text="", search=False):
        '''Builds a list of icons for the screen MDIcons.'''
        app = App.get_running_app()
        
        def add_icon_item(name_icon):
            letter = name_icon[0].upper()
            letters = app.letters
            if letter in letters:
                
                self.ids.rv.data.append(
                {
                    "viewclass": "CustomOneLineIconListItemWithLetter" if app.root.ids.rv.layout_manager.cols == 1 else 'CustomGridItem' ,
                    "icon": name_icon,
                    "text": name_icon,
                    "callback": lambda x: x,
                    'letter':letter 
                }
            )
                letters.remove(letter)
                
            else:
                self.ids.rv.data.append(
                {
                    "viewclass": "CustomOneLineIconListItem" if app.root.ids.rv.layout_manager.cols == 1 else 'CustomGridItem',
                    "icon": name_icon,
                    "text": name_icon,
                    "callback": lambda x: x,
                    
                }
            )
        self.ids.rv.data = []
        app.letters = list(ascii_uppercase)
        
        for name_icon in md_icons.keys():
            if search:
                if text in name_icon:
                    add_icon_item(name_icon)
            else:
                add_icon_item(name_icon)
    

class MainApp(MDApp):
    letters = ListProperty(list(ascii_uppercase))
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = PreviousMDIcons()
        
    def build(self):
        return self.screen

    def on_start(self):
        self.theme_cls.accent_palette = 'Blue'
        self.screen.set_list_md_icons()
        options = ['List', 'Grid']
        items_menu =  []
        for option in options:
            items_menu.append({
                'text':option,
                'viewclass':'OneLineListItem',
                'on_release':lambda x=f'{option}':self.menu_callback(x),
            })
        self.menu = MDDropdownMenu(items=items_menu, caller=self.root.ids.menu_button)

        
    def on_letters(self, instance, value):
        print(value)
    def menu_callback(self, x):
        if x == 'Grid':
            self.root.ids.rv.layout_manager.cols = 2
            self.screen.set_list_md_icons()
        if x == 'List' and self.root.ids.rv.layout_manager.cols != 1:
            self.root.ids.rv.layout_manager.cols = 1
            self.screen.set_list_md_icons()
            
        self.menu.dismiss()
    def open_dropdown(self):
        self.menu.open()
        



MainApp().run()