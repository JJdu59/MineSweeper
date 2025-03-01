import pygame, random, time

width, height = 1900, 1000

def main() -> None:
    pygame.init()
    
    menu = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Démajeur')
    
    run = True

    while run:
        pygame.display.update()

        #background
        pygame.draw.rect(menu, (36, 36, 36), pygame.Rect(0, 0, width, height))
        menu.blit(pygame.font.Font.render(pygame.font.SysFont("bahnschrift", 80), "DEMAJEUR", True, (255, 255, 255)), (width/2-205, 30))
        for i in range(5):
            pygame.draw.rect(menu, (0, 0, 0), pygame.Rect(width/2-200, 200+i*85, 400, 75))
            pygame.draw.rect(menu, (70, 70, 70), pygame.Rect(width/2-190, 210+i*85, 380, 55))
            menu.blit(pygame.font.Font.render(pygame.font.SysFont("bahnschrift", 36), ["easy", "medium", "hard", "gigachad", "quit"][i], True, (255, 255, 255)), (width/2-170, 210+i*85))
        
        for event in pygame.event.get():
            run = not event.type == pygame.QUIT
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = event.pos
                if width/2-200 <  mousePos[0] < width/2+200 and 200 <  mousePos[1] <275:
                    game("  easy  ")
                    run = False
                if width/2-200 <  mousePos[0] < width/2+200 and 285 <  mousePos[1] <360:
                    game(" medium ")
                    run = False
                if width/2-200 <  mousePos[0] < width/2+200 and 370 <  mousePos[1] <445:
                    game("  hard  ")
                    run = False
                if width/2-200 <  mousePos[0] < width/2+200 and 455 <  mousePos[1] <530:
                    game("gigachad")
                    run = False
                if width/2-200 <  mousePos[0] < width/2+200 and 540 <  mousePos[1] <635:
                    run = False

        pygame.display.update()

    pygame.quit()

def randomize(difficulty: tuple[int, int, int], coords: tuple[int, int]) -> list[list[list[str, bool, bool]]]:
    x, y, mines = difficulty
    x0, y0 = coords
    field = [[['0', False, False] for _ in range(x)] for _ in range(y)]
    '''for i in range(3):
        field[y0-1+i][x0-1+i][1] = True'''
    field[y0][x0][1]=True
    for _ in range(mines):
        while 1:
            rx = random.randint(0, x-1)
            ry = random.randint(0, y-1)
            if field[ry][rx][1] == True:
                break

            if field[ry][rx][0] != 'X':
                field[ry][rx][0] = 'X'
                try:
                    if rx > 0 and ry > 0:
                        field[ry-1][rx-1][0] = str(int(field[ry-1][rx-1][0])+1)
                except ValueError:
                    pass
                
                try:
                    if rx > 0:
                        field[ry][rx-1][0] = str(int(field[ry][rx-1][0])+1)
                except ValueError:
                    pass
                
                try:
                    if rx > 0 and ry < y-1:
                        field[ry+1][rx-1][0] = str(int(field[ry+1][rx-1][0])+1)
                except ValueError:
                    pass
                
                try:
                    if ry > 0:
                        field[ry-1][rx][0] = str(int(field[ry-1][rx][0])+1)
                except ValueError:
                    pass
                
                try:
                    if ry < y-1:
                        field[ry+1][rx][0] = str(int(field[ry+1][rx][0])+1)
                except ValueError:
                    pass
                
                try:
                    if rx < x-1  and ry > 0:
                        field[ry-1][rx+1][0] = str(int(field[ry-1][rx+1][0])+1)
                except ValueError:
                    pass

                try:
                    if rx < x-1:
                        field[ry][rx+1][0] = str(int(field[ry][rx+1][0])+1)
                except ValueError:
                    pass    
                try:
                    if rx < x-1 and ry < y-1:
                        field[ry+1][rx+1][0] = str(int(field[ry+1][rx+1][0])+1)
                except ValueError:
                    pass
                
                break
    
    rfield: list[list[list[str, bool, bool]]] = [[['' if field[iy][ix][0] == '0' else field[iy][ix][0], field[iy][ix][1],False] for ix in range(x)] for iy in range(y)]
    return rfield


def size(width: int, height: int, difficulty:tuple[int, int, int]) -> int:
    xmax = width/difficulty[0]
    ymax = (height-150)/difficulty[1]
    return(int(min(xmax, ymax)))

