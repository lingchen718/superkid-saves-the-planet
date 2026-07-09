# SuperKid.py
import pygame
import math
import os


class SuperKid:
    """Super Kid (Steve) - animated, expressive, and fun for kids."""

    # --- Flash effect types ---
    FLASH_NONE = 0
    FLASH_GOOD = 1   # green catch
    FLASH_BAD = 2    # red hit

    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.screen_rect = game.screen.get_rect()

        # --- Load base image ---
        self.base_image = game.assets.images["player"].copy()

        # Store original for flipping / tinting
        self.original_image = self.base_image.copy()
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()

        # --- Position ---
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.base_y = float(self.rect.y)     # resting Y (used for bob)

        # --- Movement flags ---
        self.moving_right = False
        self.moving_left = False
        self.facing_right = True             # which way Steve faces

        # --- Bob / sway animation ---
        self.bob_timer = 0.0                 # accumulates each frame
        self.bob_speed = 0.18                # how fast the bob cycles
        self.bob_amount = 5                  # pixels up-down while running
        self.sway_speed = 0.06              # slower idle sway
        self.sway_amount = 2                 # smaller sway when idle

        # --- Squash & stretch ---
        self.squash = 1.0                    # scale Y: < 1 = squash, > 1 = stretch
        self.squash_timer = 0

        # --- Flash effect ---
        self.flash_type = self.FLASH_NONE
        self.flash_timer = 0
        self.flash_duration = 18             # frames the flash lasts

        # --- Shadow ---
        self.shadow_color = (0, 0, 0, 60)   # translucent black

        # --- Name tag (set False to hide) ---
        self.SHOW_NAMETAG = False
        font_path = os.path.join("fonts", "ComicNeue-Bold.ttf")
        self.nametag_font = pygame.font.Font(font_path, 28)
        self._build_nametag()

        # --- Pre-build flipped image cache ---
        self._img_right = self.original_image.copy()
        self._img_left = pygame.transform.flip(self.original_image, True, False)

    # --------------------------------------------------------
    #  PUBLIC: called by main game
    # --------------------------------------------------------

    def update(self):
        """Update Steve's position and all animations."""
        is_moving = self.moving_right or self.moving_left

        # -- Horizontal movement --
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.kid_speed
            self.facing_right = True

        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.kid_speed
            self.facing_right = False

        self.rect.x = int(self.x)

        # -- Bob / sway timer --
        self.bob_timer += 1

        if is_moving:
            # Running bob: bouncy up-down
            offset_y = math.sin(self.bob_timer * self.bob_speed) * self.bob_amount
        else:
            # Idle sway: gentle float
            offset_y = math.sin(self.bob_timer * self.sway_speed) * self.sway_amount

        self.rect.y = int(self.base_y + offset_y)

        # -- Flash timer countdown --
        if self.flash_timer > 0:
            self.flash_timer -= 1
        else:
            self.flash_type = self.FLASH_NONE

        # -- Squash timer countdown --
        if self.squash_timer > 0:
            self.squash_timer -= 1
            # Ease squash back to 1.0
            self.squash = 1.0 - 0.25 * (self.squash_timer / 10)
        else:
            self.squash = 1.0

        # -- Rebuild image with current effects --
        self._build_image()

    def blitme(self):
        self._draw_shadow()

        # Fallback if update() hasn't run yet
        if not hasattr(self, "draw_rect"):
            self.draw_rect = self.image.get_rect()
            self.draw_rect.midbottom = self.rect.midbottom

        self.screen.blit(self.image, self.draw_rect)

        if self.SHOW_NAMETAG:
            self._draw_nametag()

    def center_kid(self):
        """Reset Steve to the bottom-centre of the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.base_y = float(self.rect.y)
        self.bob_timer = 0

    # --------------------------------------------------------
    #  TRIGGERS (call these from your collision / event code)
    # --------------------------------------------------------

    def trigger_catch(self):
        """Call this when Steve catches a GOOD item."""
        self.flash_type = self.FLASH_GOOD
        self.flash_timer = self.flash_duration
        self.squash = 0.75            # squash on catch
        self.squash_timer = 10

    def trigger_hit(self):
        """Call this when Steve is hit by a BAD item."""
        self.flash_type = self.FLASH_BAD
        self.flash_timer = self.flash_duration

    # --------------------------------------------------------
    #  INTERNAL HELPERS
    # --------------------------------------------------------

    def _build_image(self):
        """Compose the final image: flip + tint + squash."""
        # Choose correct facing direction
        src = self._img_right if self.facing_right else self._img_left
        img = src.copy()

        # Apply flash tint overlay
        if self.flash_type != self.FLASH_NONE and self.flash_timer > 0:
            # Pulse opacity for a blink effect
            pulse = self.flash_timer % 6
            if pulse < 3:
                alpha = 160
                if self.flash_type == self.FLASH_GOOD:
                    tint_color = (0, 255, 80, alpha)
                else:
                    tint_color = (255, 60, 60, alpha)

                tint_surf = pygame.Surface(img.get_size(), pygame.SRCALPHA)
                tint_surf.fill(tint_color)
                img.blit(tint_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # Apply squash / stretch (scale Y axis)
        if abs(self.squash - 1.0) > 0.01:
            w = img.get_width()
            h = img.get_height()
            new_h = max(1, int(h * self.squash))
            img = pygame.transform.smoothscale(img, (w, new_h))

        self.image = img

        # Recalculate draw rect keeping midbottom fixed to self.rect
        self.draw_rect = self.image.get_rect()
        self.draw_rect.midbottom = self.rect.midbottom

    def _draw_shadow(self):
        """Draw a soft ellipse shadow on the ground under Steve."""
        shadow_w = int(self.rect.width * 0.75)
        shadow_h = max(6, int(shadow_w * 0.22))

        shadow_surf = pygame.Surface((shadow_w, shadow_h), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, self.shadow_color,
                            (0, 0, shadow_w, shadow_h))

        sx = self.rect.centerx - shadow_w // 2
        sy = self.screen_rect.bottom - shadow_h - 4
        self.screen.blit(shadow_surf, (sx, sy))

    def _build_nametag(self):
        """Pre-render the 'Steve' name tag surface."""
        text = self.nametag_font.render("Steve", False, (255, 255, 255))
        pad = 6
        w = text.get_width() + pad * 2
        h = text.get_height() + pad

        tag = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(tag, (30, 30, 30, 180), (0, 0, w, h), border_radius=8)
        pygame.draw.rect(tag, (255, 255, 255, 180), (0, 0, w, h), width=2, border_radius=8)
        tag.blit(text, (pad, pad // 2))
        self.nametag_surf = tag

    def _draw_nametag(self):
        """Draw the name tag floating above Steve's head."""
        tag_rect = self.nametag_surf.get_rect()
        tag_rect.centerx = self.draw_rect.centerx
        tag_rect.bottom = self.draw_rect.top - 8
        self.screen.blit(self.nametag_surf, tag_rect)

    def resize(self):
        self.screen_rect = self.screen.get_rect()
