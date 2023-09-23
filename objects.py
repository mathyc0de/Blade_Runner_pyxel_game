import pyxel as px
from sounds import Sons, Music
from abc import ABC, abstractclassmethod
import os, platform


#Constantes
objectspos = []
timer = [[0, 0]]
bulletpos = [[0, 0, 0, 0, False, False]]
multiplier = 1.0
counter = 0
bulletind = []
enemy1 = False
enemy2 = False
enemy3 = False
enemy4 = False
enemy5 = False
score = 0
lastscore = 0
EndGame = False
GameRestart = False
killscore = 0
show = 0
scoremake = 0

def Multiplier() -> None:
    """incrementa o multiplicador conforme o tempo após o jogo começar"""
    global counter, multiplier, MapStart
    if MapStart:
        counter += 1
        if counter == 20 :
            multiplier += 0.1
            counter = 0




def choice(*elements):
    """randomizador de opções genérico para não precisar importar o random"""
    num = len(elements) - 1
    option = px.rndi(0, num)
    return elements[option]



def bestplay() -> None:
    """armazena a melhor jogada em AppData/local/Blade_Runner ou var/lib/Blade_Runner"""
    global scoremax
    if platform.system == "Windows":
        dir = os.path.expanduser('~\\AppData\\Local\\Blade_Runner\\')
    elif platform.system == "Linux":
        dir = ("\\var\\lib\\Blade_Runner\\")
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
    

