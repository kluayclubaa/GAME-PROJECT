import pygame
import sys

#Add number to collection storage
x = "number from gacha" #เป็นค่าintที่ได้จากการสุ่มจากgacha
storage_add = open("C:\Users\Punn\OneDrive\Documents\GitHub\GAME-PROJECT\collection_storage.txt","a")
storage_add.write(x)
storage_add.close
#read collection storage and set up storage
storage_dict = {}
storage_read = open("C:\Users\Punn\OneDrive\Documents\GitHub\GAME-PROJECT\collection_storage.txt","r")
list_collection = storage_read.readline().split(" ") #collection_storage จะเก็บลำดับของการ์ดที่เราได้มาใน1บรรทัดต่อไปเรื่อยๆโดยมีการเว้ณให้กัน1ช่อง
for i in range(1,16): #เพื่อให้โค้ดไม่errorจะต้องเปลี่ยนชื่อfile card ทั้งหมดเป็นตัวเลขลำดับของการ์ด และเลข16ที่เห็นก็เป็นเพียงการตั้งขึ้นมาเฉยๆสามารถปรับเปลี่ยนในภายหลังได้
    if str(i) in list_collection:
        card_no_get_rect = pygame.image.load(f"C:/Users/Punn/Downloads/{str(i)}.jpg")\
        storage_dict[f"card{i}"] = card_no_get_rect.get_rect()
# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 1920
screen_height = 900
card_width = 200
card_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('collection')

bg_image = pygame.image.load("C:/Users/Punn/Downloads/space_bg.jpg")
bg_image = pygame.transform.scale(bg_image, (screen_width, screen_height))

button_image = pygame.image.load('C:/Users/Punn/Downloads/click.png')  
button_image_hover = pygame.image.load('C:/Users/Punn/Downloads/click_hower.png')
button_rect = button_image.get_rect()
button_rect.topleft = (1700,830)

# Main loop
running = True
collection_stage = "P1"
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_pos = pygame.mouse.get_pos()
    if collection_stage == "P1":
        if button_rect.collidepoint(mouse_pos):
            screen.blit(button_image_hover, button_rect.topleft)  
            if pygame.mouse.get_pressed()[0]:  
                collection_stage = "P2"
        else:
            screen.blit(bg_image, (0, 0))
            screen.blit(button_image, button_rect.topleft)
            for j in range(1,16):
                if j <= 8:
                    pygame.draw.rect(screen, (255,255,255), (20+(j+1)*240, 20, card_width, card_height))
                else:
                    pygame.draw.rect(screen, (255,255,255), (20+(j+1)*240, 480, card_width, card_height))
            for i in list_collection:
                if int(i) <= 8: #upper
                    screen.blit(storage_dict[f"card{i}"], (20+(int(i)-1)*240, 20)) 
                else: #lower
                    screen.blit(storage_dict[f"card{i}"], (20+(int(i)-8)*240, 480))  #ทั้งหมดเป็นลำดับแบบไล่ซ้ายไปขวาแล้วค่อยลง
    if collection_stage == "P2":
        screen.blit(bg_image, (0, 0))
        #เดี๋ยวมาทำหน้า2ต่อ

    
        
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()