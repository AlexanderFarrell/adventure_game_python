from core.engine import Engine
from stages.menu import menu
from stages.play import play

e = Engine("Adventure Game")
e.register("Menu", menu)
e.register("Play", play)
e.switch_to("Play")
e.run()

