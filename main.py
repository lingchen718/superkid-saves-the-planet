import sys
import random
import pygame
import math
import time
import os
import asyncio
from settings import SuperKidsSettings
from asset_manager import AssetManager
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from SuperKid import SuperKid
from FallingItems import FallingItem




# ─────────────────────────────────────────
#  EDUCATIONAL DATA  (easy to expand later)
# ─────────────────────────────────────────

ECO_QUIZZES = [
    {
        "question": "What bin do we use for paper?",
        "options":  ["A: Blue Bin", "B: Red Bin", "C: Green Bin"],
        "answer":   0,
        "hint":     "Paper goes in the blue bin for recycling!",
    },
    {
        "question": "What do trees take in from the air?",
        "options":  ["A: Oxygen", "B: Water", "C: Carbon Dioxide"],
        "answer":   2,
        "hint":     "Trees help us by taking in carbon dioxide!",
    },
    {
        "question": "What energy comes from the sun?",
        "options":  ["A: Wind", "B: Solar", "C: Coal"],
        "answer":   1,
        "hint":     "Solar energy comes from sunlight!",
    },
    {
        "question": "How long does plastic last in the ground?",
        "options":  ["A: 1 year", "B: 10 years", "C: 500 years"],
        "answer":   2,
        "hint":     "Plastic takes a very long time to break down!",
    },
    {
        "question": "What do the '3 Rs' mean?",
        "options":  ["A: Read, Relax, Repeat", "B: Reduce, Reuse, Recycle", "C: Run, Jump, Play"],
        "answer":   1,
        "hint":     "Reduce, Reuse, and Recycle help the Earth!",
    },
    {
        "question": "Where do we put fruit peels?",
        "options":  ["A: Trash", "B: Compost", "C: Recycle Bin"],
        "answer":   1,
        "hint":     "Fruit peels can go in the compost bin!",
    },
    {
        "question": "What should you do with the water while brushing teeth?",
        "options":  ["A: Let it run", "B: Turn it off", "C: Fill the sink"],
        "answer":   1,
        "hint":     "Turning off the water saves it!",
    },
    {
        "question": "Which animal can get hurt by plastic in the ocean?",
        "options":  ["A: Fish", "B: Cat", "C: Dog"],
        "answer":   0,
        "hint":     "Fish can eat plastic and get sick!",
    },
    {
        "question": "What is made by wind?",
        "options":  ["A: Wind Energy", "B: Water Energy", "C: Fire Energy"],
        "answer":   0,
        "hint":     "Wind energy helps us make electricity!",
    },
    {
        "question": "What happens if we cut too many trees?",
        "options":  ["A: More air", "B: Animals lose homes", "C: More fruits"],
        "answer":   1,
        "hint":     "Trees are homes for many animals!",
    },
    {
        "question": "Which uses less water: a shower or a bath?",
        "options":  ["A: Shower", "B: Bath", "C: Both use the same"],
        "answer":   0,
        "hint":     "Showers usually use less water than baths!",
    },
    {
        "question": "What color is clean water?",
        "options":  ["A: Brown", "B: Blue", "C: Green"],
        "answer":   1,
        "hint":     "Clean water is clear and blue!",
    },
    {
        "question": "What do plants need to grow?",
        "options":  ["A: Sun and water", "B: Rocks", "C: Toys"],
        "answer":   0,
        "hint":     "Plants need sunlight and water to grow!",
    },
    {
        "question": "Which bag is best for the Earth?",
        "options":  ["A: Plastic bag", "B: Paper bag", "C: Reusable bag"],
        "answer":   2,
        "hint":     "Reusable bags are good for the Earth!",
    },
    {
        "question": "What should you do when you leave a room?",
        "options":  ["A: Leave lights on", "B: Turn off lights", "C: Close the door"],
        "answer":   1,
        "hint":     "Turning off lights saves energy!",
    },
    {
        "question": "Where can we find fresh water?",
        "options":  ["A: Ocean", "B: River", "C: Pool"],
        "answer":   1,
        "hint":     "Rivers have fresh water for us to use!",
    },
    {
        "question": "What is littering?",
        "options":  ["A: Throwing trash on the ground", "B: Picking up trash", "C: Cleaning up"],
        "answer":   0,
        "hint":     "Littering is bad for the Earth!",
    },
    {
        "question": "How can we save energy at home?",
        "options":  ["A: Turn off devices not in use", "B: Leave everything on", "C: Use more lights"],
        "answer":   0,
        "hint":     "Turning off devices saves energy!",
    },
    {
        "question": "What do bees do for flowers?",
        "options":  ["A: Help them grow", "B: Eat them", "C: Make them sick"],
        "answer":   0,
        "hint":     "Bees help flowers grow by spreading pollen!",
    },
    {
        "question": "Why should we plant trees?",
        "options":  ["A: For fresh air", "B: To block the sun", "C: To make noise"],
        "answer":   0,
        "hint":     "Trees give us fresh air to breathe!",
    },
]

