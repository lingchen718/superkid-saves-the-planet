import pygame
import random
from pygame.sprite import Sprite

class FallingItem(Sprite):
    """Represents an item falling from the top of the screen."""

    def __init__(self, game, item_type):
        super().__init__()

        self.screen = game.screen
        self.settings = game.settings  # Ensure settings has falling_speed defined
        self.item_type = item_type

        # Randomly select an image based on item type
        if self.item_type == "good":
            self.image = random.choice(
                game.assets.images["good_items"]
            ).copy()
        else:
            self.image = random.choice(
                game.assets.images["bad_items"]
            ).copy()


        self.image = pygame.transform.scale(
            self.image,
            (self.settings.item_width,
             self.settings.item_height)
        )
        self.rect = self.image.get_rect()

        # Set random X position within the screen width
        self.rect.x = random.randint(0, self.screen.get_width() - self.rect.width)

        # Start falling from above the screen
        self.rect.y = -self.rect.height

        self.y = float(self.rect.y)

    def update(self):
        """Move the item downwards."""
        self.y += self.settings.falling_speed + 2  # Ensure falling_speed is defined in settings
        self.rect.y = self.y

    def draw(self):
        """Draw the item on the screen."""
        self.screen.blit(self.image, self.rect)

    def off_screen(self):
        """Check if the item has fallen off the screen."""
        return self.rect.top > self.screen.get_rect().bottom
