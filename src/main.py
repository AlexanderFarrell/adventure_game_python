from core.engine import Engine
from stages.menu import menu
from stages.play import play
from stages.editor import editor

e = Engine("Adventure Game")
e.register("Menu", menu)
e.register("Play", play)
e.register("Editor", editor)
e.switch_to("Menu")
e.run()

