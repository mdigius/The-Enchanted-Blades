import pygame
import pygame as pg
import sys
import map
from player import *
from settings import *
from sounds import Sounds
from button import Button
from dialogue import Dialogue
from boss import Boss


class Game:

    def __init__(self):
        pg.display.init()
        pg.init()

        self.BG = pg.image.load("imgs/blank.png")
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.new_game()
        self.sounds = Sounds()
        self.dialogue = Dialogue()

        self.player = Player((900, 500))
        self.main_map = map.Map('tmx/CastleMap.tmx',
                                self.player, (1194, 666), False, False, False)
        self.main_map.update_player_info()
        self.main_map.set_active(True)
        self.current_map = self.main_map
        self.break_period = 0
        self.dungeon_map = map.Map(
            'tmx/Dungeon.tmx', self.player, (1000, 500), False, True, False)

        self.merchant_map = map.Map(
            'tmx/Merchant.tmx', self.player, (155, 275), True, False, False)
        self.boss_map = map.Map(
            'tmx/BossMap.tmx', self.player, (155, 275), False, False, True)

        self.main_menu()

    def death_screen(self):
        while self.player.health <= 0:
            self.sounds.stop_audio()
            self.screen.fill('black')
            self.screen.blit(self.BG, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            RESPAWN_TEXT = self.get_font(50).render(
                "You are dead", True, "#b68f40")
            RESPAWN_RECT = RESPAWN_TEXT.get_rect(
                center=(self.screen.get_rect().centerx, 100))
            RESPAWN_BUTTON = Button(image=pygame.image.load("imgs/Options Rect.png"), pos=(self.screen.get_rect().centerx, 250),
                                    text_input="RESPAWN", font=self.get_font(30), base_color="#d7fcd4", hovering_color="White")

            self.screen.blit(RESPAWN_TEXT, RESPAWN_RECT)

            RESPAWN_BUTTON.changeColor(MENU_MOUSE_POS)
            RESPAWN_BUTTON.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if RESPAWN_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.player.health = self.player.stats['health']
                        self.player.exp /= 2
                        self.player.current_room = 5
                        self.run()

            pygame.display.update()

    def game_end_screen(self):
        if self.boss_map.boss.check_boss_death():
            self.dialogue.clear_dialogue()
            current_Time = pg.time.get_ticks()
            if current_Time > 10000:
                self.sounds.stop_audio()
                self.screen.fill('black')
                self.screen.blit(self.BG, (0, 0))

                MENU_MOUSE_POS = pygame.mouse.get_pos()

                WIN_TEXT = self.get_font(50).render(
                    "Conguatulation, you defeated the boss!", True, "#b68f40")
                WIN_RECT = WIN_TEXT.get_rect(
                    center=(self.screen.get_rect().centerx, 100))
                MENU_BUTTON = Button(image=pygame.image.load("imgs/Options Rect.png"), pos=(self.screen.get_rect().centerx, 250),
                                     text_input="Quit", font=self.get_font(30), base_color="#d7fcd4", hovering_color="White")

                self.screen.blit(WIN_TEXT, WIN_RECT)

                MENU_BUTTON.changeColor(MENU_MOUSE_POS)
                MENU_BUTTON.update(self.screen)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if MENU_BUTTON.checkForInput(MENU_MOUSE_POS):
                            pygame.quit()
                            sys.exit()

                pygame.display.update()

    def load_intro(self, screen):
        self.sounds.play_audio(self.sounds.intro_music, -1)
        pg.display.set_caption("The Enchanted Blades")
        # TODO:upload a real intro image
        intro_img = pg.image.load("imgs/blank.png")
        intro_rect = intro_img.get_rect()

        pg.font.init()
        font = pg.font.Font('imgs/BreatheFireIii-PKLOB.ttf', 24)

        text1 = font.render("Press E to start", False, (255, 255, 255))
        text1_rect = text1.get_rect()
        text1_rect.centerx = screen.get_rect().centerx
        text1_rect.centery = screen.get_rect().centery - screen.get_rect().height // 3

        text2 = font.render("W A S D To Control", False, (255, 255, 255))
        text2_rect = text2.get_rect()
        text2_rect.centerx = screen.get_rect().centerx
        text2_rect.centery = screen.get_rect().centery + screen.get_rect().height // 3

        text3 = font.render("Press Q to quit", False, (255, 255, 255))
        text3_rect = text3.get_rect()
        text3_rect.centerx = screen.get_rect().centerx
        text3_rect.centery = screen.get_rect().centery

        screen.blit(intro_img, intro_rect)
        screen.blit(text1, text1_rect)
        screen.blit(text2, text2_rect)
        screen.blit(text3, text3_rect)
        pg.display.flip()

    def new_game(self):
        pass

    def update(self):
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        self.setMap()
        pg.display.set_caption(f'{self.clock.get_fps() : .1f}')

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.current_map.run()

    def setMap(self):
        # in main entering merchant
        if self.current_map.player.current_room == 1:
            self.main_map.set_active(False)
            self.merchant_map.set_active(True)
            self.current_map = self.merchant_map
            self.current_map.update_player_info()
            self.current_map.player.current_room = -1
            self.sounds.stop_audio()
            self.sounds.play_audio(self.sounds.door, 0)
            self.sounds.play_audio(self.sounds.shop_music, -1)
            self.dialogue.clear_dialogue()
            self.dialogue.merchant_message()
        # in merchant entering the main area
        elif self.current_map.player.current_room == 2:
            self.main_map.set_active(True)
            self.merchant_map.set_active(False)
            self.current_map = self.main_map
            self.current_map.update_player_info((946, 685))
            self.current_map.player.current_room = -1
            self.sounds.stop_audio()
            self.sounds.play_audio(self.sounds.door, 0)
            self.sounds.play_audio(self.sounds.base_music, -1)
            self.dialogue.clear_dialogue()
        # in main entering the dungeon
        elif self.current_map.player.current_room == 3:
            self.main_map.set_active(False)
            self.dungeon_map.set_active(True)
            self.current_map = self.dungeon_map
            self.current_map.update_player_info()
            self.current_map.player.current_room = -1
            self.sounds.stop_audio()
            self.sounds.play_audio(self.sounds.door, 0)
            self.sounds.play_audio(self.sounds.fight_music, -1)
            self.dialogue.clear_dialogue()
            self.dungeon_map.wave_number = 0
        # in dungeon entering the main area
        elif self.current_map.player.current_room == 4:
            self.main_map.set_active(True)
            self.dungeon_map.set_active(False)
            self.current_map = self.main_map
            self.current_map.update_player_info((1554, 668))
            self.current_map.player.current_room = -1
            self.sounds.stop_audio()
            self.sounds.play_audio(self.sounds.door, 0)
            self.sounds.play_audio(self.sounds.base_music, -1)
            self.dungeon_map.timer.reset_timer()
            self.dungeon_map.store_highest_waves()
            self.dungeon_map.reset_enemy()
            self.dialogue.clear_dialogue()
        # respawning in the main area
        elif self.current_map.player.current_room == 5:
            self.main_map.set_active(True)
            self.dungeon_map.set_active(False)
            self.current_map = self.main_map
            self.current_map.update_player_info((1194, 666))
            self.current_map.player.current_room = -1
            self.dungeon_map.reset_enemy()
            self.dungeon_map.timer.reset_timer()
            self.sounds.play_audio(self.sounds.base_music, -1)
            self.dungeon_map.store_highest_waves()
            self.dialogue.clear_dialogue()
        # entering the boss room
        elif self.current_map.player.current_room == 6 and self.player.highest_wave >= 5:
            self.main_map.set_active(False)
            self.boss_map.set_active(True)
            self.current_map = self.boss_map
            self.current_map.update_player_info((232, 350))
            self.current_map.player.current_room = -1
            self.sounds.stop_audio()
            self.sounds.play_audio(self.sounds.fight_music, -1)
            self.boss_map.boss.isIntro = True
            self.player.bossIntro = True
            self.dialogue.clear_dialogue()
            self.dialogue.boss_message()
        elif self.current_map.player.current_room == 6 and self.player.highest_wave < 5:
            self.player.rect.center = (1200, 535)
            self.player.hitbox.center = (1200, 535)
            self.dialogue.clear_dialogue()
            self.dialogue.unreached_requirement_message()
            self.current_map.player.current_room = -1

    def check_events(self):
        self.dialogue.display_dialogue()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if self.current_map == self.merchant_map and event.key == pg.K_e:
                    self.current_map.toggle_menu()
                    self.dialogue.clear_dialogue()
                if self.current_map == self.dungeon_map and event.key == pg.K_ESCAPE:
                    self.current_map.player.current_room = 4
                if event.key == pg.K_p:
                    self.pause()
                if event.key == pg.K_RETURN:
                    self.dialogue.next_dialogue()
                    self.dialogue.display_dialogue()
                    self.boss_map.boss.isIntro = False
                    self.player.bossIntro = False
            # timer event
            if event.type == pygame.USEREVENT:
                self.dungeon_map.timer.update_timer()
                if self.dungeon_map.wave_number == 0:
                    self.dungeon_map.wave_number += 1
                    
                    self.dungeon_map.spawn_wave()
                elif len(self.dungeon_map.enemy) == 0:
                    self.break_period += 1
                    if self.break_period > 5 :
                        self.break_period = 0
                        self.dungeon_map.wave_number += 1
                        self.dungeon_map.spawn_wave()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
            self.death_screen()
            self.game_end_screen()

    def pause(self):
        paused = True

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        paused = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

            self.screen.fill('black')
            PAUSE_TEXT = self.get_font(50).render(
                "Paused", True, "#b68f40")
            PAUSE_RECT = PAUSE_TEXT.get_rect(
                center=(self.screen.get_rect().centerx, 100))
            INFO_TEXT = self.get_font(50).render(
                "Press C to resume or Q to quit", True, "#b68f40")
            INFO_RECT = INFO_TEXT.get_rect(
                center=(self.screen.get_rect().centerx, 300))
            self.screen.blit(PAUSE_TEXT, PAUSE_RECT)
            self.screen.blit(INFO_TEXT, INFO_RECT)
            pygame.display.update()

    def main_menu(self):
        while True:
            pygame.display.set_caption("The Enchanted Blades")
            self.screen.fill('black')
            self.screen.blit(self.BG, (0, 0))
            self.sounds.play_audio(self.sounds.intro_music, -1)

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = self.get_font(50).render(
                "The Enchanted Blades", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(
                center=(self.screen.get_rect().centerx, 100))
            PLAY_BUTTON = Button(image=pygame.image.load("imgs/Play Rect.png"), pos=(self.screen.get_rect().centerx, 250),
                                 text_input="PLAY", font=self.get_font(30), base_color="#d7fcd4", hovering_color="White")
            OPTIONS_BUTTON = Button(image=pygame.image.load("imgs/Options Rect.png"), pos=(self.screen.get_rect().centerx, 400),
                                    text_input="RULES", font=self.get_font(30), base_color="#d7fcd4", hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("imgs/Quit Rect.png"), pos=(self.screen.get_rect().centerx, 550),
                                 text_input="QUIT", font=self.get_font(30), base_color="#d7fcd4", hovering_color="White")

            self.screen.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.play()
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.options()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

    def get_font(self, size):  # Returns Press-Start-2P in the desired size
        return pygame.font.Font("imgs/BreatheFireIii-PKLOB.ttf", size)

    def play(self):
        self.dialogue.intro_message()
        self.sounds.stop_audio()
        self.sounds.play_audio(self.sounds.base_music, -1)
        self.run()

    def options(self):
        while True:
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

            self.screen.fill("black")
            RULE_TEXT = self.get_font(45).render(
                "Defeat 4 waves of enemies to challenge the boss", True, "Green")
            RULE_RECT = RULE_TEXT.get_rect(
                center=(self.screen.get_rect().centerx, 90))
            MOVEMENT_TEXT = self.get_font(30).render(
                "WASD - Player movement", True, "Green")
            MOVEMENT_RECT = MOVEMENT_TEXT.get_rect(
                center=(self.screen.get_rect().centerx, 160))
            PAUSE_TEXT = self.get_font(30).render(
                "P - Pause game", True, "Green")
            PAUSE_RECT = PAUSE_TEXT.get_rect(
                center=(self.screen.get_rect().centerx, 220))
            REACTION_TEXT = self.get_font(30).render(
                "E - Merchant reaction", True, "Green")
            REACTION_RECT = REACTION_TEXT.get_rect(
                center=(self.screen.get_rect().centerx, 280))
            ARROW_TEXT = self.get_font(30).render(
                "Arrow Keys - Choose upgrade option", True, "Green")
            ARROW_RECT = ARROW_TEXT.get_rect(
                center=(self.screen.get_rect().centerx, 340))
            SPACE_TEXT = self.get_font(30).render(
                "Space Bar - Attack/Confirm upgrade", True, "Green")
            SPACE_RECT = SPACE_TEXT.get_rect(
                center=(self.screen.get_rect().centerx, 400))
            ENTER_TEXT = self.get_font(30).render(
                "ENTER - Skip dialogue", True, "Green")
            ENTER_RECT = ENTER_TEXT.get_rect(
                center=(self.screen.get_rect().centerx, 460))
            ESC_TEXT = self.get_font(30).render(
                "ESC - Leave dungeon", True, "Green")
            ESC_RECT = ESC_TEXT.get_rect(
                center=(self.screen.get_rect().centerx, 520))
            self.screen.blit(RULE_TEXT, RULE_RECT)
            self.screen.blit(MOVEMENT_TEXT, MOVEMENT_RECT)
            self.screen.blit(PAUSE_TEXT, PAUSE_RECT)
            self.screen.blit(REACTION_TEXT, REACTION_RECT)
            self.screen.blit(ARROW_TEXT, ARROW_RECT)
            self.screen.blit(SPACE_TEXT, SPACE_RECT)
            self.screen.blit(ENTER_TEXT, ENTER_RECT)
            self.screen.blit(ESC_TEXT, ESC_RECT)

            OPTIONS_BACK = Button(image=None, pos=(self.screen.get_rect().centerx, 620),
                                  text_input="BACK", font=self.get_font(75), base_color="White", hovering_color="Green")

            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_BACK.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        self.main_menu()

            pygame.display.update()


if __name__ == '__main__':
    game = Game()
