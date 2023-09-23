import pyxel as px
from objects import player1, Multiplier, map, player1, player2, config, checkDuo, checkAlive, restart


class APP:
    def __init__(self) -> None:
        px.init(320, 240, fps=60, title= 'Blade Runner')
        px.load("resources.pyxres")
        px.run(self.update, self.draw)
        px.sound(0).set()

    def update(self):
        self.isLive = checkAlive()
        restart()
        if not self.isLive[0]:
            player1.functions()
        self.duo = checkDuo()
        if self.duo and not self.isLive[1]:
            player2.functions()
        config.functions()
        map.pressStart()
        Multiplier()
        px.camera(config.camerax, 0)
        px.cls(6)
        


    def draw(self):
        map.gamebackground()
        px.blt(0, 196, 0, 2, 89, 252, 38, 5)
        px.blt(251, 220, 0, 2, 113, 87, 14, 5)
        if not self.isLive[0]:
            player1.draw()
        if self.duo and not self.isLive[1]:
            player2.draw()
        map.functions()
        px.text(13 + config.camerax, 20, f'Score: {config.score} ', 6)
        config.endgame()
        player1.lifebar.draw()
        if self.duo:
            player2.lifebar.draw()
            
        

APP()

