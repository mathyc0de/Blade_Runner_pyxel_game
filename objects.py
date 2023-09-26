import pyxel as px
from sounds import Sons, Music
import os, platform


#Constantes
objectspos = []
timer = [[0, 0]]
multiplier = 1.0
counter = 0
lastscore = 0
EndGame = False
GameRestart = False
killscore = 0
show = 0
scoremake = 0
death = [False, True]
duo = False

def Multiplier() -> None:
    """incrementa o multiplicador conforme o tempo após o jogo começar"""
    global counter, multiplier, MapStart
    if MapStart:
        counter += 1
        if counter == 20 :
            multiplier += 0.25
            counter = 0




def choice(*elements):
    """randomizador de opções genérico para não precisar importar o random"""
    num = len(elements) - 1
    option = px.rndi(0, num)
    return elements[option]



def bestplay() -> None:
    """armazena a melhor jogada em AppData/local/Blade_Runner ou var/lib/Blade_Runner"""
    global config, scoremax
    if platform.system() == "Windows":
        dir = os.path.expanduser('~\\AppData\\Local\\Blade_Runner\\')
    elif platform.system() == "Linux":
        dir = ("~/.local/share/")
    path = dir+"bestplay.txt"
    IsExist = os.path.exists(dir)
    if not IsExist:
        os.makedirs(dir)
    try:
        with open(path, 'r') as f:
            scoremax = f.read()
            f.close()
    except:
        with open(path, "x") as f:
            f.write("0")
            scoremax = 0
            f.close()
    if lastscore > int(scoremax):
        with open(path, "w") as f1:
            f1.close()
        with open(path, "w") as f2:
            f2.write(str(lastscore))
            f2.close()
        scoremax = lastscore

def checkDuo() -> bool:
    return duo

def checkAlive() -> list:
    return death

def restart():
        """restaura o jogo para o estado inicial após o seu restart"""
        global GameRestart, objectspos, multiplier, lastscore, EndGame, map, death, player1, player2, enemies, config, killscore
        if GameRestart:
            config.__init__()
            EndGame = False
            objectspos = []
            multiplier = 1.0
            lastscore = 0
            killscore = 0
            player1.__init__(129, 188, 6, 1)
            player2.__init__(160, 191, 6, 2)
            GameRestart = False
            death = [False, True]
            map.__init__()
            enemies = []

