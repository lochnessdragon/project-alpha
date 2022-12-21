import random

import pygame
from pygame.locals import *
from pygame._sdl2.video import Renderer, Texture
from enum import Enum

CLEAR_COLOR = Color(10, 10, 20, 255)
SKY_COLOR = Color(237, 173, 78, 255)

# used for fonts
WHITE = (255, 255, 255)

class IntroState(Enum):
    SHOW_AUDIO_ICON = 1
    SPACE = 2
    SPACE_WITH_TEXT = 3
    FAR_ANGLE = 4
    FAR_ANGLE_WITH_TEXT = 5
    CRASH_SCENE = 6

class IntroCutscene:
    def __init__(self, assets_dir: str, renderer: Renderer, debug_font: pygame.font.Font, main_font_filename: str, screen_size: (int, int)):
        self.sunrise_audio = pygame.mixer.Sound(assets_dir + "/audio/sunrise.ogg")
        self.timer = 0
        self.sunrise_playing = False
        self.renderer = renderer
        self.state = IntroState.SHOW_AUDIO_ICON
        self.main_font_filename = main_font_filename
        self.window_rect = Rect(0, 0, screen_size[0], screen_size[1])

        # generate stars
        self.stars = []
        for x in range(0, 100):
            self.stars.append((random.randrange(0, screen_size[0]), random.randrange(0, screen_size[1])))

        # fonts
        self.debug_font = debug_font
        self.heading3_font = pygame.font.Font(self.main_font_filename, 24)
        self.big_text_font = pygame.font.SysFont("Arial", 164, bold=True)

        # textures
        self.capsule_texture = Texture.from_surface(renderer, pygame.image.load(assets_dir + "/img/bg/falling_capsule.png"))
        self.capsule_rect = self.capsule_texture.get_rect()
        self.capsule_rect.width *= 3
        self.capsule_rect.height *= 3
        self.capsule_rect.centerx = screen_size[0] // 2
        self.capsule_rect.centery = screen_size[1] // 2
        self.capsule_direction = 1
        self.capsule_speed = 2

        self.planet_far_angle = Texture.from_surface(renderer, pygame.image.load(assets_dir + "/img/bg/planet_far_angle.png"))
        self.planet_far_angle_rect = self.planet_far_angle.get_rect()
        self.planet_far_angle_rect.width *= 2
        self.planet_far_angle_rect.height *= 2
        self.planet_far_angle_rect.centerx = screen_size[0] // 2
        self.planet_far_angle_rect.centery = screen_size[1] // 2

        self.space_text = Texture.from_surface(renderer, self.big_text_font.render("SPACE", True, WHITE))
        self.space_text_rect = self.space_text.get_rect()
        self.space_text_rect.centerx = screen_size[0] // 2
        self.space_text_rect.centery = screen_size[1] // 2

        self.more_text = Texture.from_surface(renderer, self.big_text_font.render("MORE", True, WHITE))
        self.more_text_rect = self.more_text.get_rect()
        self.more_text_rect.centerx = screen_size[0] // 2
        self.more_text_rect.centery = screen_size[1] // 2

        self.enable_audio_icon = Texture.from_surface(renderer, pygame.image.load(assets_dir + "/img/ui/enable_audio_icon.png"))
        self.audio_icon_rect = self.enable_audio_icon.get_rect()
        self.audio_icon_rect.width *= 3
        self.audio_icon_rect.height *= 3
        self.audio_icon_rect.centerx = screen_size[0] // 2
        self.audio_icon_rect.centery = screen_size[1] // 2

        self.enable_audio_text_line0 = Texture.from_surface(renderer, self.heading3_font.render("Turn your audio on for", False, WHITE))
        self.enable_audio_text_line1 = Texture.from_surface(renderer, self.heading3_font.render("the full experience!", False, WHITE))
        self.enable_audio_text_line0_rect = self.enable_audio_text_line0.get_rect()
        self.enable_audio_text_line1_rect = self.enable_audio_text_line1.get_rect()
        self.enable_audio_text_line0_rect.centerx = screen_size[0] // 2
        self.enable_audio_text_line0_rect.centery = screen_size[1] // 2 + self.enable_audio_icon.height + self.enable_audio_text_line0_rect.height
        self.enable_audio_text_line1_rect.centerx = screen_size[0] // 2
        self.enable_audio_text_line1_rect.centery = screen_size[1] // 2 + self.enable_audio_icon.height + self.enable_audio_text_line0_rect.height + self.enable_audio_text_line1_rect.height

    def update(self, deltaTime: float) -> bool:
        """
        Animation for the intro cutscene
        """
        self.previousTimer = self.timer
        self.timer += deltaTime

        if not self.sunrise_playing:
            self.sunrise_audio.play()
            self.sunrise_playing = True

        if self.state == IntroState.SHOW_AUDIO_ICON:
            if self.timer > 1000: # show audio icon at full strength for 1 second
                if self.enable_audio_icon.alpha > 0:
                    self.enable_audio_icon.alpha = max(255 - int(((self.timer - 1000) / 1000) * 255), 0) # disappear for 1 second
                    self.enable_audio_text_line0.alpha = self.enable_audio_icon.alpha
                    self.enable_audio_text_line1.alpha = self.enable_audio_icon.alpha
                else:
                    self.state = IntroState.SPACE

        if self.timer > 20000 and self.previousTimer < 20000:
            self.state = IntroState.SPACE_WITH_TEXT

        if self.timer > 30000 and self.previousTimer < 30000:
            self.state = IntroState.SPACE

        if self.timer > 38000 and self.previousTimer < 38000:
            self.state = IntroState.FAR_ANGLE

        if self.timer > 44000 and self.previousTimer < 44000:
            self.state = IntroState.FAR_ANGLE_WITH_TEXT
            self.space_text_rect.centery += self.space_text_rect.height // 2
            self.more_text_rect.centery -= self.more_text_rect.height // 2

        if self.timer > 55000 and self.previousTimer < 55000:
            self.state = IntroState.CRASH_SCENE

        if self.timer > 55100:
            # animate capsule
            self.capsule_rect.centery += self.capsule_direction * self.capsule_speed * (deltaTime / 10)
            if self.capsule_rect.centery > self.window_rect.height:
                self.capsule_direction = -1
            elif self.capsule_rect.centery < 0:
                self.capsule_direction = 1

        # return true if the animation is done
        if self.timer > 81000:
            # reset animation
            self.sunrise_audio.stop()
            self.timer = 0
            self.sunrise_playing = False
            return True

        return False

    def render(self):
        """
        Renders the Intro cutscene
        """

        # always draw the starfield
        self.renderer.draw_color = Color(255, 255, 255, 255)
        for star in self.stars:
            self.renderer.draw_point(star)

        # show debug information in the top right
        #debug_text = Texture.from_surface(self.renderer, self.debug_font.render("Time: " + str(self.timer), False, WHITE))
        #debug_text.draw(dstrect=debug_text.get_rect())

        # different drawing based on state
        if self.state == IntroState.SHOW_AUDIO_ICON:
            self.enable_audio_icon.draw(dstrect=self.audio_icon_rect)
            self.enable_audio_text_line0.draw(dstrect=self.enable_audio_text_line0_rect)
            self.enable_audio_text_line1.draw(dstrect=self.enable_audio_text_line1_rect)
        elif self.state == IntroState.SPACE:
            # no drawings, just space
            pass
        elif self.state == IntroState.SPACE_WITH_TEXT:
            # draw space text
            self.space_text.draw(dstrect=self.space_text_rect)
        elif self.state == IntroState.FAR_ANGLE:
            # draw planet
            self.planet_far_angle.draw(dstrect=self.planet_far_angle_rect)
        elif self.state == IntroState.FAR_ANGLE_WITH_TEXT:
            # draw MORE, then planet, then SPACE (order intentional)
            self.more_text.draw(dstrect=self.more_text_rect)
            self.planet_far_angle.draw(dstrect=self.planet_far_angle_rect)
            self.space_text.draw(dstrect=self.space_text_rect)
        elif self.state == IntroState.CRASH_SCENE:
            # draw sky
            self.renderer.draw_color = SKY_COLOR
            self.renderer.fill_rect(self.window_rect)

            # draw capsule
            self.capsule_texture.draw(dstrect=self.capsule_rect)
