import pygame
import random
import copy

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
BLUE     = (   0,   0, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)

blocksize=30
dimension=[20,10]
size = [blocksize*(dimension[1]+7), blocksize*(dimension[0]+1)]

list_of_tetris=[
    [[-2,-1],[-1,-1],[0,-1],[0,0]],
    [[1,-1],[0,-1],[-1,-1],[-1,0]],
    [[0,0],[0,-1],[-1,-1],[-1,0]],
    [[0,0],[0,-1],[1,-1],[-1,0]],
    [[0, 0], [-2, -1], [-1, -1], [-1, 0]],
    [[-2, -1], [-1, -1], [0, -1],[1,-1] ],
    [[1,0], [0,0], [-1, 0], [0, -1]]
]

different_shapes=len(list_of_tetris)

def set_to_the_beginning():
    return  int(dimension[1]//2),  0, 0

def check_and_delete_bottom_blocks_and_increase_count_and_y_speed(bottom_blocks, count, y_speed):
    for i in range(dimension[0]):
        index = 0
        for j in range(dimension[1]):
            if bottom_blocks.blocks[j][i] == 0:
                index = 1
        if index == 0:
            bottom_blocks.kill(i)
            count += 1
            if count % 3 == 0:
                y_speed += 0.1
    return bottom_blocks, count, y_speed

def print_initial_message(screen):
    font = pygame.font.SysFont('Calibri', blocksize * 3, True, False)
    text5 = font.render("Press Enter", True, BLUE)
    text6 = font.render("to continue", True, BLUE)
    screen.blit(text5, [int(50 * (blocksize / 25)), int(150 * (blocksize / 25))])
    screen.blit(text6, [int(50 * (blocksize / 25)), int(250 * (blocksize / 25))])

def print_scoreboard(screen, count):
    font = pygame.font.SysFont('Calibri', blocksize, True, False)
    text1 = font.render("SCORE", True, BLACK)
    text2 = font.render(str(count), True, BLACK)
    text3 = font.render("LEVEL", True, BLACK)
    text4 = font.render(str(count // 2), True, BLACK)
    screen.blit(text1, [blocksize * (dimension[1] + 1), blocksize * 1])
    screen.blit(text2, [blocksize * (dimension[1] + 1), blocksize * 4])
    screen.blit(text3, [blocksize * (dimension[1] + 1), blocksize * 7])
    screen.blit(text4, [blocksize * (dimension[1] + 1), blocksize * 10])

def draw_background(screen):
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, [0,0, blocksize*dimension[1],blocksize*dimension[0]])
    for i in range(dimension[0]+1):
        pygame.draw.line(screen, GREEN, [0, i*blocksize], [dimension[1]*blocksize, i*blocksize], 1)
    for i in range(dimension[1]+1):
        pygame.draw.line(screen, GREEN, [i*blocksize, 0], [i*blocksize, dimension[0]*blocksize], 1)


def setup_drops(tetris_lookahead):
    tetris_lookahead.append(random.randrange(0, different_shapes))
    tetris_piece = tetris(list_of_tetris[tetris_lookahead[0]])
    tetris_lookahead.pop(0)
    tetris_future = tetris(list_of_tetris[tetris_lookahead[0]])
    return tetris_lookahead, tetris_piece, tetris_future

class bottom:

    def __init__(self):
        self.blocks=[]
        for i in range(dimension[1]):
            self.blocks.append([])
            for j in range(dimension[0]):
                self.blocks[i].append(0)
            self.blocks[i].append(1)

    def draw(self, screen, color):
        for i in range(dimension[1]):
            for j in range(dimension[0]):
                if self.blocks[i][j] != 0:
                    temp=[i,j,1,1]
                    temp=[x * blocksize for x in temp]
                    pygame.draw.rect(screen, color, temp)

    def insert(self,tet):
        for i in range(4):
            if tet.shape_position[i][0]>=0 and tet.shape_position[i][1]>=0:
                self.blocks[tet.shape_position[i][0]][tet.shape_position[i][1]] =1

    def kill(self,i):
        for j in range(dimension[1]):
            for k in range(0,i):
                self.blocks[j][i-k]=self.blocks[j][i-1-k]
            self.blocks[j][0] = 0

class tetris:

    def __init__(self, shape):
        self.shape=shape
        self.pos=[0,0]
        self.shape_position=copy.deepcopy(self.shape)

    def  update_shapeposition(self):
        for i in range(4):
            for j in range(2):
                self.shape_position[i][j]=self.shape[i][j]+self.pos[j]

    def rotation(self):
        temp=copy.deepcopy(self)
        for i in range(4):
            temp.shape[i][0]=self.shape[i][1]
            temp.shape[i][1]=-self.shape[i][0]-1
        temp.update_shapeposition()
        return temp

    def position(self, x,y):
        temp=copy.deepcopy(self)
        temp.pos=[x,y]
        temp.update_shapeposition()
        return temp

    def draw(self, screen, color):
        for i in range(4):
            temp=self.shape_position[i]+[1,1]
            temp=[x * blocksize for x in temp]
            pygame.draw.rect(screen, color, temp)

    def future_draw(self,screen,color,coordinates):
        for i in range(4):
            temp=[self.shape[i][0]+coordinates[0],self.shape[i][1]+coordinates[1]]
            temp=temp+[1,1]
            temp=[x * blocksize for x in temp]
            pygame.draw.rect(screen, color, temp)


    def collision_R(self,x,y,bottom_stack):
        temp=self.position(x,y)
        index=0
        for i in range(4):
            if temp.shape_position[i][0]>=dimension[1]:
                index=1
                break
            elif temp.shape_position[i][0]>=0 and temp.shape_position[i][1]>=0:
                if bottom_stack.blocks[temp.shape_position[i][0]][temp.shape_position[i][1]] == 1:
                    index = 1
                    break
        if index==1:
            return True
        else:
            return False

    def collision_L(self,x,y,bottom_stack):
        temp=self.position(x,y)
        index=0
        for i in range(4):
            if temp.shape_position[i][0]<=-1:
                index=1
                break
            elif temp.shape_position[i][0] >= 0 and temp.shape_position[i][1] >= 0:
                if bottom_stack.blocks[temp.shape_position[i][0]][temp.shape_position[i][1]] == 1:
                    index = 1
                    break
        if index==1:
            return True
        else:
            return False

    def collision_bottom_stack(self,x,y,bottom_stack):
        temp = self.position(x, y)
        index=0
        for i in range(4):
            if temp.shape_position[i][0]>=0 and temp.shape_position[i][1]>=0:
                if bottom_stack.blocks[temp.shape_position[i][0]][temp.shape_position[i][1]]==1:
                    index=1
        if index == 1:
            return True
        else:
            return False

def main():

    pygame.init()

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(0)

    done = False
    while not done:
        print_initial_message(screen)
        pygame.display.flip()
        clock.tick(1)

        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop:
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    dead = False

                    x_speed, y_speed = 0, 0.1
                    x_coord, y_coord, y_coord_for_showing = set_to_the_beginning()

                    tetris_lookahead=[random.randrange(0, different_shapes)]
                    tetris_lookahead, tetris_piece, tetris_future=setup_drops(tetris_lookahead)

                    bottom_blocks = bottom()
                    count = 0

                    while not dead:
                        for event in pygame.event.get():  # User did something
                            if event.type == pygame.QUIT:  # If user clicked close
                                done = True  # Flag that we are done so we exit this loop
                                dead = True
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_LEFT:
                                        x_speed = -1
                                elif event.key == pygame.K_RIGHT:
                                        x_speed = 1
                                elif event.key == pygame.K_UP:
                                    temp= tetris_piece.rotation()
                                    if not temp.collision_R(x_coord, y_coord_for_showing,bottom_blocks) and not temp.collision_L(x_coord, y_coord_for_showing,bottom_blocks):
                                        tetris_piece=tetris_piece.rotation()
                                elif event.key == pygame.K_SPACE:
                                    for i in range(y_coord_for_showing, dimension[0]):
                                        if tetris_piece.collision_bottom_stack(x_coord, i, bottom_blocks):
                                            y_coord= i
                                            break
                                        else:
                                            y_coord=dimension[0]
                                elif event.key == pygame.K_DOWN:
                                    y_speed+=1

                            elif event.type == pygame.KEYUP:
                                if event.key == pygame.K_LEFT:
                                    x_speed = 0
                                elif event.key == pygame.K_RIGHT:
                                    x_speed = 0
                                elif event.key == pygame.K_DOWN:
                                    y_speed-=1

                        x_coord = x_coord + x_speed
                        while tetris_piece.collision_R(x_coord, y_coord_for_showing, bottom_blocks) and  x_speed==1:
                            x_coord = x_coord-1
                        while tetris_piece.collision_L(x_coord, y_coord_for_showing, bottom_blocks) and x_speed==-1:
                            x_coord = x_coord+1
                        y_coord = y_coord + y_speed
                        y_coord_for_showing=int(y_coord//1)

                        if tetris_piece.collision_bottom_stack(x_coord, y_coord_for_showing, bottom_blocks):

                            if y_coord_for_showing!=0:

                                tetris_piece = tetris_piece.position(x_coord, y_coord_for_showing-1)
                                bottom_blocks.insert(tetris_piece)
                                tetris_lookahead, tetris_piece, tetris_future = setup_drops(tetris_lookahead)
                                x_coord, y_coord, y_coord_for_showing = set_to_the_beginning()

                            else:
                                dead=True

                        draw_background(screen)
                        tetris_piece= tetris_piece.position(x_coord,y_coord_for_showing)
                        tetris_piece.draw(screen, BLUE)
                        bottom_blocks.draw(screen, GREEN)
                        bottom_blocks, count, y_speed=check_and_delete_bottom_blocks_and_increase_count_and_y_speed(bottom_blocks, count, y_speed)
                        bottom_blocks.draw(screen, GREEN)
                        tetris_future.future_draw(screen, BLUE, [dimension[1]+3, 13])
                        print_scoreboard(screen, count)

                        pygame.display.flip()
                        clock.tick(20)
    pygame.quit()

if __name__ == "__main__":
    main()