class Player:
    def __init__(self, x: int, y: int, lives: int, p: int) -> None:
        """param x: posicao x do personagem
           param y: posicao y do personagem
           param p: player 1 ou 2
           param lives: número de vidas do personagem"""
        self.x = x
        self.y = y
        self.dy = 0
        self.h2 = 42
        self.direction = 'right'
        self.counter = 0
        self.counter0 = 0
        self.counter1 = 0
        self.sons = Sons()
        self.music = Music()
        self.air = False
        self.col_xr = False
        self.col_xl = False
        self.col_yup = False
        self.col_yd = False
        self.col_x = False
        self.col_y = False
        self.dmg = False
        self.dx = 0
        self.cooldown = 0
        self.lifebar = LifeBar(lives, p)
        self.u = 5
        self.u1 = 5
        self.u2 = 5
        self.idle = True
        self.attack = False
        self.attacking = False
        self.add = 0
        self.kills = 0
        self.p = p
        self.p2 = px.KEY_2
        if self.p == 1:
                self.w = 29
                self.h = 32
                self.img = 0
                self.v = 0
                self.v1 = 35
                self.v2 = 128
                self.up = px.KEY_W
                self.left = px.KEY_A
                self.right = px.KEY_D
                self.down = px.KEY_S
                self.p2 = px.KEY_2
        elif self.p == 2:
                self.w = 20
                self.add = 16
                self.h = 29
                self.img = 2
                self.v = 0
                self.v1 = 0
                self.v2 = 34
                self.p2 = px.KEY_KP_DECIMAL
                self.up = px.KEY_UP
                self.left = px.KEY_LEFT
                self.right = px.KEY_RIGHT
                self.down = px.KEY_DOWN
        self.x1 = self.x + self.w
        self.y1 = self.y + self.h
    



    def functions(self) -> None:
        """agrupa as funções da classe Player"""
        self.move()
        self.damage()
        self.knockback()
        self.jump()
        self.time()
        self.DetectCollisions()
        self.hitbox()











    def DetectCollisions(self):
        """Detecta colisões em função da lista de objetos que possuem física"""
        self.x1 = self.x + self.w
        self.y1 = self.y + self.h
        for num in range(0, len(objectspos)):
            if (self.x1  -5 > objectspos[num][0] and self.x < objectspos[num][1]) and (self.y1 == objectspos[num][3]):
                self.col_xr = True
                self.col_yd = True
                self.dmg = True
                     
            elif self.y1  == objectspos[num][2]:
                if objectspos[num][5] and self.dy == 0:
                    self.col_yd = True
                    self.air = False
                    
            else:
              
                self.col_xr = False
                self.col_yd = False
        for enemy in enemies:
            if (self.x1 + 10 > enemy.x and self.x - 5 < enemy.x1) and (self.y1 == enemy.y1):
                enemy.dmg = True
            else:
                enemy.dmg = False
            if (self.x1 + 2 > enemy.bulletxf and self.x - 2 < enemy.bulletxf) and (self.y - 3 <= enemy.bullety and self.y1 + 5 >= enemy.bullety + 25):
                self.col_xr = True
                self.dmg = True







    def hitbox(self):
            """Elimina os inimigos se aconter o clique de ataque e atender ao range e aumenta o score ao matar"""
            global killscore, show, scoremake, config, map            
            for enemy in enemies:
                    if enemy.dmg and self.attack:
                        objectspos.remove([enemy.x, enemy.x1, enemy.y, enemy.y1, True, False])
                        enemies.remove(enemy)
                        self.kills += 1
                        self.killcount()
                        killscore += px.ceil(10 * (multiplier))
                        scoremake = px.ceil(10 * (multiplier))
                        show = 5
                        scoremake = px.ceil(10 * (multiplier))




    def killcount(self):
        """conta os inimigos, a cada 10 kills restaura 1hp"""
        if self.kills % 10 == 0:
            if self.lifebar.vidas < 8:
                self.lifebar.vidas += 1
                self.lifebar.vidalos -= 1





        
            
            
    def knockback(self) -> None:
        """Joga o inimigo para trás ao levar dano"""
        global config
        if self.dx > 0:
                 if self.x - 1 > config.camerax:
                    self.x -= 4
                 self.dx -= 2
        if self.cooldown > 0:
            self.cooldown -= 1




                
                
    def damage(self) -> None:
        """Checa se o personagem levou dano, caso sim, diminui a vida ativa o knockback e toca um som de dano."""
        global MapStart
        if self.dmg and self.cooldown == 0 and MapStart:
            self.cooldown = 50
            self.dx = 20
            self.lifebar.vidas -= 1
            self.lifebar.vidalos += 1
            self.sons.damage()
            self.dmg = False
        elif self.dmg and self.cooldown > 0:
            self.dmg = False
            




            
    def move(self) -> None:
        """moveset do jogador"""
        global MapStart, EndGame, config, plat, duo
        if px.btnp(px.KEY_F) and not EndGame:
            if not MapStart:
                plat = choice(6, 86, 166)
            MapStart = True
        if px.btn(self.right) and MapStart and self.x1  < config.camerax + 320:
            self.direction = 'right'
            self.idle = False
            self.x += 3
        if px.btnp(self.up) and MapStart:
            if not self.air:
                self.sons.pulo()
                self.dy = 20
                self.air = True
        if px.btn(self.down) and MapStart:
            if not self.air and self.y < 180:
                    self.air = True
                    self.col_yd = False
                    self.dy = 0

        if MapStart:
            if self.x - 1 < config.camerax:
                self.x += 2
        if px.btn(self.left) and MapStart and self.x - 1 > config.camerax:
            self.x -= 3
            self.direction = 'left'
            
            self.idle = False

        if not px.btn(self.right) and not px.btn(self.left):
            self.idle = True

        if duo:
            if self.p == 1:
                if px.btnp(px.KEY_I):
                    if not self.attack:
                        self.hitbox()
                
                        self.attack = True
                        self.counter1 = 36
            else:
                if px.btnp(px.MOUSE_BUTTON_LEFT):
                    if not self.attack:
                        self.hitbox()
                
                        self.attack = True
                        self.counter1 = 36
        else:
            if px.btnp(px.MOUSE_BUTTON_LEFT):
                    if not self.attack:
                        self.hitbox()
                
                        self.attack = True
                        self.counter1 = 36

        if px.btnp(self.p2) and not MapStart:
            if duo:
                duo = False
                death[1] = True
            else:
                duo = True
                death[1] = False












        
    def jump(self) -> None:
        """parametriza a gravidade ao jogador pular"""
        if self.air:
            if self.dy > 0:
                self.y -= 4
                self.dy -= 1
            else:
                if not self.col_yd:
                    self.y += 4
                else:
                    self.air = False






    def time(self) -> None:
        """contador genérico para load de frames"""
        if self.p == 1:
            if self.counter == 15:
                self.u = 35
            elif self.counter == 30:
                self.u = 64
            elif self.counter == 45:
                self.u = 94
            elif self.counter == 60:
                self.u = 5
                self.counter = 0
            self.counter += 1


            if self.counter0 == 15:
                self.u1 = 34
            elif self.counter0 == 30:
                self.u1 = 65
            elif self.counter0 == 45:
                self.u1 == 94
            elif self.counter0 == 60:
                self.u1 = 123
            elif self.counter0 == 75:
                self.u1 = 154
            elif self.counter0 == 90:
                self.u1 = 5
                self.counter0 = 0
            self.counter0 += 1
            
            
            if self.counter1 == 6:
                self.u2 = 34
            elif self.counter1 == 12:
                self.u2 = 65
            elif self.counter1 == 18:
                self.u2 == 94
            elif self.counter1 == 24:
                self.u2 = 123
                self.add = 19
            elif self.counter1 == 30:
                self.add = 0
                self.u2 = 154
                self.attack = False
            elif self.counter1 == 36:
                self.u2 = 5
                self.add = 0
                self.counter1 = 0
            self.counter1 += 2
        else:
            if self.counter == 15:
                self.u = 26
            elif self.counter == 30:
                self.u = 47
            elif self.counter == 45:
                self.u = 68
            elif self.counter == 60:
                self.u = 5
                self.counter = 0
            self.counter += 1


            if self.counter0 == 15:
                self.u1 = 116
            elif self.counter0 == 30:
                self.u1 = 138
            elif self.counter0 == 45:
                self.u1 == 162
            elif self.counter0 == 60:
                self.u1 = 186
            elif self.counter0 == 75:
                self.u1 = 92
                self.counter0 = 0
            elif self.counter0 == 90:
                self.u1 = 92
                self.counter0 = 0
            self.counter0 += 1
            
            
            if self.counter1 == 6:
                self.u2 = 43
            elif self.counter1 == 12:
                self.u2 = 79
            elif self.counter1 == 18:
                self.u2 == 117
            elif self.counter1 == 24:
                self.u2 = 153
            elif self.counter1 == 30:
                self.u2 = 192
                self.attack = False
            elif self.counter1 == 36:
                self.u2 = 5
                self.counter1 = 0
            self.counter1 += 2



    def draw(self) -> None:
        """desenha as posições específicas do personagem"""
        if self.p == 2:
            col = 0
            p1const = 2
            p2const = 2
        else:
            col = 5
            p1const = -10
            p2const = 0
        if self.direction == 'right':
                if self.attack:
                    px.blt(self.x, self.y + p1const, self.img, self.u2, self.v2, self.w + self.add, self.h2, col)
                elif self.idle:
                    px.blt(self.x,self.y,self.img, self.u, self.v, self.w, self.h, col)
                else:
                    px.blt(self.x, self.y + p2const, self.img, self.u1, self.v1, self.w, self.h, col)
        if self.direction == 'left':
                if self.attack:
                    px.blt(self.x, self.y + p1const, self.img, self.u2, self.v2, -1 * self.w - self.add, self.h2, col)
                elif self.idle:
                    px.blt(self.x, self.y, self.img, self.u, self.v, -1 * self.w,self.h,col)
                else:
                    px.blt(self.x, self.y + p2const, self.img, self.u1, self.v1, -1 * self.w, self.h, col)




