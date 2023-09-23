import pyxel as px
from objects import Player, Multiplier


class APP:
    def __init__(self) -> None:
        px.init(320, 240, fps=60, title= 'Blade Runner')
        px.load("resources.pyxres")
        self.player = Player(129, 188, 6)
        self.Map = self.player.Map
        px.run(self.update, self.draw)
        px.sound(0).set()

    def update(self):
        self.player.restart()
        self.Map = self.player.Map
        self.player.move()
        self.player.damage()
        self.player.knockback()
        self.player.jump()
        self.player.Score()
        self.player.time()
        Multiplier()
        self.player.DetectCollisions()
        px.camera(self.player.camerax, 0)
        self.player.hitbox()
        px.cls(6)
        


    def draw(self):
        self.Map.gamebackground(self.player.camerax)
        px.blt(0, 196, 0, 2, 89, 252, 38, 5)
        px.blt(251, 220, 0, 2, 113, 87, 14, 5)
        self.Map.flame()
        self.player.draw()
        self.player.hitbox()
        self.Map.pressStart()
        self.Map.drawStart(self.player.camerax)
        self.Map.spawnEnemies(self.player.camerax)
        px.text(13 + self.player.camerax, 20, f'Score: {self.player.score} ', 6)
        self.player.lifebar.draw()
            
        

APP()

