from random import randint, choice
from time import time, sleep
from copy import deepcopy
import keyboard


class Tetris () :
    
    
    hauteur = 20
    largeur = 10
    bonus_clean = 5
    auto_fall = 1
    
    
    def __init__(self) :
        self.plateau = list(self.largeur * [False] for k in range(self.hauteur))
        self.score = 0
        self.prev_scores = None
        self.running = True
        self.username = "Undefined"

    
    
    def dep_right (self) : 
        # verifie la possibilite d'un deplacement vers la droite
        for x, y in self.falling.right_side() :
            if x + 1 >= self.largeur or not not self.plateau[y][x + 1] :
                return False
        return True
    
    def dep_left (self) :
        # verifie la possibilite d'un deplacement vers la gauche
        for x, y in self.falling.left_side() :
            if x - 1 < 0 or not not self.plateau[y][x - 1] :
                return False
        return True
    
    def dep_down (self) :
        # verifie la possibilite d'un deplacement vers le bas
        for x, y in self.falling.down_side() :
            if y + 1 >= self.hauteur or (y >= 0 and not not self.plateau[y + 1][x]):
                print(self.falling.down_side())
                return False
        return True
    
    def dep_turn (self, plan_block) :
        # verifie la possibilite d'une rotation
        for x,y in plan_block :
            if 0 > self.falling.posx + x >= self.largeur or self.falling.posy + y >= self.hauteur or not (self.falling.posy + y < 0 or not self.plateau[y + self.falling.posy][x + self.falling.posx]) :
                return False
        return True 
    
    
    def fix (self) :
        # ancre le bloc en chute au plateau
        for x, y in self.falling.r_list :
            if self.falling.posy + self.falling.midy + y < 0 :
                self.running = False
            else :
                self.plateau[self.falling.posy + self.falling.midy + y][self.falling.posx + self.falling.midx + x] = self.falling.color
                self.score += 1
        self.falling.block = list([False] * 5 for k in range(5))
                
            
    def clean_line (self) :
        # efface les lignes lorsqu'elles sont entierement completees
        for y in range(self.hauteur - 1, -1, -1) :
            clean = True
            while clean :
                for x in range (self.largeur) :
                    if not self.plateau[y][x] :
                        clean = False
                if clean :
                    for x in range (self.largeur) :
                        self.plateau[y][x] = False
                        self.print_plateau()
                        sleep(0.1)
                    for ybis in range(y,-1,-1):
                        for x in range (self.largeur) :
                            if ybis == 0 :
                                self.plateau[ybis][x] = False
                            else :
                                self.plateau[ybis][x] = self.plateau[ybis - 1][x]
                    self.print_plateau()
                    self.score += self.bonus_clean 
                
                
    def fall (self) :
        # boucle de la chute d'un block
        # pas encore valide a cause de problemes avec le module keyboard
        self.falling = Block()
        while self.dep_down():
            free_fall = False
            deb = time()
            while time() - deb < self.auto_fall or free_fall :
                if keyboard.is_pressed("left") and self.dep_left() :
                    self.falling.posx -= 1
                    self.print_game()
                    sleep(0.1)
                    
                if keyboard.is_pressed("right") and self.dep_right() :
                    self.falling.posx += 1     
                    self.print_game()
                    sleep(0.1)
                    
                if keyboard.is_pressed("up") :
                    plan_list, plan_block = self.falling.rotate_plans()
                    if self.dep_turn(plan_block)  :
                        self.falling.rotate(plan_list, plan_block)
                        self.print_plateau()
                        sleep(0.1)
                    
                if keyboard.is_pressed("down") :
                    free_fall = True
                    sleep(0.1)
                if self.dep_down() :
                    self.falling.posy += 1
                    self.print_plateau()
        self.fix()
    
    def fall_test (self) :
        # boucle de la chute d'un block
        # modele plus simple a gerer, sans module, mais peu convaincant
        self.falling = Block()
        sleep(0.1)
        while self.dep_down():
            free_fall = False
            sleep(0.3)
            resp = input("Next Move -> ")
            if (resp == "l" or resp == "q") and self.dep_left() :
                self.falling.posx -= 1
                self.print_plateau()
                sleep(0.1)
                
            if (resp == "r" or resp == "d") and self.dep_right() :
                self.falling.posx += 1
                self.print_plateau()
                sleep(0.1)
                
            if resp == "u" or resp == "z":
                plan_list, plan_block = self.falling.rotate_plans()
                if self.dep_turn(plan_block)  :
                    self.falling.rotate(plan_list, plan_block)
                    self.print_plateau()
                    sleep(0.1)    
                    
            if resp == "d" or resp == "s":
                free_fall = True
                sleep(0.1)
                
            self.falling.posy += 1
            self.print_plateau()
        print(self.falling.posy, "y pré fix")
        self.fix()
        sleep(0.2)
        
        
    def play (self) :
        # debute une nouvelle partie
        self.running = True
        while self.running :
            self.fall_test()
            self.clean_line()
        print(self.score)
                    
    
    def add_score (self) :
        # ajoute le score effectue a la sauvegarde
        i = 0
        while i < len(self.prev_scores) and self.score <= self.prev_scores[i][0] :
            i += 1
        for k in range(len(self.prev_scores) - i) :
            pass
        
    def print_plateau (self) :
        # affiche le plateau sur la console
        n_plateau = deepcopy(self.plateau)
        for x in range (5):
            for y in range (5) :
                if self.falling.block[y][x] and self.falling.posy + y >= 0 :
                    n_plateau[self.falling.posy + y][self.falling.posx + x] = self.falling.color
                    
        mess = "\n\n" + Color.erase + Color.d
        
        for _ in range(2) :
            mess += (self.largeur + 2) * "    " + "\n"
            
        for y in range(self.hauteur) :
            for _ in range(2) :
                mess += Color.d + "    "
                for x in range(self.largeur) :
                    if not not (n_plateau[y][x]) :
                        mess += n_plateau[y][x] + "    "
                    else :
                        mess += Color.clear + "    "
                mess += Color.d + "    \n"
                
        for _ in range(2) :
            mess += (self.largeur + 2) * "    " + "\n"
        print(mess)
        
    def test_anim(self) :
        # effectue une courte animation, pour verification du bon fonctionnement
        for x in range(self.largeur) :
            for y in range (self.hauteur) :
                self.print_plateau()
                sleep(0.01)
                self.plateau[y][x] = choice([Color.r, Color.g, Color.b, Color.c, Color.y, Color.m, Color.w])
                

            

