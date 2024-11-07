import pygame
import sys

# กำหนดขนาดหน้าจอ
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 900

# สีพื้นหลัง
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# โหลดภาพ
mycard = pygame.image.load("C:/Users/Punn/OneDrive/Documents/GitHub/GAME-PROJECT/pygame-cardtest/card/Himego Kanade.jpg")
new_width, new_height = 120, 160
mycard = pygame.transform.smoothscale(mycard, (new_width, new_height))

# สร้างคลาส Picture
class Picture:
    def __init__(self, position, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=position)
        self.position = position
        self.target_position = [(480, 502),(767, 502),(1052, 502),(1342, 502)]  
        self.start_position = position  
        self.dragging = False  
        self.placed = False

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def check_click(self, mouse_position):
        if self.rect.collidepoint(mouse_position):
            return True
    
    def start_drag(self):
        if not self.placed:
            self.dragging = True
    
    def stop_drag(self):
        self.dragging = False
        
        for target_position in self.target_position:
            distance_to_target = pygame.math.Vector2(self.position[0] - target_position[0], self.position[1] - target_position[1]).length()
            if distance_to_target <= 100:
                self.position = target_position
                self.rect.topleft = self.position  # อัพเดตตำแหน่งจริงใน rect
                self.image = pygame.transform.smoothscale(self.image, (90,120))
                self.placed = True
                break
        else:
               
            self.position = self.start_position
            self.rect.topleft = self.position
            self.image = pygame.transform.smoothscale(self.image, (120,160))
    def update(self, mouse_pos):
        if self.dragging:
            # หากลากภาพ, อัพเดตตำแหน่ง
            self.position = mouse_pos
            self.rect.topleft = self.position

# ฟังก์ชันหลัก

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Click and Drag Image")

image1 = Picture((450,730), mycard)

while True:
    battle_map = pygame.image.load("C:/Users/Punn/Downloads/battle_map.jpg")
    battle_map = pygame.transform.scale(battle_map, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(battle_map, (0, 0))

       
    image1.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

            # ตรวจจับการคลิกเมาส์
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if image1.check_click(mouse_pos):
                image1.start_drag()  # เริ่มลากภาพ

        elif event.type == pygame.MOUSEBUTTONUP:
            image1.stop_drag()  # เมื่อปล่อยเมาส์ให้หยุดลาก

        # อัพเดตตำแหน่งของภาพ
    mouse_pos = pygame.mouse.get_pos()
    image1.update(mouse_pos)

    pygame.display.flip()

# รันโปรแกรมหลัก