class Skeleton:
    def __init__(self, x, y) -> None:
        """"param x: pos x
            param y: pos y"""
        self.x = x
        self.y = y
        self.w = 50
        self.h = 54
        self.v = 148
        self.x = x
        self.u = 0
        self.u1 = 0
        self.x1 = self.x + self.w
        self.y = y
        self.y1 = self.y + self.h
        self.bulletxf = self.x + self.w - 30
        self.bullety = self.y + 27
        objectspos.append([self.x, self.x1, self.y, self.y1, True, False])
        self.bultime = 0
        self.time = 0
        self.dmg = False
        

    def timer(self):
        """outro contador genérico"""
        if self.time == 10:
            self.u = 51
        elif self.time == 20:
            self.u = 102
        elif self.time == 30:
            self.u = 153
        elif self.time  == 40:
            self.u = 204
        elif self.time == 50:
            self.u = 0
            self.time = 0
        self.time += 1

    def bulletTimer(self):
        """outro contador genérico"""
        if self.timer0 == 10:
            self.u1 = 51
        elif self.timer0 == 20:
            self.u1 = 102
        elif self.timer0 == 30:
            self.u1 = 153
        elif self.timer0  == 40:
            self.u1 = 204
        elif self.timer0 == 50:
            self.u1 = 0
            self.timer0 = 0
        self.timer0 += 1

    def draw(self) -> None:
        """desenha o inimigo"""
        px.blt(self.x, self.y, 2, self.u, self.v, -1 * self.w, self.h, 0)
        self.bulletsDraw()






    def bulletsDraw(self) -> None:
        """desenha as espadas lançadas pelos esqueletos"""
        if not self.bultime == 30:
            self.bulletxf -= 2
            px.blt(self.bulletxf, self.bullety, 2, self.u1, 206, 25, 25, 0)
            self.bultime += 1
        else:
            self.bultime = 0