class Block () :
    
    mode = 2  #[0 = Random, 1 = Revisité, 2 = Original]
    
    def __init__(self) :
        self.block = choice([[self.rand_block],
                             [self.line_block, self.rand_block, self.rect_block, self.tri_block],
                             [self.c_line_block, self.c_square_block, self.c_boat_block, self.c_L_block, self.c_L_block, self.c_ramp_block, self.c_ramp_block]][self.mode])()
        self.find_mid()
        self.find_relative_list()
        self.posy = -4
        self.posx = 3
        self.color = choice([Color.r, Color.g, Color.b, Color.c, Color.y, Color.m, Color.w])
        
    def print_spec (self) :
        # affiche les caracteristiques du block
        self.print()
        print(self.posx, self.posy, self.r_list, self.block,sep = "\n")
        
    # Definition des differents blocks possibles
    # 'c_' designant un block de la version classique
    
    def c_square_block (self) :
        print("Square Block")
        blo = list([False] * 5 for k in range(5))
        blo[2][2], blo[2][1], blo[1][1], blo[1][2] = True, True, True, True
        return blo
        
    def c_boat_block (self) :
        print("Boat Block")
        blo = list([False] * 5 for k in range(5))
        blo[2][2], blo[2][1], blo[2][3], blo[1][2] = True, True, True, True
        return blo
        
    def c_ramp_block (self) :
        orien = choice([-1,1])
        if orien == 1 :
            printation = ""
        else :
            printation = "Reversed"
        print(printation, "Ramp Block")
        blo = list([False] * 5 for k in range(5))
        for i in range(2) :
            for j in range(2) :
                blo[2 + j - i][2 + i * orien] = True
        return blo
    
    def c_L_block (self) :
        orien = choice([-1,1])
        if orien == 1 :
            printation = ""
        else :
            printation = "Reversed"
        print(printation, "L Block")
        blo = list([False] * 5 for k in range(5))
        for i in range(3) :
            blo[2][1+i] = True
        blo[2 + orien][3] = True
        return blo

    def c_line_block (self):
        print("Ligne Block")
        blo = list([False] * 5 for k in range(5))
        for i in range(-2, 2) :
            blo[i + 2][2] = True
        return blo
    
    def tri_block (self) :
        print("Small tri block")
        blo = list([False] * 5 for k in range(5))
        blo[2][2], blo[2][1], blo[1][2] = True, True, True
        return blo
    
        
    def rand_block (self):
        print("Random Block")
        blo = list([False] * 5 for k in range(5))
        blo[2][2] = True
        blo_In = [[2,2]]
        for i in range(randint(1,7)):
            good = False
            while not good :
                link = choice(blo_In)[:]
                link[randint(0,1)] += choice([-1,1])
                if 0 <= link[0] < 5 and 0 <= link[1] < 5 and not link in blo_In :
                    blo[link[0]][link[1]] = True
                    blo_In.append(link) 
                    good = True 
        return blo
    
    def line_block (self):
        print("Ligne Block")
        blo = list([False] * 5 for k in range(5))
        length = choice ([1,2])
        for i in range(-length, length + 1) :
            blo[i + 2][2] = True
        return blo
           
    def rect_block (self): 
        print("Rectangle Block")
        blo = list([False] * 5 for k in range(5))
        jchoice = choice([2,3])
        for i in range(choice([2,3])) :
            for j in range(jchoice) :
                blo[1+i][1+j] = True
        return blo
    
    def tri_block (self):
        print("Triangle Block")
        blo = list([False] * 5 for k in range(5))
        for i in range(choice([1,2])) :
            blo[2+i][2] = True
            blo[2][2+i] = True
        return blo
        
        
    def find_mid (self):
        # determine le point central d'un block
        sum_i, sum_j, tot = 0, 0, 0
        for i in range(5) :
            for j in range(5) :
                if self.block[i][j] :
                    tot += 1
                    sum_i += i
                    sum_j += j
        self.midy = int (sum_i / tot + 0.4999)
        self.midx = int (sum_j / tot + 0.4999)
        
    def find_relative_list (self):
        # determine la liste des coordonnes des points du block avec pour origine le point central
        lis = []
        for y in range(5) :
            for x in range(5) :
                if self.block[y][x] :
                    lis.append((x - self.midx, y - self.midy))
        self.r_list = lis
        
    def rotate_plans (self) :
        # effectue les plans de la rotation du block
        fut_r_list = []
        fut_block = []
        for (x,y) in self.r_list :
            fut_r_list.append((-y,x))
            fut_block.append((self.midx - y,self.midy + x))
        return fut_r_list, fut_block
    
    def rotate (self, plan_list, plan_block) :
        # effectue la rotation du block
        self.r_list = plan_list
        blo = list([False] * 5 for k in range(5))
        for (x,y) in plan_block :
            blo[y][x] = True
        self.block = blo
        
    def left_side (self) :
        # renvoie la liste des coordonnees des points situes a la frontiere gauche
        lis = []
        for x in range(5):
            for y in range(5) :
                if self.block[y][x] :
                    lis.append((self.posx + x,self.posy + y))
                    break
        return lis
                
        
    def right_side (self) :
        # renvoie la liste des coordonnees des points situes a la frontiere droite
        lis = []
        for y in range(5):
            for x in range(4,-1,-1) :
                if self.block[y][x] :
                    lis.append((self.posx + x,self.posy + y))
                    break
        return lis
        
    def down_side (self) :
        # renvoie la liste des coordonnees des points situes a la frontiere du bas
        lis = []
        for x in range(5) :
            for y in range(4) :
                if self.block[y][x] and not self.block[y + 1][x] :
                    lis.append((self.posx + x,self.posy + y))
            if self.block[4][x] : 
                lis.append((self.posx + x, self.posy + 4))
        return lis
                
    def print_n (self) :
        # affichage peu satisfaisant de la structure du block
        mes = "-"*7 + "\n"
        for i in range(5) :
            mes += "|"
            for j in range(5) :
                if self.block[i][j] :
                    add = '▩' 
                else : 
                    add = " "
                mes += add
            mes += "|\n"
        mes += "-"*7
        print(mes)
        
    def print (self) :
        # affichage satisfaisant de la structure d'un block
        mess = "\n\n" + Color.d
        for _ in range(2) :
            mess += 7 * "    " + "\n"
            
        for y in range(5) :
            for _ in range(2) :
                mess += Color.d + "    "
                for x in range(5) :
                    if not not (self.block[y][x]) :
                        mess += self.color + "    "
                    else :
                        mess += Color.clear + "    "
                mess += Color.d + "    \n"
                
        for _ in range(2) :
            mess += 7 * "    " + "\n"
        print(mess)
        
        



class Color():
    d = '\033[40m'
    r = '\033[41m'
    g = '\033[42m'
    y = '\033[43m'
    b = '\033[44m'
    m = '\033[45m'
    c = '\033[46m'
    w = '\033[47m'
    UNDERLINE = '\033[4m'
    clear = '\033[0m'
    erase = '\033[2J\033[1;1H'
    
    

        

