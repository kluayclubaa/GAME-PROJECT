import pygame
import os
import sys
class DeckManager:
    def __init__(self):
        self.selected_card = None  # Stores currently selected card
        self.card_offset = (0, 0)  # Offset for dragging
        self.fixed_slots = []  # Stores fixed position slots
        self.placed_cards = {}  # Stores cards placed in each fixed slot
        self.deck_main = {}  # Stores initial deck from file
        self.initialize_fixed_slots()

    def initialize_fixed_slots(self):
        """Initialize the fixed position slots (10 slots)."""
        fixed_slot_start_x = 320  # Starting x position for the fixed slots
        fixed_slot_start_y = 50  # Starting y position for the fixed slots
        fixed_slot_start_y2 = 220
        fixed_slot_width = 120
        fixed_slot_height = 160
        fixed_slot_spacing = 10
        fixed_slots_count = 10  # Total 10 slots

        # Generate 10 fixed slots in the first row
        for i in range(fixed_slots_count):
            slot_x = fixed_slot_start_x + i * (fixed_slot_width + fixed_slot_spacing)
            slot_y = fixed_slot_start_y
            self.fixed_slots.append(pygame.Rect(slot_x, slot_y, fixed_slot_width, fixed_slot_height))
        # Generate 10 fixed slots in the second row
        for i in range(fixed_slots_count):
            slot_x = fixed_slot_start_x + i * (fixed_slot_width + fixed_slot_spacing)
            slot_y = fixed_slot_start_y2
            self.fixed_slots.append(pygame.Rect(slot_x, slot_y, fixed_slot_width, fixed_slot_height))

    def update_deck_file(self):
        """Update deck.txt file to reflect the current deck_cards state."""
        with open("deck_replace.txt", "w") as file:
            for card_name, count in self.deck_main.items():
                for _ in range(count):
                    file.write(card_name + "\n")
        print("Deck file updated.")

    def save_fixed_slots_to_file(self):
        """
        Save the names of cards currently placed in fixed slots to deck_save.txt.
        This is triggered by the save button.
        """
        print("Saving cards to deck_save.txt...")  # Debugging
        with open("deck_save.txt", "a", encoding="utf-8") as file:
            for card_name in self.fixed_slots:
                file.write(f"{card_name}\n" )
        print("Save completed!")
        """Save the names of cards currently placed in fixed slots to deck_save.txt."""
        with open("deck_save.txt", "w") as file:
            for slot_index in sorted(self.placed_cards.keys()):
                card_name = self.placed_cards[slot_index]
                file.write(card_name + "\n")
        print("Fixed slot cards saved to deck_save.txt")

    def draw_deck_page(self, screen, gacha, deck_cards):
        """Draw the deck page with cards arranged in the lower grid and handle card selection, dragging, and snapping."""
        card_width = 100
        card_height = 130
        deck_start_x = 300
        deck_start_y = 400  # Starting y position for the deck cards
        card_spacing = 10
        slots_per_row = 12

        # Draw deck slots in a 3-row grid (lower section)
        for row in range(3):
            for i in range(slots_per_row):
                slot_x = deck_start_x + i * (card_width + card_spacing)
                slot_y = deck_start_y + row * (card_height + card_spacing)
                slot_rect = pygame.Rect(slot_x, slot_y, card_width, card_height)
                pygame.draw.rect(screen, (255, 255, 255), slot_rect)
                pygame.draw.rect(screen, (200, 200, 200), slot_rect, 2)

        # Draw fixed slots in the upper section
        for slot_rect in self.fixed_slots:
            pygame.draw.rect(screen, (255, 255, 255), slot_rect)
            pygame.draw.rect(screen, (200, 200, 200), slot_rect, 2)

        # Display cards in fixed slots if placed
        for slot_index, card_name in self.placed_cards.items():
            for card in gacha.cards:
                if card.name == card_name:
                    slot_rect = self.fixed_slots[slot_index]
                    card_image = pygame.transform.smoothscale(card.card, (120, 160))
                    screen.blit(card_image, (slot_rect.x, slot_rect.y))
                    break

        # Display deck cards in the lower section and handle dragging
        card_hit_boxes = []  # List of tuples (rect, card_name)
        card_position = 0

        for card_name in list(deck_cards.keys()):  # Iterate over a copy to modify deck_cards in-place
            row = card_position // slots_per_row
            col = card_position % slots_per_row

            if row < 3:
                for card in gacha.cards:
                    if card.name == card_name:
                        # Calculate initial position
                        card_x = deck_start_x + col * (card_width + card_spacing)
                        card_y = deck_start_y + row * (card_height + card_spacing)

                        # Highlight selected card for dragging
                        if self.selected_card == card_name:
                            mouse_x, mouse_y = pygame.mouse.get_pos()
                            card_x, card_y = mouse_x - self.card_offset[0], mouse_y - self.card_offset[1]

                        # Draw card
                        card_rect = pygame.Rect(card_x, card_y, card_width, card_height)
                        card_hit_boxes.append((card_rect, card_name))
                        
                        card_image = pygame.transform.smoothscale(card.card, (card_width, card_height))
                        screen.blit(card_image, (card_x, card_y))

                        # Draw card count if > 1
                        count = deck_cards[card_name]
                        if count > 1:
                            count_font = pygame.font.Font(None, 24)
                            count_text = count_font.render(f"x{count}", True, (255, 255, 255))
                            count_rect = count_text.get_rect(bottomright=(card_x + card_width - 5, 
                                                                          card_y + card_height - 5))
                            shadow_text = count_font.render(f"x{count}", True, (0, 0, 0))
                            screen.blit(shadow_text, (count_rect.x + 1, count_rect.y + 1))
                            screen.blit(count_text, count_rect)

                        card_position += 1
                        break

        # Handle card selection, dragging, and snapping to fixed slots
        if pygame.mouse.get_pressed()[0]:  # Left click for selecting or dragging
            mouse_pos = pygame.mouse.get_pos()
            if not self.selected_card:
                # Start dragging if a card is clicked in the deck or fixed slots
                for card_rect, card_name in card_hit_boxes:
                    if card_rect.collidepoint(mouse_pos):
                        self.selected_card = card_name
                        self.card_offset = (mouse_pos[0] - card_rect.x, mouse_pos[1] - card_rect.y)
                        break
                # Check if a card in fixed slots is clicked
                for slot_index, card_name in self.placed_cards.items():
                    slot_rect = self.fixed_slots[slot_index]
                    if slot_rect.collidepoint(mouse_pos):
                        self.selected_card = card_name
                        self.card_offset = (mouse_pos[0] - slot_rect.x, mouse_pos[1] - slot_rect.y)
                        # Remove the card from placed slots and add it back to deck
                        deck_cards[self.selected_card] = deck_cards.get(self.selected_card, 0) + 1
                        del self.placed_cards[slot_index]
                        self.update_deck_file()  # Update file after adding card back to deck
                        break
        else:
            # On mouse release, snap to the nearest fixed slot if applicable
            if self.selected_card:
                mouse_pos = pygame.mouse.get_pos()
                for slot_index, slot_rect in enumerate(self.fixed_slots):
                    if slot_rect.collidepoint(mouse_pos) and slot_index not in self.placed_cards:
                        # Place card in slot and update deck count
                        self.placed_cards[slot_index] = self.selected_card
                        deck_cards[self.selected_card] -= 1
                        
                        if deck_cards[self.selected_card] <= 0:
                            del deck_cards[self.selected_card]

                        self.update_deck_file()  # Update file after placing card in fixed slot
                        break

                self.selected_card = None  # Deselect card after placing

        return card_hit_boxes

    def load_deck(self):
        """Load deck from file and count unique cards."""
        self.deck_main = {}
        try:
            with open("deck_replace.txt", "r") as file:
                for line in file:
                    card_name = line.strip()
                    if card_name in self.deck_main:
                        self.deck_main[card_name] += 1
                    else:
                        self.deck_main[card_name] = 1
        except FileNotFoundError:
            print("Deck file not found")
        return self.deck_main



