import random
import pygame

class Card:
    def __init__(self, name, power, rarity, image_path,couse,number,show_path):
        """Initialize card with name, power, rarity, and an image."""
        self.name = name
        self.power = power  # Power as integer
        self.rarity = rarity
        self.image = pygame.image.load(image_path)  # Load card image
        self.couse = couse
        self.number = number
        self.show=pygame.image.load(show_path)


class GachaSystem:
    def __init__(self):
        # Define some cards with different rarities, powers, and images
        self.cards = [
            Card("Kazuma", 3, "Common", "collection/Kazuma.png",1,1,"showcaracter/Kazuma.png"),
            Card("Shubaru yamato", 5, "Rare", "collection/Shubaru yamato.png",2,2,"showcaracter/Shubaru yamato.png"),
            Card("Rin shirozaki", 5, "Rare", "collection/Rin shirozaki.png",2,3,"showcaracter/Rin shirozaki.png"),
            Card("Shizuo Valkyria", 8, "Epic", "collection/Shizuo Valkyria.png",4,4,"showcaracter/Shizuo Valkyria.png"),
            Card("Marry Eternalblood", 8, "Epic", "collection/Marry Eternalblood.png",4,5,"showcaracter/Marry eternalblood.png"),
            Card("Traisy o' Reapper", 5, "Rare", "collection/Traisy o' Reapper.png",2,6,"showcaracter/Traisy o' Reapper.png"),
            Card("Kaguya Hime", 10, "Legendary", "collection/Kaguya Hime.png",5,7,"showcaracter/Kaguya Hime.png"),
            Card("Gaia Theyggdrasill", 10, "Legendary", "collection/Gaia Theyggdrasill.png",5,8,"showcaracter/Gaia Theyggdrasill.png"),
            Card("Himego Kanade", 10, "Legendary", "collection/Himego Kanade.png",5,9,"showcaracter/Himego Kanade.png"),
            Card("Hibaki yamanashi", 10, "Legendary", "collection/Hibaki yamanashi.png",5,10,"showcaracter/Hibaki yamanashi.png"),
            Card("Jibrili", 10, "Legendary", "collection/Jibril.png",5,11,"showcaracter/Jibril.png"),
            Card("Isuna", 8, "Epic", "card/Isuna.png",4,12,"showcaracter/Isuna.png"),
            Card("Hikari", 10, "Legendary", "card/Hikari.png",5,13,"showcaracter/Hikari.png"),
            Card("Hibani", 3, "Common", "collection/Hibani.png",1,14,"showcaracter/Hibani.png"),
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

