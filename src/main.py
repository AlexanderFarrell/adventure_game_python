from core.engine import Engine
from states.menu import menu
from states.play import play

e = Engine("Adventure Game")
e.register("Menu", menu)
e.register("Play", play)
e.switch_to("Play")
e.run()

