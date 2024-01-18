from components.usable import Usable

npc_folder_location = "content/npcs"
npc_talk_distance = 150

class NPC(Usable):
    def __init__(self, obj_name, npc_file):
        super().__init__(obj_name)
        self.npc_file = npc_file

    def on(self, other, distance):
        from components.player import Player
        player = other.get(Player)
        if distance < npc_talk_distance:
        
            file = open(npc_folder_location + "/" + self.npc_file, "r")
            data = file.read()
            file.close()
            lines = data.split('\n')
            
            from components.ui.dialogue_view import DialogueView
            DialogueView(lines, self, player)
        else:
            player.show_message("I need to get closer")
