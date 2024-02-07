from components.ui.text_input import TextInput
from components.ui.scroll_view import ScrollView, create_scroll_label_generic
from components.entity import Entity

def editor():
    Entity(TextInput("EBGaramond-ExtraBold.ttf", "Test"))
    Entity(ScrollView(["Eggs", "Ham", "Cheese", "Bread"], create_scroll_label_generic, None, 50), x=200, y=200)