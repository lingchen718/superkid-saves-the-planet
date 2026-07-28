import pygame.font

class Button:
    """为 Super Kids 游戏创建按钮的类"""

    def __init__(self, game, msg, center_x=None, center_y=None, width=200, height=60):
        """初始化按钮的属性"""
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        # 设置按钮尺寸和颜色
        self.width = width
        self.height = height
        self.button_color = (0, 200, 0)  # 绿色，更生动
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48, bold=True)

        # 创建按钮的 rect 对象
        self.rect = pygame.Rect(0, 0, self.width, self.height)

        # 居中，或使用自定义位置
        if center_x is None or center_y is None:
            self.rect.center = self.screen_rect.center
        else:
            self.rect.centerx = center_x
            self.rect.centery = center_y

        # 创建按钮标签
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """将 msg 渲染为图像，并在按钮上居中"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """绘制按钮和文本"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)