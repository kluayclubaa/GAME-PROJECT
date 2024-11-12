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
            battle_card("Gaia Theyggdrasill",500,"collection\Gaia Theyggdrasill.png"),
            battle_card("Hibaki yamanashi",500,"collection\Hibaki yamanashi.png"),
            battle_card("Hibani",100,"collection\Hibani.png"),
            battle_card("Himego Kanade",500,"collection\Himego Kanade.png"),
            battle_card("Jibril",500,"collection\Jibril.png"),
            battle_card("Kaguya Hime",500,"collection\Kaguya Hime.png"),
            battle_card("Kazuma",100,"collection\Kazuma.png"),
            battle_card("Marry Eternalblood",300,"collection\Marry Eternalblood.png"),
            battle_card("Rin shirozaki",200,"collection\Rin shirozaki.png"),
            battle_card("Shizuo Valkyria",300,"collection\Shizuo Valkyria.png"),
            battle_card("Shubaru yamato",200,"collection\Shubaru yamato.png"),
            battle_card("THE HAM",900,"collection\THE HAM.png"),
            battle_card("Traisy o' Reapper",200,"collection\Traisy o' Reapper.png"),
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
class Bot_stat:
    def __init__(self):
        self.bot_hp = 3000
        self.bot_field1 = []
        self.bot_field2 = []
        self.bot_field3 = []
        self.bot_field4 = [] 
        self.tome = []

    def check_got_click(self,x_pos,y_pos):
        bot_select_card = None
        bot_select_card = self.bot_field1 if 480 <= x_pos <= 570 and 285 <= y_pos <=405 and self.bot_field1 != [] else bot_select_card
        bot_select_card = self.bot_field2 if 767 <= x_pos <= 857 and 285 <= y_pos <=405 and self.bot_field2 != [] else bot_select_card
        bot_select_card = self.bot_field3 if 1052 <= x_pos <= 1142 and 285 <= y_pos <=405 and self.bot_field3 != [] else bot_select_card  
        bot_select_card = self.bot_field4 if 1342 <= x_pos <= 1432 and 285 <= y_pos <=405 and self.bot_field4 != [] else bot_select_card
        return bot_select_card
    
    def check_got_click_frame(self,x_pos,y_pos):
        B_rect_x, B_rect_y = None,None
        B_rect_x, B_rect_y = (475,280) if 480 <= x_pos <= 570 and 285 <= y_pos <=405 and self.bot_field1 != [] else (B_rect_x, B_rect_y)
        B_rect_x, B_rect_y = (762,280) if 767 <= x_pos <= 857 and 285 <= y_pos <=405 and self.bot_field2 != [] else (B_rect_x, B_rect_y)
        B_rect_x, B_rect_y = (1047,280) if 1052 <= x_pos <= 1142 and 285 <= y_pos <=405 and self.bot_field3 != [] else (B_rect_x, B_rect_y)
        B_rect_x, B_rect_y = (1337,280) if 1342 <= x_pos <= 1432 and 285 <= y_pos <=405 and self.bot_field4 != [] else (B_rect_x, B_rect_y)

        return B_rect_x,B_rect_y
    
class Process_battle:
    def process_battle(self,player_field, bot_field, player_hp, bot_hp, player_tome, bot_tome):
                # กรณีที่ player มีการ์ด แต่ bot ไม่มีการ์ด
                if player_field != [] and bot_field == []:
                    bot_hp -= player_field[0].power

                # กรณีที่ bot มีการ์ด แต่ player ไม่มีการ์ด
                elif player_field == [] and bot_field != []:
                    player_hp -= bot_field[0].power
                # กรณีว่างคู่
                elif player_field == [] and bot_field == []:
                    pass
                # กรณีที่การ์ดของทั้งคู่มีพลังเท่ากัน
                elif player_field[0].power == bot_field[0].power:
                    player_tome.append(player_field[0])
                    bot_tome.append(bot_field[0])
                    player_field.clear()
                    bot_field.clear()

                # กรณีที่การ์ดของ player มีพลังมากกว่า bot
                elif player_field[0].power > bot_field[0].power:
                    bot_hp -= player_field[0].power - bot_field[0].power
                    bot_tome.append(bot_field[0])
                    bot_field.clear()

                # กรณีที่การ์ดของ bot มีพลังมากกว่า player
                elif player_field[0].power < bot_field[0].power:
                    player_hp -= bot_field[0].power - player_field[0].power
                    player_tome.append(player_field[0])
                    player_field.clear()

                return player_hp, bot_hp

        