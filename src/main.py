from core.engine import Engine
from stages.menu import menu
from stages.play import play
from stages.editor.choose_file import editor_choose_file
from stages.editor.edit_map import edit_map

e = Engine("Adventure Game")
e.register("Menu", menu)
e.register("Play", play)
e.register("EditorChooseFile", editor_choose_file)
e.register("EditorEditMap", edit_map)
e.switch_to("Menu")
e.run()
