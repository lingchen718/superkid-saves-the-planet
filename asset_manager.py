import os
import pygame


class AssetManager:
    """Load and manage all game assets."""

    def __init__(self, settings):

        self.settings = settings

        # Dictionaries
        self.images = {
            "player": None,
            "items": {
                "good": [],
                "bad": []
            },
            "backgrounds": {},
            "intro": {},
            "win": {},
            "buttons": {}
        }
        self.sounds = {}
        self.music = {}
        self.fonts = {}

        # Load assets
        self.load_images()
        self.scale_images()
        self.load_sounds()
        self.load_music()
        self.load_fonts()


    def load_images(self):
        """Load all images."""

        player = pygame.image.load(
            os.path.join("images", "super_kid.png")
        ).convert_alpha()

        self.images["player"] = player

        # -------------------------
        # Good Items
        # -------------------------

        self.images["good_items"] = []

        for i in range(1, 11):
            filename = os.path.join(
                "images",
                f"good_{i}.png"
            )

            image = pygame.image.load(filename).convert_alpha()

            image = pygame.transform.scale(
                image,
                (
                    self.settings.item_width,
                    self.settings.item_height
                )
            )

            self.images["good_items"].append(image)

        # -------------------------
        # Bad Items
        # -------------------------

        self.images["bad_items"] = []

        for i in range(1, 11):
            filename = os.path.join(
                "images",
                f"bad_{i}.png"
            )

            image = pygame.image.load(filename).convert_alpha()

            image = pygame.transform.scale(
                image,
                (
                    self.settings.item_width,
                    self.settings.item_height
                )
            )

            self.images["bad_items"].append(image)

            # --------------------
            # Backgrounds
            # --------------------

            self.images["polluted_bg_raw"] = pygame.image.load(
                os.path.join("images", "polluted_4.png")
            ).convert()

            self.images["clean_bg_raw"] = pygame.image.load(
                os.path.join("images", "clean_1.png")
            ).convert()

            # --------------------
            # Intro Universe
            # --------------------

            try:
                self.images["intro_universe_raw"] = pygame.image.load(
                    os.path.join(
                        "images",
                        "intro_universe_bg.png"
                    )
                ).convert()

            except FileNotFoundError:

                self.images["intro_universe_raw"] = None

            # --------------------
            # Intro Earth
            # --------------------

            try:

                self.images["intro_earth_raw"] = pygame.image.load(
                    os.path.join(
                        "images",
                        "intro_polluted_earth.png"
                    )
                ).convert_alpha()

            except FileNotFoundError:

                self.images["intro_earth_raw"] = self.images["polluted_bg_raw"]

            # --------------------
            # Win Earth
            # --------------------

            try:

                self.images["win_earth_raw"] = pygame.image.load(
                    os.path.join(
                        "images",
                        "win_clean_earth.png"
                    )
                ).convert_alpha()

            except FileNotFoundError:

                self.images["win_earth_raw"] = self.images["clean_bg_raw"]

    def scale_images(self):

        w = self.settings.screen_width
        h = self.settings.screen_height

        self.images["polluted_bg"] = pygame.transform.scale(

            self.images["polluted_bg_raw"],

            (w, h)

        )
        self.images["clean_bg"] = pygame.transform.scale(

            self.images["clean_bg_raw"],

            (w, h)

        )

        if self.images["intro_universe_raw"] is not None:

            self.images["intro_universe"] = pygame.transform.scale(

                self.images["intro_universe_raw"],

                (w, h)

            )

        else:

            self.images["intro_universe"] = None

        raw = self.images["intro_earth_raw"]

        img_h = int(h * 0.58)

        img_w = int(
            raw.get_width() *
            img_h /
            raw.get_height()
        )

        self.images["intro_earth"] = pygame.transform.smoothscale(

            raw,

            (int(img_w * 1.2), int(img_h * 1.2))

        )

        raw = self.images["win_earth_raw"]

        win_h = int(h * 0.55)

        win_w = int(
            raw.get_width()
            * win_h
            / raw.get_height()
        )

        self.images["win_earth"] = pygame.transform.smoothscale(

            raw,

            (win_w, win_h)

        )

    def play_sound(self, name):
        """Play a sound effect."""

        sound = self.sounds.get(name)

        if sound:
            sound.play()
    def load_sounds(self):
        """Load all sound effects."""

        self.sounds["good"] = pygame.mixer.Sound(
            os.path.join(
                "sounds",
                "coinsplash.ogg"
            )
        )

        self.sounds["bad"] = pygame.mixer.Sound(
            os.path.join(
                "sounds",
                "alarm.ogg"
            )
        )

        self.sounds["quiz"] = pygame.mixer.Sound(
            os.path.join(
                "sounds",
                "magical_6.ogg"
            )
        )

        self.sounds["celebration"] = pygame.mixer.Sound(os.path.join("sounds", "newthingget.ogg"))

    def play_music(self, name, loops=-1):

        pygame.mixer.music.load(self.music[name])
        pygame.mixer.music.play(loops)


    def load_music(self):
        """Store background music file paths."""

        self.music["polluted"] = os.path.join(
            "sounds",
            "Iwan Gabovitch - Dark Ambience Loop.ogg"
        )

        self.music["clean"] = os.path.join(
            "sounds",
            "A Journey Awaits.ogg"
        )

    def stop_music(self):
        pygame.mixer.music.stop()

    def load_fonts(self):
        """Load all fonts."""

        font_regular = os.path.join("fonts", "ComicNeue-Regular.ttf")
        font_bold = os.path.join("fonts", "ComicNeue-Bold.ttf")

        self.fonts["title"] = pygame.font.Font(font_bold, 52)
        self.fonts["large"] = pygame.font.Font(font_bold, 42)
        self.fonts["medium"] = pygame.font.Font(font_regular, 30)
        self.fonts["small"] = pygame.font.Font(font_regular, 22)
        self.fonts["sub"] = pygame.font.Font(font_bold, 30)
        self.fonts["prompt"] = pygame.font.Font(font_bold, 30)
        self.fonts["headline"] = pygame.font.Font(font_bold, 58)
        self.fonts["win"] = pygame.font.Font(font_bold, 30)
        self.fonts["unlock"] = pygame.font.Font(font_bold, 58)
        self.fonts["exit"] = pygame.font.Font(font_bold, 35)
