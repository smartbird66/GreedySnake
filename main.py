import pygame
import random
import time
from collections import deque

# 帧率  游戏窗口的宽、高
FPS = 5
SCREENWIDTH = 600
SCREENHEIGHT = 600
# 坐标缩放 每个苹果和像素点20*20
ZOOM = 20
DIRECTION = {"left": 1, "right": 2, "up": 3, "down": 4, "none":0}


class GSgame:
    def __init__(self):
        # 获取时钟对象
        self.CLOCKFPS = pygame.time.Clock()
        # 设置游戏屏幕
        self.SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        pygame.display.set_caption("Greedy Snack")

        self.score = 0
        # 贪吃蛇头部的位置
        self.head_x = SCREENWIDTH / 2 / ZOOM
        self.head_y = SCREENHEIGHT / 2 / ZOOM
        self.snackVal = 1
        # 方向1234 分别代表上线左右
        self.snackDirection = DIRECTION["right"]  # -贪吃蛇的方向
        # 身体
        self.body = deque()
        self.body.append([self.head_x, self.head_y])
        # 绘制一个蛇头
        self.SnackHeadImage = pygame.Surface((ZOOM, ZOOM))  # Create a rectangular Surface.
        self.SnackHeadImage.fill((255, 0, 0))  # Fill it with a color.
        self.SnackHeadRect = pygame.Rect(self.head_x*ZOOM,self.head_y*ZOOM, ZOOM, ZOOM)  # Create a rect for where to blit the ship.

        self.preApple = self.RandomApple()
        pygame.event.set_blocked(None)
        pygame.event.set_allowed((pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN, pygame.QUIT))  # 允许鼠标按下和键盘按下事件进入队列

    # 开始游戏
    def start(self):
        while True:
            # time.sleep(1)
            # 键盘鼠标控制
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    pygame.quit()
                    quit()
                elif (event.type == pygame.KEYDOWN):
                    if event.key == pygame.K_w and self.snackDirection != DIRECTION["down"]:
                        self.snackDirection = DIRECTION["up"]
                    if event.key == pygame.K_a and self.snackDirection != DIRECTION["right"]:
                        self.snackDirection = DIRECTION["left"]
                    if event.key == pygame.K_s and self.snackDirection != DIRECTION["up"]:
                        self.snackDirection = DIRECTION["down"]
                    if event.key == pygame.K_d and self.snackDirection != DIRECTION["left"]:
                        self.snackDirection = DIRECTION["right"]
            #   蛇头朝着DIRECTION自动移动
            self.body.rotate(1)
            if self.snackDirection == DIRECTION["left"]:
                self.head_x -= self.snackVal
                self.head_x %= (SCREENWIDTH / ZOOM)
                # self.SnackHeadRect.move_ip(-1*self.snackVal*ZOOM, 0)
            elif self.snackDirection == DIRECTION["right"]:
                self.head_x += self.snackVal
                self.head_x %= (SCREENWIDTH / ZOOM)
                # self.SnackHeadRect.move_ip(1*self.snackVal*ZOOM, 0)
            elif self.snackDirection == DIRECTION["up"]:
                self.head_y -= self.snackVal
                self.head_y %= (SCREENHEIGHT / ZOOM)
                # self.SnackHeadRect.move_ip(0, -1 * self.snackVal * ZOOM)
            elif self.snackDirection == DIRECTION["down"]:
                self.head_y += self.snackVal
                self.head_y %= (SCREENHEIGHT / ZOOM)
                # self.SnackHeadRect.move_ip(0, 1 * self.snackVal * ZOOM)
            self.body[0][0] = self.head_x
            self.body[0][1] = self.head_y
            # 碰撞检测
            if self.isCrash():
                font = pygame.font.SysFont("freesansbold.ttf", 30)
                text = font.render("Game Over!", True, (8,241,8))
                self.SCREEN.blit(text, (200, 200))
                pygame.display.update()
                time.sleep(5)
                self.__init__()
            #self.snackDirection = DIRECTION["none"]
            self.eatApple() # -检测吃苹果
            # print(event)
            # 画一个方块
            self.SCREEN.fill((0,0,0)) # -画布
            self.drawSnack() # 画蛇
            # 画苹果
            pygame.draw.rect(self.SCREEN, (8,241,8), (self.preApple[0]*ZOOM, self.preApple[1]*ZOOM, ZOOM, ZOOM))
            # self.SCREEN.blit(self.SnackHeadImage, self.SnackHeadRect)



            pygame.display.update()
            self.CLOCKFPS.tick(FPS)

    # 随机生成新的合法苹果
    def RandomApple(self):
        position_x = random.randint(0, SCREENWIDTH / ZOOM - 1)
        position_y = random.randint(0, SCREENHEIGHT / ZOOM - 1)

        # 如果随机的苹果与蛇头或者蛇身重合，考虑重新生成策略
        while not self.AppleLegal(position_x, position_y):
            position_x = random.randint(0, SCREENWIDTH / ZOOM -1)
            position_y = random.randint(0, SCREENHEIGHT / ZOOM -1)
            print("illagle")
        return [position_x, position_y]

    # 判断生成的苹果是否合法
    def AppleLegal(self, x, y):
        Legal = True
        for it in self.body:
            if (it[0] == x and it[1] == y):
                Legal = False
                break
        return Legal
    # 判断是否可以吃掉苹果，吃掉之后重新生成，然后加长身体
    def eatApple(self):
        if self.preApple[0] == self.head_x and self.preApple[1] == self.head_y:
            self.body.insert(0, [self.head_x, self.head_y])
            self.preApple = self.RandomApple()

    # 画出整个贪吃蛇
    def drawSnack(self):
        for it in self.body:
            pygame.draw.rect(self.SCREEN, (255, 0, 0), (it[0] * ZOOM, it[1] * ZOOM, ZOOM, ZOOM))

    # 碰撞检测
    def isCrash(self):
        crash = False
        for i in range(self.body.__len__()):
            if i>1 and self.head_x==self.body[i][0] and self.head_y == self.body[i][1]:
                crash = True
                break
        return crash

if __name__ == "__main__":
    pygame.init()
    game = GSgame()
    print("游戏初始化完成")
    game.start()
    pygame.quit()
