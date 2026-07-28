class GameStats:
    """Track statistics for Super Kids Saves the Planet."""

    def __init__(self, game):
        """Initialize statistics."""
        self.settings = game.settings
        self.reset_stats()

        # Start at the intro screen
        self.game_active = False

    def reset_stats(self):
        """Reset statistics that change during a game."""

        self.kids_lives = self.settings.starting_lives
        self.planet_health = self.settings.starting_health

        self.score = 0
        self.eco_actions = 0

        # Start a new game

        self.game_active = True

    def update_score(self, points):
        """Update score and planet health."""

        self.score += points

        if points > 0:
            self.planet_health += points
        else:
            self.planet_health += points
            self.kids_lives -= 1

        self.planet_health = max(
            0,
            min(100, self.planet_health)
        )

        if self.kids_lives <= 0 or self.planet_health <= 0:
            self.game_active = False

    def increment_eco_actions(self):
        """Increment eco actions."""
        self.eco_actions += 1