class LifeBar:
    """classe usada para definir o hp do jogador"""
    def __init__(self, vidas: int, player: int) -> None:
        """param vidas: número de vidas"""
        self.vidas = vidas
        self.vidalos = 0
        self.die = False
        self.colort = 0
        if player == 1:
            self.x = 0
        elif player == 2:
            self.x = 200
        self.p = player






    def draw(self) -> None:
        """desenha as vidas e também procede com a morte do jogador e o restart do jogo."""
        global MapStart, lastscore, EndGame, GameRestart, config, show, scoremake
        if self.vidas == 0:
            death[self.p - 1] = True
        else:
            for numero in range(self.vidas + self.vidalos):
                px.blt(self.x + 12 *(numero+1) + config.camerax, 3, 0, 140, 5, 12, 10, 5)
            for numero in range(self.vidas):
                px.blt(self.x + 12 *(numero+1) + config.camerax, 3, 0, 125, 5, 12, 10, 5)
        if show > 0:
                px.text(13 + config.camerax, 30, f"+{scoremake}", 6)
                show -= 0.1






class Map:
    """classe usada para posicionar os objetos no mapa"""
    def __init__(self) -> None:
        global MapStart
        MapStart = False
        self.platform0 = Platform(220, "ground")
        self.platform1 = Platform(60, "platform")
        self.platform2 = Platform(140, "platform")
        self.time = 0
        self.colort = 0 
        self.timer = 0
        self.timer0 = 0
    

    def functions(self) -> None:
        """agrupa as funções da classe Map"""
        self.flame()
        self.pressStart()
        self.enemiesPos()




    




    def flame(self) -> None:
        """anima a fumaça que está sobre a fogueira na tela inicial"""
        self.stage = self.time/2 
        if self.time == 120:
            self.time = 0
        px.blt(160, 176, 0, 158 + self.stage, 0, 11, 20, 5)
        self.time += 1




    def enemiesPos(self):
        global enemies, MapStart
        if MapStart:
            for enemy in enemies:
                enemy.draw()


    def gamebackground(self) -> None:
            """desenha o background"""
            if self.timer == 0:
                self.staticx = config.camerax
            self.timer += 1
            for draw in range(5):
                px.blt(self.staticx + (draw * 160), 0,1, 0, 0, 160, 240)
            if self.timer == 240:
                self.timer = 0
            if MapStart:
                self.platform0.draw()
                self.platform1.draw()
                self.platform2.draw()
                    





    def pressStart(self) -> None:
        """desenha o startgame"""
        global MapStart, duo
        if duo:
            state = "2 jogadores"
        else:
            state = "1 jogador"
        self.colort += 0.25
        if self.colort == 16:
            self.colort = 0
        color = px.floor(self.colort)
        if not MapStart:
            px.rectb(100, 116, 120, 48, color)
            px.text(127, 136, "Press F to start", color)
            px.text(0, 80, """Pressione  '2' para jogar com dois jogadores""", 7)
            px.text(126, 150, f"Modo: {state}", 7)










        