MATH_QUIZZES = [
    {
        "question": "What is 36 + 3?",
        "options":  ["A: 38", "B: 39", "C: 40"],
        "answer":   1,
        "hint":     "Add: 36 plus 3 equals 39. Good counting!",
    },
    {
        "question": "If you have 15 apples and eat 4, how many left?",
        "options":  ["A: 10", "B: 11", "C: 12"],
        "answer":   1,
        "hint":     "Subtract: 15 minus 4 equals 11. Yummy apples!",
    },
    {
        "question": "What is 18 + 6?",
        "options":  ["A: 23", "B: 24", "C: 25"],
        "answer":   1,
        "hint":     "Add: 18 plus 6 equals 24. Keep going!",
    },
    {
        "question": "You have 20 toys. Give away 5. How many now?",
        "options":  ["A: 14", "B: 15", "C: 16"],
        "answer":   1,
        "hint":     "Subtract: 20 minus 5 equals 15. Fun toys!",
    },
    {
        "question": "What is 19 + 4?",
        "options":  ["A: 23", "B: 24", "C: 25"],
        "answer":   0,
        "hint":     "Add: 19 plus 4 equals 23. Nice work!",
    },
    {
        "question": "If you have 16 candies and share 3, how many left?",
        "options":  ["A: 12", "B: 13", "C: 14"],
        "answer":   1,
        "hint":     "Subtract: 16 minus 3 equals 13. Sweet sharing!",
    },
    {
        "question": "What is 14 + 8?",
        "options":  ["A: 15", "B: 22", "C: 17"],
        "answer":   1,
        "hint":     "Add: 14 plus 8 equals 22. Easy one!",
    },
    {
        "question": "You have 19 books. Read 6. How many left?",
        "options":  ["A: 12", "B: 13", "C: 14"],
        "answer":   1,
        "hint":     "Subtract: 19 minus 6 equals 13. Read more!",
    },
    {
        "question": "What is 18 + 15?",
        "options":  ["A: 30", "B: 33", "C: 36"],
        "answer":   1,
        "hint":     "Add: 18 plus 15 equals 33. Great job!",
    },
    {
        "question": "If you have 17 balls and lose 5, how many now?",
        "options":  ["A: 12", "B: 13", "C: 14"],
        "answer":   0,
        "hint":     "Subtract: 17 minus 5 equals 12. Bounce on!",
    },
    {
        "question": "What is 15 + 3 + 6?",
        "options":  ["A: 22", "B: 24", "C: 26"],
        "answer":   1,
        "hint":     "Equals 24. Count up!",
    },
    {
        "question": "You have 18 flowers. Pick 7. How many left?",
        "options":  ["A: 10", "B: 11", "C: 12"],
        "answer":   1,
        "hint":     "Subtract: 18 minus 7 equals 11. Pretty flowers!",
    },
    {
        "question": "What is 21 + 8 + 1?",
        "options":  ["A: 29", "B: 30", "C: 31"],
        "answer":   1,
        "hint":     "Equals 30. Well done!",
    },
    {
        "question": "What is 30 + 8 + 2?",
        "options":  ["A: 36", "B: 38", "C: 40"],
        "answer":   2,
        "hint":     "Equals 40. Happy dogs!",
    },
    {
        "question": "What is 20 - 5 - 1?",
        "options":  ["A: 16", "B: 14", "C: 13"],
        "answer":   1,
        "hint":     "Equals 14. Think step by step!",
    },
    {
        "question": "You have 12 pencils. Use 3. How many left?",
        "options":  ["A: 7", "B: 8", "C: 9"],
        "answer":   2,
        "hint":     "Subtract: 12 minus 3 equals 9. Draw away!",
    },
    {
        "question": "What is 19 + 10 + 1?",
        "options":  ["A: 28", "B: 29", "C: 30"],
        "answer":   2,
        "hint":     "Equals 30. Almost there!",
    },
    {
        "question": "13 birds on the tree,4 fly away, how many left?",
        "options":  ["A: 8", "B: 9", "C: 10"],
        "answer":   1,
        "hint":     "Subtract: 13 minus 4 equals 9. Birds sing!",
    },
    {
        "question": "What is 11 + 7 + 3?",
        "options":  ["A: 19", "B: 20", "C: 21"],
        "answer":   2,
        "hint":     "Equals 21. Fly high!",
    },
    {
        "question": "You have 20 stars. Color 6. How many left?",
        "options":  ["A: 14", "B: 15", "C: 16"],
        "answer":   0,
        "hint":     "Subtract: 20 minus 6 equals 14. Shiny stars!",
    },
    {
        "question": "What is 25 - 6?",
        "options":  ["A: 18", "B: 19", "C: 20"],
        "answer":   1,
        "hint":     "Eequals 19. Count down!",
    },
    {
        "question": "If you have 14 cakes and eat 5, how many now?",
        "options":  ["A: 8", "B: 9", "C: 10"],
        "answer":   0,
        "hint":     "Subtract: 14 minus 5 equals 9. Tasty cakes!",
    },
    {
        "question": "What is 12 + 14?",
        "options":  ["A: 26", "B: 27", "C: 28"],
        "answer":   0,
        "hint":     "Equals 26. Sweet treat!",
    },
    {
        "question": "You have 17 fish. Catch 3. How many left?",
        "options":  ["A: 13", "B: 14", "C: 15"],
        "answer":   1,
        "hint":     "Subtract: 17 minus 3 equals 14. Swim on!",
    },
    {
        "question": "What is 38 + 8?",
        "options":  ["A: 46", "B: 47", "C: 48"],
        "answer":   0,
        "hint":     "Equals 46. Big number!",
    },
    {
        "question": "If you have 10 bananas and add 6, how many?",
        "options":  ["A: 15", "B: 16", "C: 17"],
        "answer":   1,
        "hint":     "Add: 10 plus 6 equals 16. Healthy snack!",
    },
    {
        "question": "What is 23 - 7?",
        "options":  ["A: 16", "B: 17", "C: 18"],
        "answer":   0,
        "hint":     "Equals 16. Peel it!",
    },
    {
        "question": "You have 19 cars. Park 8. How many left?",
        "options":  ["A: 10", "B: 11", "C: 12"],
        "answer":   1,
        "hint":     "Subtract: 19 minus 8 equals 11. Vroom!",
    },
    {
        "question": "What is 56 + 3?",
        "options":  ["A: 57", "B: 58", "C: 59"],
        "answer":   2,
        "hint":     "Equals 59. Drive safe!",
    },
    {
        "question": "If you have 11 dolls and buy 5 more, how many?",
        "options":  ["A: 15", "B: 16", "C: 17"],
        "answer":   1,
        "hint":     "Add: 11 plus 5 equals 16. Play time!",
    },
    {
        "question": "What is 80 - 8?",
        "options":  ["A: 70", "B: 71", "C: 72"],
        "answer":   2,
        "hint":     "Equals 72. Number fun!",
    },
    {
        "question": "You have 15 eggs. Use 4. How many left?",
        "options":  ["A: 10", "B: 11", "C: 12"],
        "answer":   1,
        "hint":     "Subtract: 15 minus 4 equals 11. Bake on!",
    },
    {
        "question": "What is 84 + 5?",
        "options":  ["A: 87", "B: 88", "C: 93"],
        "answer":   2,
        "hint":     "Equals 93. Egg-cellent!",
    },
    {
        "question": "If you have 12 kites and 3 break, how many now?",
        "options":  ["A: 9", "B: 10", "C: 11"],
        "answer":   0,
        "hint":     "Subtract: 12 minus 3 equals 9. Fly high!",
    },
    {
        "question": "What is 47 + 1?",
        "options":  ["A: 48", "B: 59", "C: 60"],
        "answer":   0,
        "hint":     "Equals 48. Windy day!",
    },
    {
        "question": "You have 18 buttons. Lose 6. How many left?",
        "options":  ["A: 11", "B: 12", "C: 13"],
        "answer":   1,
        "hint":     "Subtract: 18 minus 6 equals 12. Sew it up!",
    },
    {
        "question": "What is 80 + 9?",
        "options":  ["A: 89", "B: 90", "C: 91"],
        "answer":   0,
        "hint":     "Equals 89. Button fun!",
    },
    {
        "question": "If you have 13 chairs and add 4, how many?",
        "options":  ["A: 16", "B: 17", "C: 18"],
        "answer":   1,
        "hint":     "Add: 13 plus 4 equals 17. Sit down!",
    },
    {
        "question": "What is 55 - 2?",
        "options":  ["A: 53", "B: 54", "C: 55"],
        "answer":   0,
        "hint":     "Equals 53. Chair time!",
    },
    {
        "question": "You have 19 hats. Give 7 away. How many now?",
        "options":  ["A: 10", "B: 11", "C: 12"],
        "answer":   2,
        "hint":     "Subtract: 19 minus 7 equals 12. Hat party!",
    },
    {
        "question": "What is 45 + 6?",
        "options":  ["A: 49", "B: 50", "C: 51"],
        "answer":   2,
        "hint":     "Equals 51. Cover up!",
    },
    {
        "question": "If you have 16 spoons and use 5, how many left?",
        "options":  ["A: 10", "B: 11", "C: 12"],
        "answer":   1,
        "hint":     "Subtract: 16 minus 5 equals 11. Eat up!",
    },
    {
        "question": "What is 42 - 3?",
        "options":  ["A: 37", "B: 38", "C: 39"],
        "answer":   2,
        "hint":     "Equals 39. Spoon fun!",
    },
    {
        "question": "You have 14 clocks. Set 2. How many left?",
        "options":  ["A: 11", "B: 12", "C: 13"],
        "answer":   1,
        "hint":     "Subtract: 14 minus 2 equals 12. Tick tock!",
    },
    {
        "question": "What is 18 + 6?",
        "options":  ["A: 17", "B: 18", "C: 24"],
        "answer":   2,
        "hint":     "Equals 24. Time flies!",
    },
    {
        "question": "If you have 20 leaves and pick 9, how many?",
        "options":  ["A: 10", "B: 11", "C: 12"],
        "answer":   1,
        "hint":     "Subtract: 20 minus 9 equals 11. Fall leaves!",
    },
    {
        "question": "What is 33 + 8?",
        "options":  ["A: 43", "B: 42", "C: 41"],
        "answer":   2,
        "hint":     "Equals 41. Leaf pile!",
    },
    {
        "question": "You have 10 windows. Open 1 more. How many open?",
        "options":  ["A: 10", "B: 11", "C: 12"],
        "answer":   1,
        "hint":     "Add: 10 plus 1 equals 11. Fresh air!",
    },
    {
        "question": "What is 27 - 4 - 3?",
        "options":  ["A: 20", "B: 23", "C: 24"],
        "answer":   0,
        "hint":     "Equals 20. Window view!",
    },
]

