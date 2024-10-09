import random
import pygame

class Card:
    def __init__(self, name, power, rarity, image_path):
        """Initialize card with name, power, rarity, and an image."""
        self.name = name
        self.power = power  # Power as integer
        self.rarity = rarity
        self.image = pygame.image.load(image_path)  # Load card image

class GachaSystem:
    def __init__(self):
        # Define some cards with different rarities, powers, and images
        self.cards = [
            Card("Kazuma", 3, "Common", "card/Kazuma.jpg"),
            Card("Shubaru yamato", 6, "Rare", "card/Shubaru yamato.jpg"),
            Card("Rin shirozaki", 6, "Rare", "card/Rin shirozaki.jpg"),
            Card("Shizuo Valkyria", 9, "Epic", "card/Shizuo Valkyria.jpg"),
            Card("Marry Eternalblood", 8, "Epic", "card/Marry Eternalblood.jpg"),
            Card("Traisy o' Reapper", 9, "Rare", "card/Traisy o' Reapper.jpg"),
            Card("Kaguya Hime", 10, "Legendary", "card/Kaguya Hime.jpg"),
            Card("Gaia Theyggdrasill", 10, "Legendary", "card/Gaia Theyggdrasill.jpg"),
            Card("Himego Kanade", 10, "Legendary", "card/Himego Kanade.jpg"),
            Card("Hibaki yamanashi", 15, "Limited", "card/Hibaki yamanashi.jpg"),
        ]

    def pull(self):
        """Simulate a gacha pull."""
        rarity_probabilities = {
            "Common": 60,
            "Rare": 25,
            "Epic": 10,
            "Legendary": 4,
            "Limited": 1
        }
        # Create a pool of cards based on rarity probabilities
        card_pool = [card for card in self.cards for _ in range(rarity_probabilities[card.rarity])]
        # Randomly choose a card from the pool
        return random.choice(card_pool)

