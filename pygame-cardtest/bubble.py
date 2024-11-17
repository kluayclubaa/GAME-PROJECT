# bubble.py
import pygame
import random

# กำหนดค่าเริ่มต้นของหน้าจอ (ควรตรงกับในไฟล์หลัก)
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 900
MIN_BUBBLE_RADIUS = 3
MAX_BUBBLE_RADIUS = 20
BUBBLE_COLOR_RANGE = (0, 50)

class Bubble:
    def __init__(self):
        # สุ่มตำแหน่งของฟองสบู่
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = SCREEN_HEIGHT + random.randint(0, SCREEN_HEIGHT)
        
        # สุ่มขนาดของฟองสบู่
        self.radius = random.randint(MIN_BUBBLE_RADIUS, MAX_BUBBLE_RADIUS)
        
        # สุ่มสีของฟองสบู่
        color_value = random.randint(BUBBLE_COLOR_RANGE[0], BUBBLE_COLOR_RANGE[1])
        self.color = (color_value, color_value, 255)
        
        # ความเร็วในการเคลื่อนที่ขึ้น
        self.speed = random.uniform(1, 5)

    def update(self):
        # อัปเดตตำแหน่ง y ของฟองสบู่ (เลื่อนขึ้น)
        self.y -= self.speed
        
        # ถ้าฟองสบู่ออกจากหน้าจอ ให้รีเซ็ตตำแหน่งใหม่ที่ด้านล่าง
        if self.y < -self.radius:
            self.y = SCREEN_HEIGHT + self.radius
            self.x = random.randint(0, SCREEN_WIDTH)
            self.speed = random.uniform(1, 5)

    def draw(self, screen):
        # วาดฟองสบู่ลงบนหน้าจอ
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