def verify(case: tuple[int, int], gridsize: tuple[int, int, int], field: list[list[list[str, bool, bool]]]) -> list[tuple[int, int]]:
    l = [case]
    xmax, ymax, _ = gridsize
    count=1
    while count != 0:
        count=0
        for case in l:
            if 0 <= case[1]-1 and field[case[1]-1][case[0]][0:2] == ['', False] and (case[0],case[1]-1) not in l:#haut
                l.append((case[0],case[1]-1))
                count+=1
            if case[0]+1 <xmax and field[case[1]][case[0]+1][0:2] == ['', False] and (case[0]+1,case[1]) not in l:#droite
                l.append((case[0]+1,case[1]))
                count+=1
            if case[1]+1 < ymax and field[case[1]+1][case[0]][0:2] == ['', False] and (case[0],case[1]+1) not in l:#bas
                l.append((case[0],case[1]+1))
                count+=1
            if 0 <= case[0]-1 and field[case[1]][case[0]-1][0:2] == ['', False] and (case[0]-1,case[1]) not in l:#gauche
                l.append((case[0]-1,case[1]))
                count+=1

            if 0 <= case[1]-1 and 0 <= case[0]-1 and field[case[1]-1][case[0]-1][0:2] == ['',False] and (case[0]-1,case[1]-1) not in l:#haut gauche
                l.append((case[0]-1,case[1]-1))
            if 0 <= case[1]-1 and case[0]+1 <xmax and field[case[1]-1][case[0]+1][0:2] == ['',False] and (case[0]+1,case[1]-1) not in l:#haut droite
                l.append((case[0]+1,case[1]-1))
            if case[1]+1 < ymax and case[0]+1 <xmax and field[case[1]+1][case[0]+1][0:2] == ['',False] and (case[0]+1,case[1]+1) not in l:#bas droite
                l.append((case[0]+1,case[1]+1))
            if case[1]+1 < ymax and 0 <= case[0]-1 and field[case[1]+1][case[0]-1][0:2] == ['',False] and (case[0]-1,case[1]+1) not in l:#bas gauche
                l.append((case[0]-1,case[1]+1))
    return(l)

def show(l: list[tuple[int, int]], field: list[list[list[str, bool, bool]]], gridsize: tuple[int, int, int]) -> tuple[list[list[list[str, bool, bool]]], list[tuple[int, int]]]:
    returned = []
    xmax, ymax, _ = gridsize
    for n in l:
        if 0<=n[1]-1:
            field[n[1]-1][n[0]][1] = True
            returned.append((n[1]-1, n[0]))
            if 0<=n[0]-1:
                field[n[1]-1][n[0]-1][1] = True
                returned.append((n[1]-1, n[0]-1))
            if n[0]+1<xmax:
                field[n[1]-1][n[0]+1][1] = True
                returned.append((n[1]-1, n[0]+1))
        if 0<=n[0]-1:
            field[n[1]][n[0]-1][1] = True
            returned.append((n[1], n[0]-1))
        if n[0]+1<xmax:
            field[n[1]][n[0]+1][1] = True
            returned.append((n[1], n[0]+1))
        if n[1]+1<ymax:
            field[n[1]+1][n[0]][1] = True
            returned.append((n[1]+1, n[0]))
            if 0<=n[0]-1:
                field[n[1]+1][n[0]-1][1] = True
                returned.append((n[1]+1, n[0]-1))
            if n[0]+1<xmax:
                field[n[1]+1][n[0]+1][1] = True 
                returned.append((n[1]+1, n[0]+1))
    return (field, returned)

