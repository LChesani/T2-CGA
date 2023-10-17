import pygame as pg
import random
import sympy

#funcao que cria n pontos randomicos e retorna

W = H = 1000
gap = 50
def pontos(n):
    pontos = []
    for i in range(n):
        x, y = random.randint(gap, W-gap), random.randint(gap, H-gap)
        
        pontos.append([x, y])
    return pontos

#cria curvas entre os pontos

#desenha curvas b spline entre os pontos
def curva(pontos):
    retas = [] #lista de retas que resume as curvas
    for i in range(len(pontos)-3):
        p0 = pontos[i]
        p1 = pontos[i+1]
        p2 = pontos[i+2]
        p3 = pontos[i+3]
        
        for t in range(0, 100, 1):
            t = t/100
            
            x = int((-t**3 + 3*t**2 - 3*t + 1)*p0[0]/6 + (3*t**3 - 6*t**2 + 4)*p1[0]/6 + (-3*t**3 + 3*t**2 + 3*t + 1)*p2[0]/6 + t**3*p3[0]/6)
            y = int((-t**3 + 3*t**2 - 3*t + 1)*p0[1]/6 + (3*t**3 - 6*t**2 + 4)*p1[1]/6 + (-3*t**3 + 3*t**2 + 3*t + 1)*p2[1]/6 + t**3*p3[1]/6)
          
            retas.append([x, y])
    return retas


#inicializa o pygame
def init():
    pg.init()
    screen = pg.display.set_mode((W, H))
    pg.display.set_caption("T2")
    return screen

def preenche(screen, pontos):
    for i in pontos:
        pg.draw.circle(screen, (255, 0, 0), (i[0], i[1]), 2)

def upd(circ_list, r, segmentos):
    while True:
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_0:
                    orderna_forca_bruta(circ_list, r, segmentos)
                if event.key == pg.K_1:
                    ordena_hash(circ_list, r, hash_table(segmentos))
                if event.key == pg.K_2:
                    circulos.clear()
                    for _ in range(25):
                        circulos.append(gera_circulos(tamanho, seg))

            
            if event.type == pg.QUIT:
                pg.quit()
                exit(0)

def desenha_curvas(pontos, color):
    for i in range(len(pontos)-1):
        pg.draw.line(screen, color, (pontos[i][0], pontos[i][1]), (pontos[i+1][0], pontos[i+1][1]), 1)

def seg_retas(pontos): #discretiza os pontos de controle para gerar reta entre eles
    retas = []
    for i in range(0, len(pontos), 20):
        retas.append(pontos[i])


    return retas


def interseccao_circulo_reta(p0, p1, circulo, r):
    if (p0[0] < circulo[0]-r and p1[0] < circulo[0]-r) or (p0[0] > circulo[0]+r and p1[0] > circulo[0]+r) or (p0[1] < circulo[1]-r and p1[1] < circulo[1]-r) or (p0[1] > circulo[1]+r and p1[1] > circulo[1]+r):
        return False
    e = 0.0000001
    x, y = sympy.symbols('x y', real=True)
    circ = sympy.Eq(((x - circulo[0])**2) + ((y - circulo[1])**2), r**2) #equacao do circulo
    m = (p1[1]-p0[1])/(p1[0]-p0[0]+e) #coeficiente angular da reta
    reta = sympy.Eq(y - p0[1], m*(x - p0[0])) #equacao da reta
    return sympy.solve((circ, reta), (x, y))


def gera_circulos(r, pontos): #gera n circulos que nao estao em segmentos de retas entre os pontos
    x = random.randint(gap, W-gap)
    y = random.randint(gap, H-gap)

    j = 0
    while j < (len(pontos)-1):

        if not interseccao_circulo_reta(pontos[j], pontos[j+1], (x, y), r):
            j+=1
        else:
            return x, y, False
    return x, y, True
    
def orderna_forca_bruta(circ_list, r, segmentos):
    i = 0
    while i < len(circ_list):
        if not circ_list[i][2]: #se o circulo estiver em cima de um ponto da curva
            x, y = random.randint(gap, W-gap), random.randint(gap, H-gap)
            j = 0
            while j < (len(segmentos)-1):
                if not interseccao_circulo_reta(segmentos[j], segmentos[j+1], (x, y), r):
                    j+=1
                else:
                    j = 0
                    x, y = random.randint(gap, W-gap), random.randint(gap, H-gap)
            circ_list[i] = (x, y, True)
        i+=1



dim = 3
scr_dim = W//dim
def hash_table(segmentos):
    table = [[] for _ in range(dim*dim)]
    for i in range(1, len(segmentos)-1):
        p0 = segmentos[i]
        p1 = segmentos[i+1]

        table[(p0[0]//scr_dim)*dim + p0[1]//scr_dim].append((p0, p1))
        table[(p1[0]//scr_dim)*dim + p1[1]//scr_dim].append((p0, p1))



    return table

def ordena_hash(circ_list, r, table):
    i = 0
    while i < len(circ_list):
        if not circ_list[i][2]: #se o circulo estiver em cima de um ponto da curva
            x, y = random.randint(gap, W-gap), random.randint(gap, H-gap)
            
            index = (x//scr_dim)*dim + y//scr_dim

            j = 0
            while j < len(table[index]):
                indexes = [(x//scr_dim)*dim + y//scr_dim]

                for index in indexes:
                    if len(table[index]) == 0:
                        continue
                    if not interseccao_circulo_reta(table[index][j][0], table[index][j][1], (x, y), r):
                        j+=1
                    else:
                        j = 0
                        x, y = random.randint(gap, W-gap), random.randint(gap, H-gap)
            circ_list[i] = (x, y, True)
        i+=1
    
    

if __name__ == '__main__':
    screen = init()
    pontos = pontos(200)
    #preenche(screen, pontos)

    pontos_curva = curva(pontos)
    #desenha_curvas(pontos_curva, (0, 0, 255))
    
    seg = seg_retas(pontos_curva)
    tamanho = 5
    desenha_curvas(seg, (0, 255, 0))
    circulos = []
    for i in range(25):
        circulos.append(gera_circulos(tamanho, seg))


    for i in circulos:
        color = (255, 0, 255) if i[2] else (255, 255, 0)
        pg.draw.circle(screen, color, (i[0], i[1]), tamanho)

    upd(circulos, tamanho, seg)