# ─────────────────────────────────────────
#  INTRO STORY LINES
# ─────────────────────────────────────────
INTRO_STORY_LINES = [
    "Our beautiful planet is in DANGER...",
    "Factories pour smoke into the skies.",
    "Plastic chokes our rivers and oceans.",
    "Animals lose their homes every single day.",
    "The air we breathe is no longer clean.",
    "The Earth is crying out for help!",
    "",
    "But there is still HOPE...",
    "YOU can make a difference!",
    "Collect eco-friendly items, answer questions,",
    "and SAVE THE PLANET before it is too late!",
]

# ─────────────────────────────────────────
#  WIN SCREEN MESSAGES
# ─────────────────────────────────────────
WIN_LINES = [
    "YOU DID IT, SUPERKID!",
    "The planet is healthy and beautiful again!"
]


class SuperKidsGame:
    """SuperKid Saves the Planet — Educational Edition"""

    # ─────────────────────────────────────────
    #  INIT
    # ─────────────────────────────────────────
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = SuperKidsSettings()

        self._quiz_option_rects = []

        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        display_info = pygame.display.Info()

        self.screen = pygame.display.set_mode(
            (display_info.current_w, display_info.current_h)
        )
        self.settings.screen_width  = display_info.current_w
        self.settings.screen_height = display_info.current_h
        pygame.display.set_caption("SuperKid Saves the Planet")

        self.assets = AssetManager(self.settings)


        # ── Sound effects ─────────────────────────────────────────
        pygame.mixer.init()
        self.good_sound = self.assets.sounds["good"]
        self.bad_sound = self.assets.sounds["bad"]
        self.quiz_sound = self.assets.sounds["quiz"]

        # ── Music tracks ──────────────────────────────────────────
        self.polluted_music_path = self.assets.music["polluted"]
        self.clean_music_path = self.assets.music["clean"]
        self.current_music_mode  = None

        self.settings.clean_mode = False
        self._play_music("polluted")

        # ── Core objects ──────────────────────────────────────────
        self.stats = GameStats(self)
        self.sb    = Scoreboard(self)
        self.kid   = SuperKid(self)
        self.items = pygame.sprite.Group()

        # ── Educational state ─────────────────────────────────────
        self.fact_message  = ""
        self.fact_timer    = 0
        self.FACT_DURATION = 180

        self.quiz_active        = False
        self.current_quiz       = None
        self.quiz_result        = None
        self.quiz_result_timer  = 0
        self.items_caught       = 1
        self.QUIZ_INTERVAL      = 5

        # ── Planet health ─────────────────────────────────────────
        self.planet_health = 0
        self.stats.update_score(self.settings.bad_points)
        self.eco_actions   = 0

        self.clean_mode_triggered = False
        self.clean_msg_timer      = 0
        self.CLEAN_MSG_DURATION   = 180

        # ── Fonts ─────────────────────────────────────────────────
        self.font_large = self.assets.fonts["large"]
        self.font_medium = self.assets.fonts["medium"]
        self.font_small = self.assets.fonts["small"]

        # ── Background images ─────────────────────────────────────

        self.polluted_bg = self.assets.images["polluted_bg"]
        self.clean_bg = self.assets.images["clean_bg"]

        # ── Intro background: universe image ──────────────────────
        # Place your space/universe artwork at images/intro_universe_bg.png
        self.intro_universe_bg = self.assets.images["intro_universe"]

        self.current_bg = self.polluted_bg

        # ── Intro screen image (polluted Earth) ───────────────────
        # Place your polluted-earth artwork at images/intro_polluted_earth.png
        # Falls back gracefully if the file is missing.
        self.intro_earth_img = self.assets.images["intro_earth"]

        # ── Win screen image (beautiful Earth) ────────────────────
        # Place your clean-earth artwork at images/win_clean_earth.png
        self.win_earth_img = self.assets.images["win_earth"]

        # ── Win-screen particle system ────────────────────────────
        self._win_particles = []

        # ── Intro / win state ─────────────────────────────────────
        # game_state: "intro" | "playing" | "won" | "gameover"
        self.game_state = "intro"

        # ── Intro subtitle state (pre-initialise) ─────────────────
        self._intro_sub_timer = 0
        self._intro_sub_index = 0
        self._intro_sub_alpha = 0
        self._intro_sub_fading = False
        self._intro_lines_done = False  # replaces the old flag
        self.congratulation_timer = 0

        # ── TIME LIMIT ────────────────────────────────────────────
        self.GAME_DURATION   = 5 * 60
        self.game_start_time = None
        self.time_up         = False

        # ── Game state ────────────────────────────────────────────
        self.stats.game_active = False
        self.play_button       = Button(self, "Start Game")
        self.restart_button = Button(self, "Play Again")
        self.game_won          = False
        self.running = True

    # ─────────────────────────────────────────
    #  MAIN LOOP
    # ─────────────────────────────────────────

    async def run_game(self):
        """Main game loop — dispatches based on game_state."""
        while True:
            self._check_events()

            if self.game_state == "intro":
                self._update_intro()
                self._draw_intro_screen()

            elif self.game_state == "playing":
                # ── TIME LIMIT ────────────────────────────────────
                if self.stats.game_active and self.game_start_time is not None:
                    elapsed = time.time() - self.game_start_time
                    if elapsed >= self.GAME_DURATION and not self.time_up:
                        self.time_up = True
                        self.stats.game_active = False
                        self.game_state = "gameover"
                        pygame.mouse.set_visible(True)
                        print("[Game] Time's up! Game over.")

                self._update_music_for_mode()

                if self.stats.game_active and not self.quiz_active:
                    self.kid.update()
                    self._update_items()
                    self._check_clean_mode_trigger()
                    self._tick_timers()

                # Check win
                if self.game_won:
                    self.game_state = "won"
                    self._init_win_screen()

                self._update_screen()

            elif self.game_state == "won":
                self._update_win_particles()
                self._draw_win_screen()

            elif self.game_state == "gameover":
                self._update_screen()

            pygame.display.flip()
            self.clock.tick(self.settings.fps)
            await asyncio.sleep(0)

    # ─────────────────────────────────────────

    #  INTRO SCREEN
    # ─────────────────────────────────────────

    def _update_intro(self):
        """
        Advance the subtitle-style display each frame.
        Each line is shown for INTRO_LINE_HOLD frames, then replaced by the next.
        Empty lines act as short pauses.
        """
        INTRO_LINE_HOLD = 80  # frames a full line stays visible (~2.8 s at 60 fps)
        INTRO_LINE_PAUSE = 30  # frames an empty/pause line waits

        # Initialise subtitle state on first call
        if not hasattr(self, '_intro_sub_timer'):
            self._intro_sub_timer = 0
            self._intro_sub_index = 0
            self._intro_sub_alpha = 0
            self._intro_sub_fading = False

        if self._intro_lines_done:
            return

        hold = INTRO_LINE_PAUSE if (
                self._intro_sub_index < len(INTRO_STORY_LINES)
                and INTRO_STORY_LINES[self._intro_sub_index] == ""
        ) else INTRO_LINE_HOLD

        if not self._intro_sub_fading:
            self._intro_sub_alpha = min(255, self._intro_sub_alpha + 10)
            self._intro_sub_timer += 1
            if self._intro_sub_timer >= hold:
                self._intro_sub_fading = True
        else:
            self._intro_sub_alpha = max(0, self._intro_sub_alpha - 14)
            if self._intro_sub_alpha == 0:
                self._intro_sub_index += 1
                self._intro_sub_timer = 0
                self._intro_sub_fading = False
                if self._intro_sub_index >= len(INTRO_STORY_LINES):
                    self._intro_lines_done = True

    def _draw_intro_screen(self):
        """
        Intro / story screen:
        - Universe image fills the entire background
        - Earth centred on screen with a thin flickering icy-blue rim
        - Title above the earth
        - Film-subtitle text below the earth, one sentence at a time
        - Pulsing 'Press ENTER to Begin' at the bottom
        """
        sw = self.settings.screen_width
        sh = self.settings.screen_height
        t = pygame.time.get_ticks() * 0.001

        # ── 1. Background — universe image (or dark fallback) ─────────
        if self.intro_universe_bg is not None:
            self.screen.blit(self.intro_universe_bg, (0, 0))
        else:
            # Fallback: deep space dark fill
            self.screen.fill((8, 9, 14))

        # Optional: very subtle darkening vignette so the edges feel deep
        vignette = pygame.Surface((sw, sh), pygame.SRCALPHA)
        for i in range(8):
            radius = int(sh * 0.75) - i * 30
            if radius <= 0:
                continue
            alpha = 6 + i * 3
            fog = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.ellipse(fog, (0, 0, 0, alpha), fog.get_rect())
            # Blit as a subtractive darkening layer at screen centre
            self.screen.blit(
                fog,
                (sw // 2 - radius, sh // 2 - radius),
                special_flags=pygame.BLEND_RGBA_SUB
            )

        # ── 2. Earth image — centred ──────────────────────────────────
        img = self.intro_earth_img
        img_x = sw // 2 - img.get_width() // 2
        img_y = int(sh * 0.12)

        draw_x = int(img_x * 0.99)
        draw_y = int(img_y * 1.1)

        fast_pulse = math.sin(t * 2.3)

        # Pulse the earth image alpha directly — no rim at all
        earth_alpha = int(200 + fast_pulse * 55)  # range: 145 – 255
        pulsed_earth = img.copy()
        pulsed_earth.set_alpha(earth_alpha)

        self.screen.blit(pulsed_earth, (draw_x, draw_y))

        # ── 3. Game title — above the earth ───────────────────────────
        title_font = self.assets.fonts["title"]
        shimmer = math.sin(t * 1.6)
        tc_r = int(160 + shimmer * 60)
        tc_g = int(200 + shimmer * 40)
        tc_b = int(230 + shimmer * 25)
        title_surf = title_font.render("SuperKid Saves the Planet", True, (tc_r, tc_g, tc_b))
        title_shadow = title_font.render("SuperKid Saves the Planet", True, (10, 14, 25))
        title_x = sw // 2 - title_surf.get_width() // 2
        title_y = int(sh * 0.02)
        self.screen.blit(title_shadow, (title_x + 3, title_y + 3))
        self.screen.blit(title_surf, (title_x, title_y))

        # ── 4. Subtitle text — one line at a time below the earth ─────
        # sub_font = pygame.font.SysFont("Arial Rounded MT Bold", 30)
        sub_font = self.assets.fonts["sub"]
        sub_y = img_y + img.get_height() - 20

        if hasattr(self, '_intro_sub_index') and not self._intro_lines_done:
            idx = self._intro_sub_index
            line = INTRO_STORY_LINES[idx] if idx < len(INTRO_STORY_LINES) else ""
        elif self._intro_lines_done:
            line = "Are you ready to be the hero our planet needs?"
        else:
            line = ""

        if line:
            if any(kw in line for kw in
                   ("DANGER", "smoke", "chokes", "lose", "crying", "longer", "Plastic", "Animals")):
                sub_color = (200, 80, 70)
            elif any(kw in line for kw in
                     ("HOPE", "YOU", "SAVE", "difference", "Collect", "answer", "hero", "ready")):
                sub_color = (100, 200, 160)
            else:
                sub_color = (190, 200, 215)

            alpha = getattr(self, '_intro_sub_alpha', 255)
            line_surf = sub_font.render(line, True, sub_color)
            shadow_surf = sub_font.render(line, True, (5, 8, 15))
            sub_x = sw // 2 - line_surf.get_width() // 2

            # Cinema backing bar (semi-transparent, keeps subtitle readable over stars)
            bar_pad = 28
            bar_w = line_surf.get_width() + bar_pad * 2
            bar_h = line_surf.get_height() + 18
            bar_surf = pygame.Surface((bar_w, bar_h), pygame.SRCALPHA)
            bar_surf.fill((0, 0, 0, int(alpha * 0.55)))
            self.screen.blit(bar_surf, (sw // 2 - bar_w // 2, sub_y - 9))

            shadow_surf.set_alpha(alpha)
            line_surf.set_alpha(alpha)
            self.screen.blit(shadow_surf, (sub_x + 2, sub_y + 2))
            self.screen.blit(line_surf, (sub_x, sub_y))

        # ── 5. Pulsing "Press ENTER to Begin" ─────────────────────────
        pulse = 0.65 + 0.35 * math.sin(t * 3.0)
        # prompt_font = pygame.font.SysFont("Arial Rounded MT Bold", 30, bold=True)
        prompt_font = self.assets.fonts["prompt"]
        pr = int(160 * pulse + 60)
        pg = int(200 * pulse + 40)
        pb = int(230 * pulse + 25)
        prompt_surf = prompt_font.render(
            "Press ENTER to Begin Your Mission!", True, (pr, pg, pb)
        )
        prompt_x = sw // 2 - prompt_surf.get_width() // 2
        prompt_y = int(sh * 0.86)

        gp_w = prompt_surf.get_width() + 44
        gp_h = prompt_surf.get_height() + 18
        gp = pygame.Surface((gp_w, gp_h), pygame.SRCALPHA)
        gp.fill((0, 0, 0, int(90 * pulse)))
        self.screen.blit(gp, (prompt_x - 22, prompt_y - 9))

        prompt_shadow = prompt_font.render(
            "Press ENTER to Begin Your Mission!", True, (5, 8, 18)
        )
        self.screen.blit(prompt_shadow, (prompt_x + 2, prompt_y + 2))
        self.screen.blit(prompt_surf, (prompt_x, prompt_y))

    #  WIN SCREEN
    # ─────────────────────────────────────────

    def _init_win_screen(self):
        """Set up the win screen state (called once when transitioning to 'won')."""
        self._win_start_ticks = pygame.time.get_ticks()
        self._win_particles   = []
        # Spawn initial burst of celebratory particles
        for _ in range(120):
            self._spawn_win_particle(burst=True)
        # Play celebration sound
        pygame.mixer.music.stop()
        self.assets.play_sound("celebration")
        # Try to play a happy ending track
        try:
            pygame.mixer.music.load(self.clean_music_path)
            pygame.mixer.music.set_volume(0.8)
            pygame.mixer.music.play(-1)
        except Exception:
            pass

    def _spawn_win_particle(self, burst=False):
        """Create one confetti / star particle for the win screen."""
        sw = self.settings.screen_width
        sh = self.settings.screen_height
        colors = [
            (255, 220, 50),   # gold
            (100, 255, 120),  # eco-green
            (80, 200, 255),   # sky blue
            (255, 120, 180),  # pink
            (255, 255, 255),  # white
            (180, 255, 100),  # lime
        ]
        self._win_particles.append({
            "x":      random.randint(0, sw),
            "y":      random.randint(-40, sh // 2) if burst else random.randint(-80, -10),
            "vx":     random.uniform(-1.5, 1.5),
            "vy":     random.uniform(1.5, 4.5),
            "size":   random.randint(4, 12),
            "color":  random.choice(colors),
            "alpha":  255,
            "shape":  random.choice(["circle", "rect", "star"]),
            "angle":  random.uniform(0, 360),
            "spin":   random.uniform(-4, 4),
        })

    def _update_win_particles(self):
        """Move and spawn particles each frame."""
        sw = self.settings.screen_width
        sh = self.settings.screen_height
        # Spawn new particles continuously
        if random.randint(1, 3) == 1:
            self._spawn_win_particle()

        alive = []
        for p in self._win_particles:
            p["x"]     += p["vx"]
            p["y"]     += p["vy"]
            p["angle"] += p["spin"]
            p["alpha"]  = max(0, p["alpha"] - 0.8)
            if p["y"] < sh + 20 and p["alpha"] > 0:
                alive.append(p)
        self._win_particles = alive

    def _draw_win_screen(self):
        """
        Full-screen win/congratulations screen:
        - Beautiful clean Earth image
        - Congratulation message lines
        - Confetti particle rain
        - 'Press ENTER to Exit' prompt
        """
        sw = self.settings.screen_width
        sh = self.settings.screen_height
        t  = pygame.time.get_ticks() * 0.001

        # ── 1. Deep sky / sunrise gradient background ──────────────
        for y in range(sh):
            ratio = y / sh
            r = int(10  + (135 - 10)  * ratio)
            g = int(15  + (206 - 15)  * ratio)
            b = int(30  + (235 - 30)  * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (sw, y))

        # ── 2. Draw confetti particles ────────────────────────────
        for p in self._win_particles:
            surf = pygame.Surface((p["size"] * 2, p["size"] * 2), pygame.SRCALPHA)
            col  = (*p["color"], int(p["alpha"]))
            if p["shape"] == "circle":
                pygame.draw.circle(surf, col, (p["size"], p["size"]), p["size"])
            elif p["shape"] == "rect":
                pygame.draw.rect(surf, col, surf.get_rect())
            else:  # star — approximate with two overlapping rects
                pygame.draw.rect(surf, col,
                                 pygame.Rect(p["size"] // 2, 0, p["size"], p["size"] * 2))
                pygame.draw.rect(surf, col,
                                 pygame.Rect(0, p["size"] // 2, p["size"] * 2, p["size"]))
            rotated = pygame.transform.rotate(surf, p["angle"])
            self.screen.blit(rotated,
                             (int(p["x"]) - rotated.get_width()  // 2,
                              int(p["y"]) - rotated.get_height() // 2))

        # ── 3. Clean Earth image — centred ────────────────────────
        img    = self.win_earth_img
        img_x  = sw // 2 - img.get_width() // 2
        img_y  = int(sh * 0.10)

        # Pulsing golden-green glow
        glow_r    = int(img.get_width() * 0.55 + math.sin(t * 1.8) * 14)
        glow_surf = pygame.Surface((glow_r * 2, glow_r * 2), pygame.SRCALPHA)
        for step in range(glow_r, 0, -6):
            fade_a = int(50 * step / glow_r)
            pygame.draw.ellipse(
                glow_surf,
                (80, 220, 80, fade_a),
                pygame.Rect(glow_r - step, glow_r - step, step * 2, step * 2)
            )
        cx_win = img_x + img.get_width() // 2
        cy_win = img_y + img.get_height() // 2
        self.screen.blit(glow_surf, (cx_win - glow_r, cy_win - glow_r))
        self.screen.blit(img, (img_x, img_y))

        # ── 4. Congratulation headline ────────────────────────────
        # headline_font = pygame.font.SysFont("Arial Rounded MT Bold", 58, bold=True)
        headline_font = self.assets.fonts["headline"]
        headline_text = "CONGRATULATIONS, SUPERKID!"

        shimmer_boost = int(math.sin(t * 3.0) * 30)
        hl_color      = (min(255, 80 + shimmer_boost), 255, min(255, 80 + shimmer_boost))

        hl_surf    = headline_font.render(headline_text, True, hl_color)
        hl_shadow  = headline_font.render(headline_text, True, (20, 60, 20))
        hl_x       = sw // 2 - hl_surf.get_width() // 2
        hl_y       = img_y + img.get_height() + 18

        # Subtle scale-pulse on the headline
        scale_pulse = 1.0 + 0.025 * math.sin(t * 2.5)
        pw = max(1, int(hl_surf.get_width()  * scale_pulse))
        ph = max(1, int(hl_surf.get_height() * scale_pulse))
        hl_surf_scaled = pygame.transform.smoothscale(hl_surf, (pw, ph))
        hl_x_scaled    = sw // 2 - pw // 2

        self.screen.blit(hl_shadow, (hl_x + 3, hl_y + 3))
        self.screen.blit(hl_surf_scaled, (hl_x_scaled, hl_y))

        # ── 5. Congratulation sub-lines ───────────────────────────
        # win_font   = pygame.font.SysFont("Arial Rounded MT Bold", 28)
        win_font = self.assets.fonts["win"]
        line_y     = hl_y + hl_surf.get_height() + 18
        line_gap   = 36


        for i, line in enumerate(WIN_LINES):
            if not line:
                line_y += line_gap // 2
                continue
            # Staggered fade-in: each line appears 0.3 s after the previous
            delay_s    = i * 0.30
            elapsed_s  = pygame.time.get_ticks() * 0.001 - getattr(self, "_win_start_ticks", 0) * 0.001
            fade_alpha = min(255, max(0, int((elapsed_s - delay_s) * 300)))

            if any(kw in line for kw in ("YOU DID IT")):
                lc = (255, 220, 60)   # gold
            elif "Reduce" in line:
                lc = (100, 255, 120)  # eco green
            else:
                lc = (230, 245, 255)  # soft white

            ls = win_font.render(line, True, lc)
            ls.set_alpha(fade_alpha)
            self.screen.blit(ls, (sw // 2 - ls.get_width() // 2, line_y))
            line_y += line_gap

        # ── 6. "Press ENTER to Exit" prompt ───────────────────────
        pulse_e     = 0.7 + 0.3 * math.sin(t * 3.2)
        # exit_font   = pygame.font.SysFont("Arial Rounded MT Bold", 32, bold=True)
        exit_font = self.assets.fonts["exit"]
        exit_surf   = exit_font.render("Press ENTER to Exit",
                                        True, (int(200 * pulse_e), 255, int(200 * pulse_e)))
        self.screen.blit(exit_surf, (sw // 2 - exit_surf.get_width() // 2, int(sh * 0.92)))

    # ─────────────────────────────────────────
    #  BACKGROUND
    # ─────────────────────────────────────────

    def _draw_background(self):
        if hasattr(self, 'current_bg') and self.current_bg is not None:
            self.screen.blit(self.current_bg, (0, 0))
        else:
            if self.settings.clean_mode:
                self.screen.fill((100, 200, 100))
            else:
                self.screen.fill((60, 60, 60))

    # ─────────────────────────────────────────
    #  ENVIRONMENT MODE TRANSITION
    # ─────────────────────────────────────────

    def _check_clean_mode_trigger(self):
        if (
            not self.clean_mode_triggered
            and self.eco_actions >= self.settings.clean_mode_eco_threshold
        ):
            self.clean_mode_triggered = True
            self.settings.clean_mode  = True
            print("[Environment] Clean Environment Unlocked!")
            self.current_bg       = self.clean_bg
            self.clean_msg_timer  = self.CLEAN_MSG_DURATION

    def _draw_clean_mode_message(self):
        if self.clean_msg_timer <= 0:
            return

        screen_cx = self.settings.screen_width  // 2
        screen_cy = self.settings.screen_height // 2

        start_timer = getattr(self, "clean_msg_start_timer", self.clean_msg_timer)
        progress    = self.clean_msg_timer / max(start_timer, 1)
        alpha       = int(255 * (progress / 0.30)) if progress < 0.30 else 255

        t = self.clean_msg_timer * 0.10

        r = int(100 + 80 * math.sin(t * 0.7))
        g = int(220 + 35 * math.sin(t * 0.7 + 1.0))
        b = int(80  + 40 * math.sin(t * 0.5))
        COLOR_TEXT = (min(255, r), min(255, g), min(255, b))

        shimmer_phase = (self.clean_msg_timer * 0.07) % (2 * math.pi)
        shimmer_boost = int(max(0, math.sin(shimmer_phase)) * 90)
        COLOR_SHIMMER = (
            min(255, 200 + shimmer_boost),
            255,
            min(255, 100 + shimmer_boost)
        )
        COLOR_OUTLINE = (10, 40, 10)
        COLOR_SHADOW  = (20, 70, 20)

        # font    = pygame.font.SysFont("Courier New", 54, bold=True)

        unlock_font = self.assets.fonts["unlock"]
        message = "CLEAN ENVIRONMENT UNLOCKED!"

        outline_size  = 3
        base_text     = unlock_font.render(message, False, COLOR_TEXT)
        shimmer_text  = unlock_font.render(message, False, COLOR_SHIMMER)
        shadow_text   = unlock_font.render(message, False, COLOR_SHADOW)
        outline_text  = unlock_font.render(message, False, COLOR_OUTLINE)

        w = base_text.get_width()  + outline_size * 2 + 4
        h = base_text.get_height() + outline_size * 2 + 4
        text_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        ox, oy = outline_size, outline_size

        for dx in range(-outline_size, outline_size + 1):
            for dy in range(-outline_size, outline_size + 1):
                if dx == 0 and dy == 0:
                    continue
                text_surf.blit(outline_text, (ox + dx, oy + dy))

        text_surf.blit(shadow_text, (ox + outline_size + 2, oy + outline_size + 2))
        text_surf.blit(base_text, (ox, oy))

        shimmer_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        shimmer_surf.blit(shimmer_text, (ox, oy))
        band_x     = int((math.sin(shimmer_phase) * 0.5 + 0.5) * w)
        band_width = w // 4
        band_rect  = pygame.Rect(band_x - band_width // 2, 0, band_width, h)
        mask = pygame.Surface((w, h), pygame.SRCALPHA)
        mask.fill((0, 0, 0, 0))
        pygame.draw.rect(mask, (255, 255, 255, 180), band_rect)
        shimmer_surf.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        text_surf.blit(shimmer_surf, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        msg_x = screen_cx - text_surf.get_width()  // 2
        msg_y = screen_cy - text_surf.get_height() // 2

        glow_pulse  = 1.0 + 0.12 * math.sin(t * 1.2)
        glow_layers = [
            (int(55 * glow_pulse), (20, 120, 20, 18)),
            (int(35 * glow_pulse), (40, 180, 40, 30)),
            (int(18 * glow_pulse), (100, 255, 100, 50)),
        ]
        for radius_extra, (gr, gg, gb, ga) in glow_layers:
            glow_w    = text_surf.get_width()  + radius_extra * 2
            glow_h    = text_surf.get_height() + radius_extra * 2
            glow_surf = pygame.Surface((glow_w, glow_h), pygame.SRCALPHA)
            for step in range(radius_extra, 0, -4):
                fade        = int(ga * (step / radius_extra))
                ellipse_rect = pygame.Rect(
                    radius_extra - step, radius_extra - step,
                    text_surf.get_width() + step * 2,
                    text_surf.get_height() + step * 2
                )
                pygame.draw.ellipse(glow_surf, (gr, gg, gb, fade), ellipse_rect)
            glow_surf.set_alpha(alpha)
            self.screen.blit(glow_surf, (msg_x - radius_extra, msg_y - radius_extra))

        random.seed(42)
        num_sparks  = 10
        spark_color = (120, 255, 120)
        for i in range(num_sparks):
            sx      = msg_x + random.randint(-40, text_surf.get_width() + 40)
            sy      = msg_y + random.randint(-30, text_surf.get_height() + 30)
            twinkle = math.sin(t * 1.5 + i * 1.1)
            if twinkle > 0.3:
                size       = int(2 + twinkle * 3)
                s_alpha    = int(alpha * twinkle)
                spark_surf = pygame.Surface((size * 4, size * 4), pygame.SRCALPHA)
                cx2, cy2   = size * 2, size * 2
                pygame.draw.line(spark_surf, (*spark_color, s_alpha),
                                 (cx2 - size * 2, cy2), (cx2 + size * 2, cy2), max(1, size // 2))
                pygame.draw.line(spark_surf, (*spark_color, s_alpha),
                                 (cx2, cy2 - size * 2), (cx2, cy2 + size * 2), max(1, size // 2))
                self.screen.blit(spark_surf, (sx - size * 2, sy - size * 2))

        text_surf.set_alpha(alpha)
        self.screen.blit(text_surf, (msg_x, msg_y))
        self.clean_msg_timer -= 1

    # ─────────────────────────────────────────
    #  MUSIC
    # ─────────────────────────────────────────

    def _play_music(self, mode, fade_ms=1500):
        if mode == self.current_music_mode:
            return
        track = (
            self.polluted_music_path if mode == "polluted"
            else self.clean_music_path
        )
        pygame.mixer.music.load(track)
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-1)
        self.current_music_mode = mode
        print(f"[Music] Switched to {mode.upper()} environment track.")

    def _update_music_for_mode(self):
        if not self.stats.game_active:
            return
        desired_mode = "clean" if self.settings.clean_mode else "polluted"
        if desired_mode != self.current_music_mode:
            self._play_music(desired_mode)

    def _pause_music(self):
        pygame.mixer.music.pause()

    def _resume_music(self):
        pygame.mixer.music.unpause()

    def _set_music_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

    # ─────────────────────────────────────────
    #  EVENTS
    # ─────────────────────────────────────────

    def _check_events(self):
        """Process pygame events — dispatch by game state."""
        for event in pygame.event.get():
            # Intro screen — any tap starts the game
            if self.game_state == "intro":
                if event.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
                    self._start_game()
                    continue
                if event.type == pygame.KEYDOWN and event.key in (
                        pygame.K_RETURN, pygame.K_SPACE
                ):
                    self._start_game()
                    continue

            # Active quiz — answer tap or key
            if getattr(self, "quiz_active", False):
                if event.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
                    self._check_quiz_click(event)
                    continue
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_a, pygame.K_b, pygame.K_c):
                    self._check_quiz_keydown(event)
                    continue

            # Game-over screen — restart button click/tap
            if self.game_state == "gameover":
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_r):
                    self._start_game()
                    continue
                if event.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
                    # Map touch to (x,y) and route through _check_play_button
                    pos = getattr(event, "pos", None)
                    if pos is None:
                        w, h = self.screen.get_size()
                        pos = (int(event.x * w), int(event.y * h))
                    self._check_play_button(pos)
                    continue

            # Standard keyboard / mouse flow during play
            if event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_play_button(event.pos)

    def _start_game(self):
        """Transition from intro to gameplay."""
        print("[Game] Starting game from intro screen...")
        self.game_state = "playing"
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_planet_health()
        self.sb.prep_lives()
        self.stats.game_active = True
        self.items.empty()
        self.kid.center_kid()
        self.items_caught        = 0
        self.eco_actions         = 0
        self.clean_mode_triggered = False
        self.settings.clean_mode = False
        self.current_bg          = self.polluted_bg
        self.game_start_time     = time.time()
        self.time_up             = False
        pygame.mouse.set_visible(False)

    def _check_play_button(self, mouse_pos):
        """Click handler that knows about all in-game buttons."""
        if self.stats.game_active:
            return  # only handle clicks when no game is in progress

        # Restart button on game-over screen?
        if hasattr(self, "restart_button") and self.restart_button.rect.collidepoint(mouse_pos):
            self._start_game()
            return

        # Default play button (intro / first launch)
        if hasattr(self, "play_button") and self.play_button.rect.collidepoint(mouse_pos):
            self._start_game()
            return

    def _check_keydown_events(self, event):
        # From intro screen: Enter or Space starts the game
        if self.game_state == "intro":
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._start_game()
                return

        if event.key == pygame.K_RIGHT:
            self.kid.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.kid.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.kid.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.kid.moving_left = False

    # ─────────────────────────────────────────
    #  QUIZ HANDLING
    # ─────────────────────────────────────────

    def _trigger_quiz(self):
        self.quiz_active = True
        self.quiz_result = None
        if self.settings.clean_mode:
            self.current_quiz = random.choice(ECO_QUIZZES)
        else:
            self.current_quiz = random.choice(ECO_QUIZZES + MATH_QUIZZES)
        if hasattr(self, 'quiz_sound'):
            self.quiz_sound.play()
        pygame.mouse.set_visible(True)

    def _check_quiz_click(self, event_or_pos):
        """Single source of truth for tap-or-click on quiz answers."""
        # Accept either an event with .pos or .x/.y or a tuple
        if hasattr(event_or_pos, "pos") and event_or_pos.pos:
            pos = event_or_pos.pos
        elif hasattr(event_or_pos, "x"):
            # FINGERDOWN event — x and y are normalised 0–1
            w, h = self.screen.get_size()
            pos = (int(event_or_pos.x * w), int(event_or_pos.y * h))
        elif isinstance(event_or_pos, tuple):
            pos = event_or_pos
        else:
            return  # unknown event, ignore

        if self.quiz_result is not None:
            self._dismiss_quiz()
            return

        for i, rect in enumerate(self._quiz_option_rects):
            if rect.collidepoint(pos):
                self._evaluate_quiz(i)
                return

    def _check_quiz_keydown(self, event):
        if self.quiz_result is not None:
            self._dismiss_quiz()
            return
        key_map = {pygame.K_a: 0, pygame.K_b: 1, pygame.K_c: 2}
        if event.key in key_map:
            self._evaluate_quiz(key_map[event.key])

    def _evaluate_quiz(self, chosen_index):
        correct = self.current_quiz["answer"]
        if chosen_index == correct:
            self.quiz_result = "correct"
            self.stats.update_score(6)
            self.eco_actions += 1
        else:
            self.quiz_result = "wrong"
        self.sb.prep_score()

    def _dismiss_quiz(self):
        self.quiz_active  = False
        self.current_quiz = None
        self.quiz_result  = None
        pygame.mouse.set_visible(False)

    # ─────────────────────────────────────────
    #  GAME LOGIC
    # ─────────────────────────────────────────

    def _handle_good_catch(self, item):
        self.stats.update_score(self.settings.good_points)
        self.stats.increment_eco_actions()
        self.sb.prep_eco_actions()
        self.good_sound.play()

    def _handle_bad_catch(self, item):
        self.stats.update_score(self.settings.bad_points)
        self.stats.planet_health = max(0, self.stats.planet_health - 2)
        self.sb.prep_planet_health()
        self.bad_sound.play()
        if self.stats.planet_health <= 0:
            self.stats.game_active = False

    def _update_items(self):
        if random.randint(1, 50) == 1:
            item_type = "good" if random.random() < 0.6 else "bad"
            self.items.add(FallingItem(self, item_type))
        self.items.update()

        collisions = pygame.sprite.spritecollide(self.kid, self.items, True)
        for item in collisions:
            self.items_caught += 1
            if item.item_type == "good":
                self._handle_good_catch(item)
                self.kid.trigger_catch()
            else:
                self._handle_bad_catch(item)
                self.kid.trigger_hit()
            if self.items_caught % self.QUIZ_INTERVAL == 0:
                self._trigger_quiz()
                break

        self.sb.prep_score()
        self.sb.prep_planet_health()
        self.sb.prep_lives()
        self.check_planet_health()

        for item in self.items.copy():
            if item.off_screen():
                self.items.remove(item)

        if not self.stats.game_active:
            pygame.mouse.set_visible(True)
            return

    def _tick_timers(self):
        if self.fact_timer > 0:
            self.fact_timer -= 1

    # ─────────────────────────────────────────
    #  WIN CONDITION
    # ─────────────────────────────────────────

    def check_planet_health(self):
        if self.stats.planet_health >= 100:
            self.game_won = True
            self.stats.planet_health = 100

    # ─────────────────────────────────────────
    #  SCREEN UPDATE  (playing / gameover)
    # ─────────────────────────────────────────

    def _update_screen(self):
        self._draw_background()

        if self.stats.game_active:
            self.kid.blitme()
            for item in self.items.sprites():
                item.draw()

        self.sb.show_score()

        if self.game_start_time is not None:
            self._draw_timer_hud()

        if self.fact_timer > 0:
            self._draw_fact_banner(self.fact_message, y_offset=120)

        self._draw_clean_mode_message()

        if self.quiz_active:
            self._draw_quiz_panel()

        if not self.stats.game_active:
            self.play_button.draw_button()

        if self.congratulation_timer > 0:
            self.congratulation_timer -= 1
            self._draw_celebration_message("Planet Health Restored to 100!")
        else:
            self.congratulation_timer = 0

    def _draw_fact_banner(self, message, y_offset=120):
        if not message:
            return
        padding = 16
        surf    = self.font_small.render(message, True, (255, 255, 230))
        w       = surf.get_width() + padding * 2
        h       = surf.get_height() + padding
        x       = (self.settings.screen_width - w) // 2
        banner  = pygame.Surface((w, h), pygame.SRCALPHA)
        banner.fill((0, 80, 0, 200))
        self.screen.blit(banner, (x, y_offset))
        self.screen.blit(surf, (x + padding, y_offset + padding // 2))

    def _draw_timer_hud(self):
        if self.game_start_time is None:
            return
        elapsed   = time.time() - self.game_start_time
        remaining = max(0, self.GAME_DURATION - elapsed)
        minutes   = int(remaining) // 60
        seconds   = int(remaining) % 60

        if remaining > 60:
            color = (100, 255, 100)
        elif remaining > 30:
            color = (255, 200, 50)
        else:
            color = (255, 60, 60)

        if self.time_up:
            label = "TIME UP!"
            color = (255, 60, 60)
        else:
            label = f"Time: {minutes:01d}:{seconds:02d}"

        timer_surf  = self.font_large.render(label, True, color)
        x           = (self.settings.screen_width - timer_surf.get_width()) // 2
        y           = 16
        shadow_surf = self.font_large.render(label, True, (0, 0, 0))
        self.screen.blit(shadow_surf, (x + 2, y + 2))
        self.screen.blit(timer_surf,  (x, y))

    def _draw_quiz_panel(self):
        sw, sh = self.settings.screen_width, self.settings.screen_height
        pw, ph = 700, 420
        px, py = (sw - pw) // 2, (sh - ph) // 2

        panel = pygame.Surface((pw, ph), pygame.SRCALPHA)
        panel.fill((10, 40, 10, 230))
        pygame.draw.rect(panel, (80, 200, 80), (0, 0, pw, ph), 4, border_radius=16)
        self.screen.blit(panel, (px, py))

        self._render_text("ECO QUIZ TIME!", self.font_large, (100, 255, 100), (px + 20, py + 16))
        self._render_text(
            self.current_quiz["question"],
            self.font_medium, (255, 255, 200),
            (px + 20, py + 72)
        )

        if self.quiz_result is None:
            self._quiz_option_rects = []
            for i, option in enumerate(self.current_quiz["options"]):
                oy   = py + 140 + i * 70
                rect = pygame.Rect(px + 40, oy, pw - 80, 52)
                pygame.draw.rect(self.screen, (20, 100, 20), rect, border_radius=10)
                pygame.draw.rect(self.screen, (80, 200, 80), rect, 2, border_radius=10)
                self._render_text(option, self.font_medium, (255, 255, 255),
                                  (rect.x + 16, rect.y + 12))
                self._quiz_option_rects.append(rect)
            self._render_text(
                "Press A / B / C  or  click an option",
                self.font_small, (150, 150, 150),
                (px + 20, py + ph - 36)
            )
        else:
            if self.quiz_result == "correct":
                self._render_text("Correct! +6 bonus points!", self.font_large,
                                  (80, 255, 80), (px + 40, py + 160))
            else:
                self._render_text("Not quite!", self.font_large,
                                  (255, 80, 80), (px + 40, py + 160))
            self._render_text(
                self.current_quiz["hint"],
                self.font_small, (255, 230, 100),
                (px + 40, py + 230)
            )
            self._render_text(
                "Click or press any key to continue",
                self.font_small, (200, 200, 200),
                (px + 40, py + ph - 50)
            )

    def _draw_celebration_message(self, message, text_color=(128, 0, 128)):
        font           = pygame.font.SysFont("Courier New", 60, bold=True)
        elapsed_time   = pygame.time.get_ticks() / 1000.0
        scale_factor   = min(elapsed_time / 1.0, 1.0)
        scale_factor   = 1 - (1 - scale_factor) ** 3
        shimmer_offset = math.sin(pygame.time.get_ticks() * 0.005) * 5

        text_surface   = font.render(message, True, text_color)
        glow_surface   = font.render(message, True, (255, 255, 224))
        scaled_width   = max(1, int(text_surface.get_width()  * scale_factor))
        scaled_height  = max(1, int(text_surface.get_height() * scale_factor))
        scaled_text    = pygame.transform.smoothscale(text_surface, (scaled_width, scaled_height))
        scaled_glow    = pygame.transform.smoothscale(glow_surface, (scaled_width, scaled_height))
        center_x       = self.settings.screen_width  // 2
        center_y       = self.settings.screen_height // 2
        scaled_text_rect = scaled_text.get_rect(center=(center_x, center_y + shimmer_offset))
        scaled_glow_rect = scaled_glow.get_rect(center=(center_x, center_y + shimmer_offset))
        glow_radius = 3
        for dx in range(-glow_radius, glow_radius + 1):
            for dy in range(-glow_radius, glow_radius + 1):
                if dx ** 2 + dy ** 2 <= glow_radius ** 2:
                    self.screen.blit(scaled_glow,
                                     (scaled_glow_rect.x + dx, scaled_glow_rect.y + dy))
        self.screen.blit(scaled_text, scaled_text_rect)

    def _render_text(self, text, font, color, pos):
        surf = font.render(text, True, color)
        self.screen.blit(surf, pos)

    # ─────────────────────────────────────────
    #  RESET
    # ─────────────────────────────────────────

    def _reset_game(self):
        self.eco_actions          = 0
        self.clean_mode_triggered = False
        self.clean_msg_timer      = 0
        self.settings.clean_mode  = False
        self.settings.initialize_dynamic_settings()
        self.current_bg           = self.polluted_bg




if __name__ == '__main__':
    game = SuperKidsGame()
    asyncio.run(game.run_game())