def game(difficulty) -> None:

    difficulties = {
        "  easy  ":(8, 10, 10),
        " medium ":(14, 18, 40),
        "  hard  ":(20, 24, 99),
        "gigachad":(52, 30, 180)
    }
    
    pygame.init()

    field: list[list[list[str, bool, bool]]] = []
    game = pygame.display.set_mode((width, height))

    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.mixer.init()
    loser = pygame.mixer.Sound("assets/loser.ogg")
    loser2 = pygame.mixer.Sound("assets/loser2.mp3")
    loser.set_volume(4269)
    loser2.set_volume(4269)

    clock = pygame.time.Clock()

    mineleft = difficulties[difficulty][2]

    run = True
    time0 = time.time()
    _size = size(width, height, difficulties[difficulty])

    pygame.draw.rect(game, (36, 36, 36), pygame.Rect(0, 0, width, height))
    game.blit(pygame.font.Font.render(pygame.font.SysFont("bahnschrift", 50), 'Mines restantes: '+str(mineleft), True, (255, 255, 255)), (20, 40))

    for y in range(difficulties[difficulty][1]):
        for x in range(difficulties[difficulty][0]):
            pygame.draw.rect(game, (0, 0, 0), pygame.Rect((width-difficulties[difficulty][0]*_size)/2+_size*x, 150+_size*y, _size, _size))
            pygame.draw.rect(game, (70, 70, 70), pygame.Rect((width-difficulties[difficulty][0]*_size)/2+_size*x+2, 150+_size*y+2, _size-4, _size-4))

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                main()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = event.pos
                case = (int((mousePos[0]-(width-difficulties[difficulty][0]*_size)/2))//_size, (mousePos[1]-150)//_size)
                
                if field == [] and 0 <= case[0] < difficulties[difficulty][0] and 0 <= case[1] < difficulties[difficulty][1]:
                    field = randomize(difficulties[difficulty], case)
                if 0 <= case[0] < difficulties[difficulty][0] and 0 <= case[1] < difficulties[difficulty][1] and event.button == 1:
                    x, y = case
                    field[case[1]][case[0]][1] = True
                    uncover = sum([i for sublist in [[j[1] for j in k] for k in field] for i in sublist])
                    pygame.draw.rect(game, (100, 100, 100), pygame.Rect((width-difficulties[difficulty][0]*_size)/2+_size*x+2, 150+_size*y+2, _size-4, _size-4))
                    game.blit(pygame.font.Font.render(pygame.font.SysFont("bahnschrift", int(_size*0.8)), field[y][x][0], True, (255, 255, 255)), ((width-difficulties[difficulty][0]*_size)/2+_size*x+_size//3, 150+_size*y))
                    if field[case[1]][case[0]][0] == 'X':
                        loser2.play()
                        win=0
                        run = False
                        break
                    if field[case[1]][case[0]][0] == '':
                        field, lst = show(verify(case,difficulties[difficulty],field),field,difficulties[difficulty])
                        for i in lst:
                            y, x = i
                            pygame.draw.rect(game, (0, 0, 0), pygame.Rect((width-difficulties[difficulty][0]*_size)/2+_size*x, 150+_size*y, _size, _size))
                            if field != [] and field[y][x][1] == True:
                                pygame.draw.rect(game, (100, 100, 100), pygame.Rect((width-difficulties[difficulty][0]*_size)/2+_size*x+2, 150+_size*y+2, _size-4, _size-4))
                                game.blit(pygame.font.Font.render(pygame.font.SysFont("bahnschrift", int(_size*0.8)), field[y][x][0], True, (255, 255, 255)), ((width-difficulties[difficulty][0]*_size)/2+_size*x+_size//3, 150+_size*y))
                            else:
                                pygame.draw.rect(game, (70, 70, 70), pygame.Rect((width-difficulties[difficulty][0]*_size)/2+_size*x+2, 150+_size*y+2, _size-4, _size-4))
                    if uncover == difficulties[difficulty][0] * difficulties[difficulty][1] - difficulties[difficulty][2]:
                        win=1
                        run = False
                        break
                    
                if 0 <= case[0] < difficulties[difficulty][0] and 0 <= case[1] < difficulties[difficulty][1] and event.button == 3:
                    field[case[1]][case[0]][2] = not field[case[1]][case[0]][2]
                    x, y = case
                    if field != [] and field[y][x][1] == False and field[y][x][2]==True:
                        game.blit(pygame.transform.scale(pygame.image.load("assets/flag.png"),(_size-4,_size-4)), ((width-difficulties[difficulty][0]*_size)/2+_size*x+2, 150+_size*y+2))
                    elif field != [] and field[y][x][1] == False:
                        pygame.draw.rect(game, (70, 70, 70), pygame.Rect((width-difficulties[difficulty][0]*_size)/2+_size*x+2, 150+_size*y+2, _size-4, _size-4))
                mineleft = difficulties[difficulty][2]-sum([i for sublist in [[(not j[1] and j[2]) for j in k] for k in field] for i in sublist])

        # debut affichage
        clock.tick(60)
        pygame.display.update()
        pygame.draw.rect(game, (36, 36, 36), pygame.Rect(0, 0, width, 150))
        fpsTxt = pygame.font.Font.render(pygame.font.SysFont("bahnschrift", 23), str(int(clock.get_fps())), True, (255, 255, 255))
        game.blit(fpsTxt, (0, 0))
        game.blit(pygame.font.Font.render(pygame.font.SysFont("bahnschrift", 50), 'Mines restantes: '+str(mineleft), True, (255, 255, 255)), (20, 40))
        game.blit(pygame.font.Font.render(pygame.font.SysFont("bahnschrift", 80), difficulty, True, (255, 255, 255)), (width/2-205, 30))
        game.blit(pygame.font.Font.render(pygame.font.SysFont("bahnschrift", 50), f'{round((time.time()-time0))//60//10}{round((time.time()-time0))//60%10}:{round((time.time()-time0))%60//10}{round((time.time()-time0))%60%10}', True, (255, 255, 255)), (width-350, 40))
    
        # fin affichage

    run = True
    while run:
        pygame.display.update()
        pygame.draw.rect(game, (0, 0, 0), pygame.Rect((width-600)//2, 100, 600, 800))
        pygame.draw.rect(game, (36, 36, 36), pygame.Rect((width-600)//2+5, 100+5, 590, 790))
        game.blit(pygame.font.Font.render(pygame.font.SysFont("bahnschrift", 100), ['GAME OVER','   GG BRO!'][win], True, (255, 255, 255)), ((width-600)//2+20, 100))

        pygame.draw.rect(game, (0, 0, 0), pygame.Rect((width-400)/2, 800, 400, 75))
        pygame.draw.rect(game, (70, 70, 70), pygame.Rect((width-400)/2+5, 805, 390, 65))
        game.blit(pygame.font.Font.render(pygame.font.SysFont("bahnschrift", 50), 'QUIT', True, (255, 255, 255)), ((width-400)/2+150, 805))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                main()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = event.pos
                if abs(mousePos[0]-width/2)<200 and abs(mousePos[1]-837.5)<37.5:
                    main()
                    run = False
        
main()
