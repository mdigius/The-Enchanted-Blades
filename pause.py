import pygame

class Pause:
    def __init__(self, screen, font=None, font_size=48, font_color=(0, 0, 0), bg_color=(255, 255, 255)):
        # Store the screen object
        self.screen = screen

        # Set up the font for the "paused" screen
        if font is None:
            font = pygame.font.SysFont(None, font_size)
        self.font = font
        self.font_size = font_size
        self.font_color = font_color

        # Set up the background color for the "paused" screen
        self.bg_color = bg_color

        # Set up the paused variable to indicate whether the game is paused or not
        self.paused = False

        # Store the last time the "p" key was pressed
        self.last_pause_time = None

        # Set up a delay before the "p" key can be pressed again
        self.pause_delay = 200  # milliseconds

        # Set up a message to display on the "paused" screen
        self.message = font.render("Paused", True, font_color)

        # Set up an image to display on the "paused" screen
        self.image = None
        self.image_rect = None

        # Set up a button to display on the "paused" screen
        self.button = None
        self.button_rect = None

    def handle_events(self, event):
        # Check for the "p" key being pressed to toggle the paused state
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            if self.last_pause_time is None or pygame.time.get_ticks() - self.last_pause_time >= self.pause_delay:
                self.paused = not self.paused
                self.last_pause_time = pygame.time.get_ticks()

        # Check for the "q" key being pressed to quit the game
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            pygame.quit()
            quit()

    def draw(self):
        # Draw the "paused" screen if the game is paused
        if self.paused:
            # Create a surface to display the paused screen on
            paused_surf = pygame.Surface(self.screen.get_size())
            paused_surf.set_alpha(128)  # Set the transparency of the surface

            # Fill the surface with the background color
            paused_surf.fill(self.bg_color)

            # Blit the message onto the surface
            paused_surf.blit(self.message, ((self.screen.get_width() - self.message.get_width()) // 2,
                                            (self.screen.get_height() - self.message.get_height()) // 2))

            # Blit the image onto the surface, if there is one
            if self.image is not None:
                paused_surf.blit(self.image, self.image_rect)

            # Blit the button onto the surface, if there is one
            if self.button is not None:
                paused_surf.blit(self.button, self.button_rect)

            # Blit the paused surface onto the main screen
            self.screen.blit(paused_surf, (0, 0))

    def is_paused(self):
        # Return whether the game is paused or not
        return self.paused

    def set_paused(self, paused):
        # Set the paused state of the game
        self.paused = paused

    def set_message(self, message):
        # Set the message to display on the "paused" screen
        self.message = self.font.render(message, True, self.font_color)

    def set_bg_color(self, color):
        # Set the background color for the "paused" screen
        self.bg_color = color

    def set_font_color(self, color):
        # Set the font color for the "paused" screen message
        self.font_color = color

    def set_font_size(self, size):
        # Set the font size for the "paused" screen message
        self.font_size = size
        self.font = pygame.font.SysFont(None, size)  # Update the font object