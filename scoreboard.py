import pygame

class Scoreboard:
    """Kid-friendly HUD: big text + outlined font + rounded panels."""

    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.stats = game.stats

        # --- Toggle what to show (simplify for kids) ---
        self.SHOW_SCORE = False   # set True if you still want score
        self.SHOW_LIVES = True
        self.SHOW_HEALTH = True
        self.SHOW_ECO_ACTIONS = False  # New toggle for eco actions

        # --- Fonts (big + readable) ---
        self.font_big = game.assets.fonts["large"]
        self.font_med = game.assets.fonts["medium"]

        # --- Colors (high contrast) ---
        self.text_color = (255, 255, 255)
        self.outline_color = (10, 10, 10)

        self.panel_border = (255, 255, 255)

        # Panels per stat (fun colors)
        self.health_panel = (20, 120, 60)   # green
        self.lives_panel = (40, 90, 180)    # blue
        self.score_panel = (160, 90, 30)    # orange/brown
        self.eco_panel = (160, 90, 30)     # yellow/brown for eco actions

        # Health bar colors
        self.bar_bg = (230, 230, 230)
        self.bar_good = (60, 220, 90)
        self.bar_mid = (255, 200, 60)
        self.bar_bad = (255, 80, 80)

        # Prepare initial images
        self.prep_score()
        self.prep_planet_health()
        self.prep_eco_actions()  # Prepare eco actions
        self.prep_lives()


    # ---------------- PREP ----------------

    def prep_score(self):
        if not self.SHOW_SCORE:
            self.score_surf = None
            return
        score = getattr(self.stats, "score", 0)
        self.score_surf = self._render_outlined(f"SCORE  {score}", self.font_med)

    def prep_planet_health(self):
        if not self.SHOW_HEALTH:
            self.health_surf = None
            return
        health = getattr(self.stats, "planet_health", 0)
        self.health_surf = self._render_outlined(f"PLANET HEALTH  {int(health)}%", self.font_med)



    def prep_eco_actions(self):
        if not self.SHOW_ECO_ACTIONS:
            self.eco_surf = None
            return
        eco_actions = getattr(self.stats, "eco_actions", 0)
        self.eco_surf = self._render_outlined(f"ECO ACTIONS  {eco_actions}", self.font_med)

    def prep_lives(self):
        if not self.SHOW_LIVES:
            self.lives_surf = None
            return
        lives = getattr(self.stats, "kids_lives", 5)
        self.lives_surf = self._render_outlined(f"LIVES  {int(lives)}", self.font_med)

    # ---------------- DRAW ----------------

    def show_score(self):
        """Draw HUD cards in the top-right corner + health bar."""
        margin = int(self.screen_rect.width * 0.00001)
        x_left = self.screen_rect.left - margin
        y = 8

        # Stack cards from top to bottom
        if self.SHOW_HEALTH and self.health_surf:
            y = self._draw_card_topleft(self.health_surf, x_left, y, fill=self.health_panel)
            y += 10
            y = self._draw_health_bar_topleft(x_left, y)
            y += 14

        if self.SHOW_ECO_ACTIONS and self.eco_surf:
            y = self._draw_card_topleft(self.eco_surf, x_left, y, fill=self.eco_panel)
            y += 10

        if self.SHOW_LIVES and self.lives_surf:
            y = self._draw_card_topleft(self.lives_surf, x_left, y, fill=self.lives_panel)
            y += 10



        if self.SHOW_SCORE and self.score_surf:
            y = self._draw_card_topleft(self.score_surf, x_left, y, fill=self.score_panel)
            y += 10

    # ---------------- HEALTH BAR ----------------

    def _draw_health_bar_topleft(self, x_left, y_top):
        """Draw a rounded health bar under the Planet card."""
        bar_width = int(self.screen_rect.width * 0.22)
        bar_height = int(self.screen_rect.height * 0.02)

        health = getattr(self.stats, "planet_health", 0)
        health = max(0, min(100, float(health)))
        ratio = health / 100.0
        filled = int(bar_width * ratio)

        # Choose color by level
        if health >= 70:
            fill_color = self.bar_good
        elif health >= 35:
            fill_color = self.bar_mid
        else:
            fill_color = self.bar_bad

        rect = pygame.Rect(0, 0, bar_width, bar_height)
        rect.top = y_top
        rect.left = x_left

        # Background
        pygame.draw.rect(self.screen, self.bar_bg, rect, border_radius=12)
        pygame.draw.rect(self.screen, self.panel_border, rect, width=3, border_radius=12)

        # Filled portion
        if filled > 0:
            fill_rect = pygame.Rect(rect.x, rect.y, filled, rect.height)
            pygame.draw.rect(self.screen, fill_color, fill_rect, border_radius=12)

        return rect.bottom

    # ---------------- HELPERS ----------------

    def _render_outlined(self, text, font):
        """Render text with a thick outline for readability."""
        base = font.render(text, True, self.text_color)

        outline = font.render(text, True, self.outline_color)
        w, h = base.get_size()
        surf = pygame.Surface((w + 6, h + 6), pygame.SRCALPHA)

        # Thicker outline
        offsets = [
            (-2, 0), (2, 0), (0, -2), (0, 2),
            (-2, -2), (-2, 2), (2, -2), (2, 2),
            (-3, 0), (3, 0), (0, -3), (0, 3),
        ]
        for ox, oy in offsets:
            surf.blit(outline, (3 + ox, 3 + oy))
        surf.blit(base, (3, 3))
        return surf

    def _draw_card_topleft(self, text_surf, x_left, y_top, fill):
        """Draw a rounded panel card aligned to the top-left."""
        pad_x = int(self.screen_rect.width * 0.008)
        pad_y = int(self.screen_rect.height * 0.008)

        w = text_surf.get_width() + pad_x * 2
        h = text_surf.get_height() + pad_y * 2

        rect = pygame.Rect(0, 0, w, h)
        rect.top = y_top
        rect.left = x_left

        pygame.draw.rect(self.screen, fill, rect, border_radius=16)
        pygame.draw.rect(self.screen, self.panel_border, rect, width=3, border_radius=16)

        self.screen.blit(text_surf, (rect.x + pad_x, rect.y + pad_y))
        return rect.bottom
