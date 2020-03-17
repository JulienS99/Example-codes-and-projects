import pygame
import os


class player(object):
    run = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(8, 16)]
    jump = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(1, 8)]
    slide = [pygame.image.load(os.path.join('images', 'S1.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(
        os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S3.png')), pygame.image.load(os.path.join('images', 'S4.png')), pygame.image.load(os.path.join('images', 'S5.png'))]
    jumpList = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4]
    fall = pygame.image.load(os.path.join("images", "0.png"))

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.sliding = False
        self.slideCount = 0
        self.jumpCount = 0
        self.runCount = 0
        self.slideUp = False
        self.falling = False

    def draw(self, win):
        if self.jumping:
            self.y -= self.jumpList[self.jumpCount] * 1.3
            win.blit(self.jump[self.jumpCount//18], (self.x, self.y))
            self.jumpCount += 1
            if self.jumpCount > 108:
                self.jumpCount = 0
                self.jumping = False
                self.runCount = 0
            self.hitbox = (self.x + 4, self.y, self.width-28, self.height-14)  # NEW
        elif self.sliding or self.slideUp:
            if self.slideCount < 20:
                self.y += 1
                self.hitbox = (self.x + 4, self.y, self.width-24, self.height-10)  # NEW
            elif self.slideCount == 80:
                self.y -= 19
                self.sliding = False
                self.slideUp = True
            # NEW ELIF STATEMENT
            elif self.slideCount > 20 and self.slideCount < 80:  # NEW
                self.hitbox = (self.x, self.y+3, self.width-8, self.height-35)  # NEW

            if self.slideCount >= 110:
                self.slideCount = 0
                self.runCount = 0
                self.slideUp = False
                self.hitbox = (self.x + 4, self.y, self.width-24, self.height-10)  # NEW
            win.blit(self.slide[self.slideCount//10], (self.x, self.y))
            self.slideCount += 1

        elif self.falling:
            win.blit(self.fall, (self.x, self.y + 30))

        else:
            if self.runCount > 42:
                self.runCount = 0
            win.blit(self.run[self.runCount//6], (self.x, self.y))
            self.runCount += 1
            self.hitbox = (self.x + 4, self.y, self.width-24, self.height-13)  # NEW
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)  # NEW - Draws hitbox


class saw(object):
    img = [pygame.image.load(os.path.join("images", "SAW0.png")), pygame.image.load(os.path.join(
        "images", "SAW1.png")), pygame.image.load(os.path.join("images", "SAW2.png")), pygame.image.load(os.path.join("images", "SAW3.png"))]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (x, y, width, height)
        self.count = 0

    def draw(self, win):
        self.hitbox = (self.x + 10, self.y + 10, self.width - 15, self.height - 10)
        if self.count >= 8:
            self.count = 0
        win.blit(pygame.transform.scale(self.img[self.count//2], (64, 64)), (self.x, self.y))
        self.count += 1
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1]:
                return True
            return False


class spike(saw):
    img = pygame.image.load(os.path.join("images", "spike.png"))

    def draw(self, win):
        self.hitbox = (self.x + 6, self.y, 28, 315)
        win.blit(self.img, (self.x, self.y))
    # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] < self.hitbox[3]:
                return True
            return False
