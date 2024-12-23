import random
import pygame

class battle_card:
    def __init__(self,name,power : int, path):
        self.name = name
        self.power = power
        self.path = path
        self.image = pygame.image.load(path)

class battle_storage:
    def __init__(self):
        self.storage = [
            battle_card("Gaia Theyggdrasill",500,"card\Gaia Theyggdrasill.png"),
            battle_card("Hibaki yamanashi",500,"card\Hibaki yamanashi.png"),
            battle_card("Hibani",100,"card\Hibani.png"),
            battle_card("Himego Kanade",500,"card\Himego Kanade.png"),
            battle_card("Jibril",500,"card\Jibril.png"),
            battle_card("Kaguya Hime",500,"card\Kaguya Hime.png"),
            battle_card("Kazuma",100,"card\Kazuma.png"),
            battle_card("Marry Eternalblood",300,"card\Marry Eternalblood.png"),
            battle_card("Rin shirozaki",200,"card\Rin shirozaki.png"),
            battle_card("Shizuo Valkyria",300,"card\Shizuo Valkyria.png"),
            battle_card("Shubaru yamato",200,"card\Shubaru yamato.png"),
            battle_card("THE HAM",900,"card\THE HAM.png"),
            battle_card("Traisy o' Reapper",200,"card\Traisy o' Reapper.png"),
            battle_card("Heal",8888,"card\Heal.png"),
            battle_card("DarkHole",9999,"card\DarkHole.png")
        ]

        self.deck_storage = []

class Player_stat:
    def __init__(self):
        self.hp = 3000
        self.deck = []
        self.field1 = []
        self.field2 = []
        self.field3 = []
        self.field4 = []
        self.tome = []
        self.continue_play = True

    def add_card(self,card):
        self.deck.append(card)
        self.update_deck_positions()

    def update_deck_positions(self):
        i = 0
        for card in self.deck:
            card.position = (450 + 150 * i, 730)  # อัปเดตตำแหน่ง x ตามสูตร และตำแหน่ง y คงที่
            card.rect.topleft = card.position
            i = i + 1
    
    def check_rect(self,num):
        if num == 0:
            P_rect_x, P_rect_y = (475,497)
        elif num == 1:    
            P_rect_x, P_rect_y = (762,497)
        elif num == 2:
            P_rect_x, P_rect_y = (1047,497)
        elif num == 3:
            P_rect_x, P_rect_y = (1337,497)
        return (P_rect_x,P_rect_y)

class Bot_stat:
    def __init__(self):
        self.bot_hp = 3000
        self.bot_field1 = []
        self.bot_field2 = []
        self.bot_field3 = []
        self.bot_field4 = [] 
        self.tome = []

    def check_got_click(self,x_pos,y_pos,the_field):
        bot_select_card = []
        bot_select_card = self.bot_field1 if 480 <= x_pos <= 570 and 285 <= y_pos <=405 and self.bot_field1 != [] else bot_select_card
        bot_select_card = self.bot_field2 if 767 <= x_pos <= 857 and 285 <= y_pos <=405 and self.bot_field2 != [] else bot_select_card
        bot_select_card = self.bot_field3 if 1052 <= x_pos <= 1142 and 285 <= y_pos <=405 and self.bot_field3 != [] else bot_select_card  
        bot_select_card = self.bot_field4 if 1342 <= x_pos <= 1432 and 285 <= y_pos <=405 and self.bot_field4 != [] else bot_select_card
        if bot_select_card == []:
            pass
        elif bot_select_card[0].power > the_field[0].power:
            bot_select_card = []
        return bot_select_card
    
    def check_got_click_frame(self,x_pos,y_pos,bot_select_card):
        B_rect_x, B_rect_y = None,None
        B_rect_x, B_rect_y = (475,280) if 480 <= x_pos <= 570 and 285 <= y_pos <=405 and self.bot_field1 != [] else (B_rect_x, B_rect_y)
        B_rect_x, B_rect_y = (762,280) if 767 <= x_pos <= 857 and 285 <= y_pos <=405 and self.bot_field2 != [] else (B_rect_x, B_rect_y)
        B_rect_x, B_rect_y = (1047,280) if 1052 <= x_pos <= 1142 and 285 <= y_pos <=405 and self.bot_field3 != [] else (B_rect_x, B_rect_y)
        B_rect_x, B_rect_y = (1337,280) if 1342 <= x_pos <= 1432 and 285 <= y_pos <=405 and self.bot_field4 != [] else (B_rect_x, B_rect_y)
        if bot_select_card == None:
            B_rect_x, B_rect_y = None,None
        return B_rect_x,B_rect_y
    
