from pygame import mixer
import settings

class Sounds:
    def __init__(self):
        self.sound_volume = settings.SOUND_VOLUME
        self.music_volume = settings.MUSIC_VOLUME

        # Music
        self.base_music = mixer.Sound('audio/music/Main.wav')
        self.fight_music = mixer.Sound('audio/music/dungeon.mp3')
        self.shop_music = mixer.Sound('audio/music/shop.wav')
        self.intro_music = mixer.Sound('audio/music/intro.mp3')

        self.set_volume(self.base_music,self.music_volume)
        self.set_volume(self.fight_music,self.music_volume)
        self.set_volume(self.shop_music,self.music_volume)
        self.set_volume(self.intro_music,self.music_volume)

        # Sounds
        self.player_damaged = mixer.Sound('audio/sound/Minifantasy_Dungeon_SFX/11_human_damage_2.wav')
        self.enemy_damaged = mixer.Sound('audio/sound/Minifantasy_Dungeon_SFX/11_human_damage_3.wav')
        self.attack = mixer.Sound('audio/sound/human_atk_sword_2.wav')
        self.level_up = mixer.Sound('audio/sound/level_up.wav')
        self.door = mixer.Sound('audio/sound/door.wav')
        self.start_game = mixer.Sound('audio/sound/start_game.wav')

        self.set_volume(self.attack,self.sound_volume)
        self.set_volume(self.level_up,self.sound_volume)
        self.set_volume(self.door,self.sound_volume)
        self.set_volume(self.start_game,self.sound_volume)
        

    def set_volume(self,name,volume):
        mixer.Sound.set_volume(name,max(0,volume))
        
    def play_audio(self,name,loops):
        mixer.Sound.play(name,loops)
    
    def stop_audio(self):
        mixer.stop()