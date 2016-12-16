from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import (ObjectProperty, ListProperty, StringProperty,
    NumericProperty)
from kivy.uix.listview import ListItemButton
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.storage.jsonstore import JsonStore
from kivy.uix.modalview import ModalView
from kivy.clock import Clock
import bar
import os
from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')

def global_fn():
  global myApp
  print dir(myApp)
  myApp.root.bar_red.bar_value += 3

class SensorRoot(BoxLayout):

  bar_red = ObjectProperty()
  bar_yellow = ObjectProperty()
  bar_green = ObjectProperty()
  bar_blue = ObjectProperty()
  exit_text = ObjectProperty()

  ## BEGIN INIT
  #def __init__(self, **kwargs):
    #pass


class BarWidget(BoxLayout):
  bar_color = ListProperty()
  bar_value = NumericProperty() 
  bar_text = StringProperty() # the text right under the bar
  bar_legend = StringProperty() # the legend under the bar
  bar_width  = StringProperty() # 

  def set_value(self,value):
    self.bar_value = str(value)

  def on_bar_legend(self, instance, value):
    pass #self.bar.value = value
    print('Value changed to ', str(value))

  def button_press(self):
    self.bar_value = self.bar_value+1
    print "boing"

class AboutPopup(BoxLayout):
  about_text  = StringProperty() # 

class ConfirmationDialog(BoxLayout):
  dialog_text  = StringProperty() # 

#---------------------------------------

class BlipperApp(App):
  app_root = Builder.load_file("display.kv")

   
  def build(self):
    return self.app_root

  def exit(self):
    #self.root.exit_text.text = "Exiting..."
    print "stopping"
    self.stop()

  def shutdown(self):
    #self.root.exit_text.text = "Exiting..."
    print "stopping"
    os.system('sudo shutdown now')

  def reboot(self):
    print "rebooting"
    os.system('sudo reboot now')

  def about(self):    
    Builder.load_file("popup.kv")
    self.view = ModalView(size_hint=(None, None), size=(700, 440),auto_dismiss=False)
    self.view.add_widget(AboutPopup())
    for child in self.view.children[:]:
      print child

    f = open('about.txt')
    self.view.children[0].about_text = f.read()
    #self.view.ModalView.about_text = f.read()
    self.view.open()    

  def dismiss(self):
    self.view.dismiss()
    self.view.clear_widgets()
    Builder.unload_file("popup.kv")

  def reboot_confirm(self):    
    self.view = ModalView(size_hint=(None, None), size=(500, 300),auto_dismiss=False)
    self.view.add_widget(ConfirmationDialog())
    self.view.children[0].dialog_text ="[size=24]Are you sure you wish\n to reboot?[/size]"
    #self.view.ModalView.about_text = f.read()
    self.confirm_callback = self.reboot
    self.view.open()    

  def shutdown_confirm(self):    
    self.view = ModalView(size_hint=(None, None), size=(500, 300),auto_dismiss=False)
    self.view.add_widget(ConfirmationDialog())
    self.view.children[0].dialog_text ="[size=24]Are you sure you wish\n to shut down?[/size]\n\n(Always shut down the app before\nunplugging the  power adapter!)"
    #self.view.ModalView.about_text = f.read()
    self.confirm_callback = self.shutdown
    self.view.open()    

  def confirm(self):
    self.confirm_callback()


if __name__ == '__main__':
  global myApp
  #Builder.load_file('display.kv')
  myApp = BlipperApp()
  myApp.run()