class Process_battle:
    def process_battle_P_B(self,player_field, bot_field, player_hp, bot_hp, player_tome, bot_tome):
                # กรณีที่ player มีการ์ด แต่ bot ไม่มีการ์ด
                if player_field != [] and bot_field == []:
                    bot_hp -= player_field[0].power

                # กรณีที่ bot มีการ์ด แต่ player ไม่มีการ์ด
                elif player_field == []:
                    pass
                # กรณีที่การ์ดของทั้งคู่มีพลังเท่ากัน
                elif player_field[0].power == bot_field[0].power:
                    player_tome.append(player_field[0])
                    bot_tome.append(bot_field[0])
                    player_field.clear()
                    bot_field.clear()

                # กรณีที่การ์ดของ player มีพลังมากกว่า bot
                elif player_field[0].power > bot_field[0].power:
                    bot_hp = bot_hp - player_field[0].power + bot_field[0].power
                    bot_tome.append(bot_field[0])
                    bot_field.clear()

                return player_hp, bot_hp
    
    def process_battle_B_P(self,player_field, bot_field, player_hp, bot_hp, player_tome, bot_tome):
                if bot_field == []:
                    pass
                elif player_field == []:
                    player_hp = player_hp - bot_field[0].power
                # กรณีที่การ์ดของทั้งคู่มีพลังเท่ากัน
                elif player_field[0].power == bot_field[0].power:
                    player_tome.append(player_field[0])
                    bot_tome.append(bot_field[0])
                    player_field.clear()
                    bot_field.clear()

                # กรณีที่การ์ดของ bot มีพลังมากกว่า player
                elif player_field[0].power < bot_field[0].power:
                    player_hp =  player_hp - bot_field[0].power + player_field[0].power
                    player_tome.append(player_field[0])
                    player_field.clear()

                return player_hp, bot_hp
class Picture:
    def __init__(self, position, image,power):
        self.image = image
        self.rect = self.image.get_rect(topleft=position)
        self.position = position
        self.target_position = [(480, 502),(767, 502),(1052, 502),(1342, 502)]  
        self.start_position = position  
        self.dragging = False  
        self.placed = False
        self.power = power

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def check_click(self, mouse_position):
        if self.rect.collidepoint(mouse_position):
            return True
    
    def start_drag(self):
        if not self.placed:
            self.dragging = True
    
    def stop_drag(self,player,location_click):
        player1 = player
        self.dragging = False
        i = 0
        for target_position in self.target_position:
            distance_to_target = pygame.math.Vector2(self.position[0] - target_position[0], self.position[1] - target_position[1]).length()
            if distance_to_target <= 100:
                self.position = target_position
                self.rect.topleft = self.position  # อัพเดตตำแหน่งจริงใน rect
                self.image = pygame.transform.smoothscale(self.image, (90,120))
                self.placed = True
                if i == 0:
                    player1.field1.append(player1.deck[location_click])
                elif i == 1:
                    player1.field2.append(player1.deck[location_click])
                elif i == 2:
                    player1.field3.append(player1.deck[location_click])
                elif i == 3:
                    player1.field4.append(player1.deck[location_click])
                player1.deck.remove(player1.deck[location_click])
                player1.update_deck_positions()
                player1.continue_play = not player1.continue_play
                break
            i += 1
        else:
               
            self.position = self.start_position
            self.rect.topleft = self.position

    def update(self, mouse_pos):
        if self.dragging:
            # หากลากภาพ, อัพเดตตำแหน่ง
            self.position = mouse_pos
            self.rect.topleft = self.position