class Player:
    def __init__(self, x: int, y: int, lives: int) -> None:
        """param x: posicao x do personagem
           param y: posicao y do personagem
           param lives: número de vidas do personagem"""
        self.x = x
        self.y = y
        self.dy = 0
        self.w = 29
        self.h = 32
        self.h2 = 42
        self.x1 = self.x + self.w
        self.y1 = self.y + self.h
        self.direction = 'right'
        self.counter = 0
        self.counter0 = 0
        self.counter1 = 0
        self.sons = Sons()
        self.music = Music()
        self.Map = Map()
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
        self.camerax = 0
        self.lifebar = LifeBar(lives)
        self.u = 5
        self.u1 = 5
        self.u2 = 5
        self.idle = True
        self.attack = False
        self.attacking = False
        self.add = 0
        self.score = 0
        self.kills = 0
        






    def restart(self):
        """restaura o jogo para o estado inicial após o seu restart"""
        global GameRestart, objectspos, timer, bulletpos, multiplier, counter, bulletind, enemy1, enemy2, enemy3, enemy4, enemy5, score, lastscore, EndGame
        if GameRestart:
            objectspos = []
            timer = [[0, 0]]
            bulletpos = [[0, 0, 0, 0, False, False]]
            multiplier = 1.0
            counter = 0
            bulletind = []
            enemy1 = False
            enemy2 = False
            enemy3 = False
            enemy4 = False
            enemy5 = False
            score = 0
            lastscore = 0
            EndGame = False
            self.__init__(129, 188, 6)
            self.Map = Map()
            GameRestart = False
            






    def DetectCollisions(self):
        """Detecta colisões em função da lista de objetos que possuem física"""
        global enemy1, enemy2, enemy3, enemy4, enemy5
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

            if (self.x1 + 10 > objectspos[num][0] and self.x - 5 < objectspos[num][1]) and (self.y1 == objectspos[num][3]) and objectspos[num][4] == True:
                if objectspos[num][6] == 0:
                    enemy1 = True
                elif objectspos[num][6] == 1:
                    enemy2 = True
                elif objectspos[num][6] == 2:
                    enemy3 = True
                elif objectspos[num][6] == 3:
                    enemy4 = True
                elif objectspos[num][6] == 4:
                    enemy5 = True

            elif objectspos[num][4]:
                if objectspos[num][6] == 0:
                    enemy1 = False
                elif objectspos[num][6] == 1:
                    enemy2 = False
                elif objectspos[num][6] == 2:
                    enemy3 = False
                elif objectspos[num][6] == 3:
                    enemy4 = False
                elif objectspos[num][6] == 4:
                    enemy5 = False

        for num in range(0, len(bulletpos)):
            if (self.x1 + 2 > bulletpos[num][0] and self.x - 2 < bulletpos[num][1]) and (self.y - 3 <= bulletpos[num][2] and self.y1 + 5 >= bulletpos[num][3]):
                self.col_xr = True
                self.dmg = True








    def hitbox(self):
            """Elimina os inimigos se o clique de ataque e atender ao range e aumenta o score ao matar"""
            global enemy1, enemy2, enemy3, enemy4, enemy5, killscore, show, scoremake            
            if enemy1 and self.attack:
                    self.Map.skel.pop(-300, 400)
                    self.kills += 1
                    self.killcount()
                    killscore += px.ceil(10 * (multiplier))
                    scoremake = px.ceil(10 * (multiplier))
                    show = 5
            if enemy2 and self.attack:
                    self.Map.skel1.pop(-300, 400)
                    self.kills += 1
                    killscore += px.ceil(10 * (multiplier))
                    scoremake = px.ceil(10 * (multiplier))
                    show = 5
            if enemy3 and self.attack:
                    self.Map.skel2.pop(-300, 400)
                    self.kills += 1
                    self.killcount()
                    killscore += px.ceil(10 * (multiplier))
                    scoremake = px.ceil(10 * (multiplier))
                    show = 5
            if enemy4 and self.attack:
                    self.Map.skel3.pop(-300, 400)
                    self.kills += 1
                    self.killcount()
                    killscore += px.ceil(10 * (multiplier))
                    scoremake = px.ceil(10 * (multiplier))
                    show = 5
            if enemy5 and self.attack:
                    self.Map.skel4.pop(-450, 400)
                    self.kills += 1
                    self.killcount()
                    killscore += px.ceil(10 * (multiplier))
                    scoremake = px.ceil(10 * (multiplier))
                    show = 5
            if show > 0:
                    px.text(13 + self.camerax, 30, f"+{scoremake}", 6)
                    show -= 0.1




    def killcount(self):
        """conta os inimigos, a cada 10 kills restaura 1hp"""
        if self.kills % 10 == 0:
            if self.lifebar.vidas < 8:
                self.lifebar.vidas += 1
                self.lifebar.vidalos -= 1







    def Score(self):
        """Define a pontuação!"""
        global score, killscore
        self.score =  px.ceil(self.camerax / 10 + (self.camerax/ 10 * multiplier)) + killscore
        score = self.score

        
            
            
    def knockback(self) -> None:
        """Joga o inimigo para trás ao levar dano"""
        if self.dx > 0:
                 if self.x - 1 > self.camerax:
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
        global MapStart, EndGame
        self.StartCheck()
        if px.btnp(px.KEY_F) and not EndGame:
            MapStart = True
        if px.btn(px.KEY_D) and MapStart and self.x1  < self.camerax + 320:
            self.direction = 'right'
            self.idle = False
            self.x += 3
        if px.btnp(px.KEY_SPACE) or px.btnp(px.KEY_W) and MapStart:
            if not self.air:
                self.sons.pulo()
                self.dy = 20
                self.air = True
        if px.btn(px.KEY_S) and MapStart:
            if not self.air and self.y < 180:
                    self.air = True
                    self.col_yd = False
                    self.dy = 0

        if MapStart:
            if self.x - 1 < self.camerax:
                self.x += 2
        if px.btn(px.KEY_A) and MapStart and self.x - 1 > self.camerax:
            self.x -= 3
            self.direction = 'left'
            
            self.idle = False

        if not px.btn(px.KEY_A) and not px.btn(px.KEY_D):
            self.idle = True

        if px.btnp(px.MOUSE_BUTTON_LEFT):
            if not self.attack:
                self.hitbox()
                
                self.attack = True
                self.counter1 = 36







    def StartCheck(self) -> None:
        """Inicializa o mapa ao apertar F"""
        global MapStart
        if MapStart:
            self.camerax += 2
            self.lifebar.camerax = self.camerax
            px.cls(5)






        
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






    def draw(self) -> None:
        """desenha as posições específicas do personagem"""
        if self.direction == 'right':
                if self.attack:
                    px.blt(self.x, self.y - 10, 0, self.u2, 128, self.w + self.add, self.h2, 5)
                elif self.idle:
                    px.blt(self.x,self.y,0, self.u,0, self.w, self.h, 5)
                else:
                    px.blt(self.x, self.y, 0, self.u1, 35, self.w, self.h, 5)
        if self.direction == 'left':
                if self.attack:
                    px.blt(self.x, self.y - 10, 0, self.u2, 128, -1 * self.w - self.add, self.h2, 5)
                elif self.idle:
                    px.blt(self.x, self.y, 0, self.u, 0, -1 * self.w,self.h,5)
                else:
                    px.blt(self.x, self.y, 0, self.u1, 35, -1 * self.w, self.h, 5)








