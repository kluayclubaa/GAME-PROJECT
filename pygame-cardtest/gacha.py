import random
import pygame

class Card:
    def __init__(self, name, power, rarity, image_path,couse,number,show_path,card_path):
        """Initialize card with name, power, rarity, and an image."""
        self.name = name
        self.power = power  # Power as integer
        self.rarity = rarity
        self.image = pygame.image.load(image_path)  # Load card image
        self.couse = couse
        self.number = number
        self.show=pygame.image.load(show_path)
        self.card=pygame.image.load(card_path)


class GachaSystem:
    def __init__(self):
        # Define some cards with different rarities, powers, and images
        self.cards = [
            Card("Kazuma", 3, "Common", "collection/Kazuma.png",1,1,"showcaracter/Kazuma.png","card/Kazuma.png"),
            Card("Shubaru yamato", 5, "Rare", "collection/Shubaru yamato.png",2,2,"showcaracter/Shubaru yamato.png","card/Shubaru yamato.png"),
            Card("Rin shirozaki", 5, "Rare", "collection/Rin shirozaki.png",2,3,"showcaracter/Rin shirozaki.png","card/Rin shirozaki.png"),
            Card("Shizuo Valkyria", 8, "Epic", "collection/Shizuo Valkyria.png",4,4,"showcaracter/Shizuo Valkyria.png","card/Shizuo Valkyria.png"),
            Card("Marry Eternalblood", 8, "Epic", "collection/Marry Eternalblood.png",4,5,"showcaracter/Marry eternalblood.png","card/Marry Eternalblood.png"),
            Card("Traisy o' Reapper", 5, "Rare", "collection/Traisy o' Reapper.png",2,6,"showcaracter/Traisy o' Reapper.png","card/Traisy o' Reapper.png"),
            Card("Kaguya Hime", 10, "Legendary", "collection/Kaguya Hime.png",5,7,"showcaracter/Kaguya Hime.png","card/Kaguya Hime.png"),
            Card("Gaia Theyggdrasill", 10, "Legendary", "collection/Gaia Theyggdrasill.png",5,8,"showcaracter/Gaia Theyggdrasill.png","card/Gaia Theyggdrasill.png"),
            Card("Himego Kanade", 10, "Legendary", "collection/Himego Kanade.png",5,9,"showcaracter/Himego Kanade.png","card/Himego Kanade.png"),
            Card("Hibaki yamanashi", 10, "Legendary", "collection/Hibaki yamanashi.png",5,10,"showcaracter/Hibaki yamanashi.png","card/Hibaki yamanashi.png"),
            Card("Jibrili", 10, "Legendary", "collection/Jibril.png",5,11,"showcaracter/Jibril.png","card/Jibril.png"),
            Card("Isuna", 8, "Epic", "collection/Isuna.png",4,12,"showcaracter/Isuna.png","card/Isuna.png"),
            Card("Hikari", 10, "Legendary", "collection/Hikari.png",5,13,"showcaracter/Hikari.png","card/Hikari.png"),
            Card("Hibani", 3, "Common", "collection/Hibani.png",1,14,"showcaracter/Hibani.png","card/Hibani.png"),
            Card("THE HAM", 10, "Legendary", "collection/THE HAM.png",5,15,"showcaracter/THE HAM.jpg","card/THE HAM.png"),
            Card("Heal",888,"Legendary","collection/Heal.png",5,16,"showcaracter/Heal.png","card/Heal.png"),
            Card("DarkHole",999,"Legendary","collection/DarkHole.png",5,17,"showcaracter/DarkHole.png","card/DarkHole.png")
        ]
        self.pull_count = 0

    def pull(self):
        
        rarity_probabilities = {
            "Common": 60,
            "Rare": 25,
            "Epic": 10,
            "Legendary": 4,
            "Limited": 1

        }
        if self.pull_count == 9  :
            self.pull_count = 0
            
            return self.get_legendary_card()
        # Create a pool of cards based on rarity probabilities
        card_pool = [card for card in self.cards for _ in range(rarity_probabilities[card.rarity])]
        
        pull_card = random.choice(card_pool)

        if pull_card.rarity !="Legendary":
            self.pull_count += 1
        else:
            self.pull_count = 0
        
        return pull_card
        
    
    def get_legendary_card(self):   
        card_pool = [card for card in self.cards if card.rarity == "Legendary"]
        return random.choice(card_pool)
    def get_random_card(self):
        random_card = random.choice(self.cards)
        return random_card.show

