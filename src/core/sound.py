import pygame

audio_folder_location = "content/audio/sounds/"
sound_effects = {}
audio_enabled = True

class Sound:
    def __init__(self, file, volume=1.0):
        self.file = file
        if not file in sound_effects:
            path = audio_folder_location + file
            sound_effects[file] = pygame.mixer.Sound(path)
        
        self.sound = sound_effects[file]
        self.sound.set_volume(volume)

    def play(self):
        if audio_enabled:
            pygame.mixer.Sound.play(self.sound)

    def set_volume(self, volume):
        self.sound.set_volume(volume)