class Enemies (ABC):
    @abstractclassmethod
    def __init__(self, x, y) -> None:
        """param x: posição x do inimigo
           param y: posição y do inimigo"""
        self.x = x
        self.y = y
        self.time = 0

    def timer(self, num: int, u1, u2, u3, u4, u5) -> int:
        """outro contador genérico"""
        u = timer[num][1]
        if timer[num][0] == 10:
            u = u2
        elif timer[num][0] == 20:
            u = u3
        elif timer[num][0] == 30:
            u = u4
        elif timer[num][0] == 40:
            u = u5
        elif timer[num][0] == 50:
            u = u1
            timer[num][0] = 0
        a = timer[num][0]
        a += 1
        timer[num][0] = a
        timer[num][1] = u
        return u
    






class Skeleton(Enemies):
    def __init__(self, x, y, index) -> None:
        """"param x: pos x
            param y: pos y
            param index: indíce do inimigo na lista de inimigos, usado para identificar"""
        super().__init__(x, y)
        self.w = 50
        self.h = 54
        self.v = 148
        self.x = x
        self.u = 0
        self.count = 0
        self.x1 = self.x + self.w
        self.y = y
        self.y1 = self.y + self.h
        self.bulletxi = self.x + self.w - 30
        self.bulletxf = self.bulletxi
        self.bullet_constant = -2
        self.bullety = self.y + 27
        self.b2 = False
        timer.append([0, 0])
        timer.append([0, 0])
        objectspos.append([self.x, self.x1, self.y, self.y1, True, False, index])
        self.skeltimeindex = len(timer) - 2
        self.bullettimeindex = len(timer) - 1
        bulletind.append(0)
        self.bulletindex =  len(bulletind) - 1
        bulletpos.insert(self.bulletindex, [0, 0, 0, 0, False, False])
        self.bultime = 0
        self.index = index
        





    def draw(self) -> None:
        """desenha o inimigo"""
        u = super().timer(self.skeltimeindex, 0, 51, 102, 153, 204)
        px.blt(self.x, self.y, 2, u, self.v, -1 * self.w, self.h, 0)
        self.bulletsDraw()






    def bulletsDraw(self) -> None:
        """desenha as espadas lançadas pelos esqueletos"""
        u = super().timer(self.bullettimeindex , 0, 26, 52, 78, 105)
        if not self.bultime == 30:
            self.bulletxf += self.bullet_constant
            px.blt(self.bulletxf, self.bullety, 2, u, 206, 25, 25, 0)
            bulletpos.pop(self.bulletindex)
            bulletpos.insert(self.bulletindex, [self.bulletxf + 25, self.bulletxf, self.bullety, self.bullety + 25])
            self.bultime += 1
        else:
            self.bultime = 0





    def pop(self, x, y) -> None:
        """Exclui os inimigos"""
        objectspos.remove([self.x, self.x1, self.y, self.y1, True, False, self.index])
        self.count = 0
        self.__init__(x, y, self.index)