class Platform:
    def __init__(self, y: int, type: str, Damage: bool=False, Fisica: bool=True) -> None:
        """Gera plataformas"""
        objectspos.append([0, 0, y, y + 14, Damage, Fisica])
        self.y = y
        self.timer = 0
        if type == "ground":
            self.u = 2
            self.v = 113
            self.w = 200
            self.h = 14
            self.draw_const = 160
            self.range = 5
        elif type == "platform":
            self.u = 0
            self.v = 178
            self.w = 85
            self.h = 7
            self.draw_const = 80
            self.range = 10







    def draw(self) -> None:
        """Desenha as plataformas no mapa e atualiza conforme o parâmetro camerax"""
        if self.timer == 0:
                self.staticx = config.camerax
        self.timer += 1
        for draw in range(self.range):
                px.blt(self.staticx + (draw * (self.draw_const)), self.y , 0, self.u, self.v, self.w, self.h, 5)
        if self.timer == 240:
                self.timer = 0

class Setup:
    def __init__(self) -> None:
        self.camerax = 0
        self.colort = 0
        self.enemyconst = 0
        self.index = 0
        self.enemycount = 1
        self.peak = 10
    
    def functions(self) -> None:
        """agrupamento das funções da classe Setup"""
        self.StartCheck()
        self.Score()
        self.enemyGen()
        self.enemyrate()
        self.endgame()
        self.enemiestimer()

    def Score(self):
        """Define a pontuação!"""
        global killscore, show, scoremake
        self.score =  px.ceil(self.camerax / 10 + (self.camerax/ 10 * multiplier)) + killscore

    def StartCheck(self) -> None:
        """Inicializa o mapa ao apertar F"""
        global MapStart
        if MapStart:
            self.camerax += 2
    
    def enemyrate(self) -> None:
        """a frequência com que os inimigos aparecem se conecta com o multiplicador
        que é incrementado conforme o tempo"""
        
        if multiplier > self.peak:
            self.enemycount += 1
            self.peak += 10

        if multiplier <= 48:
            self.enemyconst = px.ceil(multiplier * 10)
        else:
            self.enemyconst = 480

    def randcolor(self) -> int:
        """randomizador de cor"""
        self.colort += 0.25
        if self.colort == 16:
            self.colort = 0
        color = px.floor(self.colort)
        return color
    
    def endgame(self) -> None:
        """finaliza o jogo e recomeça"""
        global GameRestart, lastscore, EndGame, MapStart
        if death[0] and death[1]:
            MapStart = False
            EndGame = True
            if px.btnp(px.KEY_F):
                GameRestart = True
            lastscore = config.score
            bestplay()
            px.cls(0)
            px.rectb(config.camerax + 100, 86, 132, 48, self.randcolor())
            px.text(config.camerax + 105, 106, "You died, press F to play again", self.randcolor())
            px.text(config.camerax + 120, 200, f"Seu score foi: {lastscore}", 7)
            px.text(config.camerax + 120, 225, f"Sua melhor jogada foi: {scoremax}", 7)

    def enemyGen(self) -> None:
        """gera inimigos e põe em uma lista"""
        global enemies, plat
        if MapStart:
            if len(enemies) <= self.enemycount:
                enemies.append(Skeleton(px.rndi(config.camerax + 320, config.camerax + 700 + self.enemyconst), plat))
                self.index += 1
                newplat = choice(6, 86, 166)
                if plat == newplat:
                    newplat = choice(6, 86, 166)
                else:
                    plat = newplat    
            for enemy in enemies:
                if self.camerax - 40 > enemy.x:
                    enemies.remove(enemy)
    
    def enemiestimer(self) -> None:
        """roda o temporizador de cada inimigo"""
        if len(enemies) > 0:
            for index in range(len(enemies)):
                enemies[index].timer()



map = Map()
player1 = Player(129, 188, 6, 1)
player2 = Player(180, 191, 6, 2)
config = Setup()
enemies = []