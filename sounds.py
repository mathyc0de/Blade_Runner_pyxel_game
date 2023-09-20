from pygame import mixer

class Music:
    def __init__(self) -> None:
        mixer.init()




class Sons:
    def __init__(self) -> None:
        mixer.init()
        self.pulo_sound = mixer.Sound('assets/pulo.mp3')
        self.damage_sound = mixer.Sound('assets/damage.mp3')


    def pulo(self):
        self.pulo_sound.set_volume(0.15)
        self.pulo_sound.play()

    def damage(self):
        self.damage_sound.play(maxtime=500)