class LifeBar:
    """classe usada para definir o hp do jogador"""
    def __init__(self, vidas: int) -> None:
        """param vidas: número de vidas"""
        self.vidas = vidas
        self.vidalos = 0
        self.camerax = 0
        self.die = False
        self.colort = 0





    def randcolor(self) -> int:
        """randomizador de cor"""
        self.colort += 0.25
        if self.colort == 16:
            self.colort = 0
        color = px.floor(self.colort)
        return color






    def draw(self) -> None:
        """desenha as vidas e também procede com a morte do jogador e o restart do jogo."""
        global MapStart, score, lastscore, EndGame, GameRestart
        if self.vidas == 0:
            MapStart = False
            EndGame = True
            if px.btnp(px.KEY_F):
                GameRestart = True
            lastscore = score
            bestplay()
            px.cls(0)
            px.rectb(self.camerax + 100, 86, 132, 48, self.randcolor())
            px.text(self.camerax + 105, 106, "You died, press F to play again", self.randcolor())
            px.text(self.camerax + 120, 200, f"Seu score foi: {score}", 7)
            px.text(self.camerax + 120, 225, f"Sua melhor jogada foi: {scoremax}", 7)
        else:
            for numero in range(self.vidas + self.vidalos):
                px.blt(12*(numero+1) + self.camerax, 3, 0, 140, 5, 12, 10, 5)
            for numero in range(self.vidas):
                px.blt(12*(numero+1) + self.camerax, 3, 0, 125, 5, 12, 10, 5)







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
        self.randn = -40
        self.randn0 = -40
        self.randn1 = -40
        self.randn2 = - 40
        self.randn3 = -40
        self.randn4 = -40
        self.skel = Skeleton(-300, 166, 0)
        self.skel1 = Skeleton(-450, 166, 1)
        self.skel2 = Skeleton(-600, 166, 2)
        self.skel3 = Skeleton(-700, 33, 3)
        self.skel4 = Skeleton(-400 , 22, 4)
        self.enemyconst = 0
    




    def enemyrate(self) -> None:
        """a frequência com que os inimigos aparecem se conecta com o multiplicador
        que é incrementado conforme o tempo"""
        if multiplier <= 48:
            self.enemyconst = px.ceil(multiplier * 10)
        else:
            self.enemyconst = 480

    




    def flame(self) -> None:
        """anima a fumaça que está sobre a fogueira na tela inicial"""
        self.stage = self.time/2 
        if self.time == 120:
            self.time = 0
        px.blt(160, 176, 0, 158 + self.stage, 0, 11, 20, 5)
        self.time += 1







    def gamebackground(self, camerax) -> None:
            """desenha o background"""
            self.camerax = camerax
            if self.timer == 0:
                self.staticx = camerax
            self.timer += 1
            for draw in range(5):
                px.blt(self.staticx + (draw * 160), 0,1, 0, 0, 160, 240)
            if self.timer == 240:
                self.timer = 0
                





    def pressStart(self) -> None:
        """desenha o startgame"""
        global MapStart
        self.colort += 0.25
        if self.colort == 16:
            self.colort = 0
        color = px.floor(self.colort)
        if not MapStart:
            px.rectb(100, 116, 120, 48, color)
            px.text(127, 136, "Press F to start", color)





            
    def drawStart(self, cam_x) -> None:
        """desenha as plataformas"""
        if MapStart:
            self.platform0.draw(cam_x)
            self.platform1.draw(cam_x)
            self.platform2.draw(cam_x)
            






    def spawnEnemies(self, cam_x) -> None:
        """Gera os inimigos"""            
        if  cam_x - 50 > self.randn:
            plat0 = choice(6, 86, 166)
            self.randn = px.rndi(cam_x + 320, cam_x + 700 - self.enemyconst)
            self.skel.pop(self.randn, plat0)
        if cam_x - 50 > self.randn0 and multiplier >= 5:
            plat1 = choice(6, 86, 166)
            self.randn0 = px.rndi(cam_x + 320, cam_x + 700 - self.enemyconst)
            self.skel1.pop(self.randn0, plat1)
        if cam_x - 50 > self.randn1 and multiplier >= 10:
            plat2 = choice(6, 86, 166, 166, 166)
            self.randn1 = px.rndi(cam_x + 320, cam_x + 700 - self.enemyconst)
            self.skel2.pop(self.randn1, plat2)
        if cam_x - 50 > self.randn2 and multiplier >= 20:
            plat3 = choice(6, 6, 6, 86, 166)
            self.randn2 = px.rndi(cam_x + 320, cam_x + 700 - self.enemyconst)
            self.skel3.pop(self.randn2, plat3)
        if cam_x - 50 > self.randn3 and multiplier >= 40:
            plat4 = choice(6, 86, 86, 86, 166)
            self.randn3 = px.rndi(cam_x + 320, cam_x + 700 - self.enemyconst)
            self.skel4.pop(self.randn2, plat4)

        self.skel.draw()
        self.skel1.draw()
        self.skel2.draw()
        self.skel3.draw()
        self.skel4.draw()
        
            

        






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







    def draw(self, camerax) -> None:
        """Desenha as plataformas no mapa e atualiza conforme o parâmetro camerax"""
        if self.timer == 0:
                self.staticx = camerax
        self.timer += 1
        for draw in range(self.range):
                px.blt(self.staticx + (draw * (self.draw_const)), self.y , 0, self.u, self.v, self.w, self.h, 5)
        if self.timer == 240:
                self.timer = 0
        