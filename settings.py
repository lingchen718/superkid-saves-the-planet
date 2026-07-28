

class SuperKidsSettings:
    """存储《Super Kids Saves the Planet》游戏的所有设置"""
    def __init__(self):
        # Android / Desktop 通用
        self.fullscreen = True

        # 音量
        self.music_volume = 0.6

        self.sound_volume = 0.8

        # 是否开启震动（以后手机可用）
        self.enable_vibration = False

        """初始化游戏的静态设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 900
        self.bg_color = (20, 20, 40)
        # 帧率设置
        self.fps = 60  # Set the desired frames per second
        # 玩家设置

        self.kid_speed = 20
        self.starting_lives = 8
        self.starting_health = 10

        # 增加难度
        self.speedup_scale = 1.4

        # 收集物品设置，好的加分，污染的减分
        self.item_width = 40
        self.item_height = 40
        self.items_allowed = 20  # 同屏最多几个物品


        # 分数设置
        self.good_points = 1
        self.bad_points = -1

        # --- Game Mode Settings ---
        self.game_mode = "polluted"              # 默认从白天模式开始
        self.clean_mode = False  # Default to pollute mode

        self.polluted_item_fall_speed = 9       # polluted模式下的下落速度
        self.clean_item_fall_speed = 10     # clean模式下的下落速度（更快）

        # --- Night Mode Trigger ---
        self.clean_mode_eco_threshold = 6   # 达到5个eco actions后切换到夜间模式

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.kid_speed = 20
        self.falling_speed = self.polluted_item_fall_speed  # 开始时使用白天速度
        self.items_allowed = 28
        self.fleet_direction = -1
        self.game_mode = "polluted"  # 每次重新开始时重置为白天模式

    def apply_game_mode(self, mode):
        """根据选择的游戏模式应用设置"""
        self.game_mode = mode
        if mode == "clean":
            self.falling_speed = self.clean_item_fall_speed
            print("Switched to Clean Mode")  # Debug statement

        else:
            self.falling_speed = self.polluted_item_fall_speed
            print("Switched to Polluted Mode")  # Debug statement

    # def increase_speed(self):
       # """提高游戏难度"""
       # self.kid_speed *= self.speedup_scale
       # self.falling_speed *= self.speedup_scale
       # self.good_points = int(self.good_points)
       # self.bad_points = int(self.bad_points)
       # print(f"New points: {self.good_points}, {self.bad_points}")

    def toggle_clean_mode(self):
        """Toggle between day and night mode."""
        self.clean_mode = not self.clean_mode