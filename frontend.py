import backend
import pygame
import datetime

# Gives the current number of milliseconds since epoch
def msecs_since_epoch():
    epoch = datetime.datetime(1970, 1, 1)
    diff = datetime.datetime.now() - epoch
    return (diff.microseconds * 1000)

# Provides the display for the simulation and allows interaction
class Display:
    def __init__(self, n_rows, n_cols, max_fps, colour_rule, rule_set):
        # Set up pygame stuff first
        pygame.init()

        # Some defaults
        default_window_width = 500
        default_window_height = 500

        self.border_thickness = 2

        self.square_x_size = (default_window_width - 2 * self.border_thickness) / n_cols
        self.square_y_size = (default_window_height - 2 * self.border_thickness) / n_rows

        self.screen_options = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE
        pygame.display.set_caption("Cellular Automata")
        self.screen = pygame.display.set_mode([default_window_width, default_window_height], self.screen_options)
        self.rule = rule_set
        self.colour_rule = colour_rule

        # Work out the number of states there are
        max_state = 0
        for key in colour_rule:
            if key > max_state:
                max_state = key

        self.grid = backend.Grid(n_rows, n_cols, max_state, True)
        self.button_pressed_in_window = False
        self.simulating = False
        self.min_time_between_frames = 1 / max_fps
        self.time_of_last_draw = 0

    # Returns a Rect which matches the given grid x, y coordinates
    def grid_coords_to_display_rect(self, x, y):
        left = self.grid_x_to_display_x(x)
        top = self.grid_y_to_display_y(y)
        width = self.square_x_size + 2 * self.border_thickness
        height = self.square_y_size + 2 * self.border_thickness
        return pygame.Rect(left, top, width, height)

    def grid_x_to_display_x(self, x):
        return x * self.square_x_size + self.border_thickness

    def grid_y_to_display_y(self, y):
        return y * self.square_y_size + self.border_thickness

    def render(self):
        # Draw the coloured squares
        for x in range(self.grid.n_cols):
            for y in range(self.grid.n_rows):
                # Grab the value in the grid, choose the right colour
                # Then draw a box to match
                colour = self.colour_rule[self.grid.get_state(x, y)]
                rect = self.grid_coords_to_display_rect(x, y)
                pygame.draw.rect(self.screen, colour, rect)

        # Whack in some grid lines
        black = (0, 0, 0)

        x = 1
        while x < self.grid.n_cols:
            startCoords = (self.grid_x_to_display_x(x) , self.grid_y_to_display_y(0))
            endCoords = (self.grid_x_to_display_x(x), self.grid_y_to_display_y(self.grid.n_rows))
            pygame.draw.line(self.screen, black, startCoords, endCoords)
            x += 1

        y = 1
        while y < self.grid.n_rows:
            startCoords = (self.grid_x_to_display_x(0), self.grid_y_to_display_y(y))
            endCoords = ( self.grid_x_to_display_x(self.grid.n_cols), self.grid_y_to_display_y(y))
            pygame.draw.line(self.screen, black, startCoords, endCoords)
            y += 1

        # Special coloured grid lines around edge to show play/ pause
        topLeft = (0, 0)
        topRight = (self.square_x_size * self.grid.n_cols, 0)
        bottomRight = (self.square_x_size * self.grid.n_cols, self.square_y_size * self.grid.n_rows)
        bottomLeft=(0, self.square_y_size * self.grid.n_rows)

        if self.simulating:
            borderColour = (0, 255, 0)
        else:
            borderColour = (255, 0, 0)

        # Maybe should use draw.lines in future but this won't
        # be a rate-limiting step and some issues with joins
        # apparently
        pygame.draw.line(self.screen, borderColour, topLeft, topRight)
        pygame.draw.line(self.screen, borderColour, topRight, bottomRight)
        pygame.draw.line(self.screen, borderColour, bottomRight, bottomLeft)
        pygame.draw.line(self.screen, borderColour, bottomLeft, topLeft)

        pygame.display.update()

    def run(self):
        stop = False

        # Initial draw
        self.render()

        while not stop:
            # Deal with any queued events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.VIDEORESIZE:
                    # Rescale to match new size
                    newRes = event.dict['size']
                    self.square_x_size = (newRes[0] - self.border_thickness) / self.grid.n_cols
                    self.square_y_size = (newRes[1] - self.border_thickness) / self.grid.n_rows
                    self.screen = pygame.display.set_mode(newRes, self.screen_options)

                    self.render()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.button_pressed = event.button
                    self.button_pressed_in_window = True
                    self.button_press_coords = pygame.mouse.get_pos()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.button_pressed_in_window:
                        self.button_pressed_in_window = False
                        gridX = self.button_press_coords[0] / self.square_x_size
                        gridY = self.button_press_coords[1] / self.square_y_size

                        if self.button_pressed == 1:
                            # LMB
                            self.grid.increment_state(gridX, gridY)
                        elif self.button_pressed == 3:
                            # RMB
                            self.grid.decrement_state(gridX, gridY)

                        self.render()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    # If running then pause, otherwise start running
                    self.simulating = not self.simulating
                    self.render()

            if self.simulating:
                # Make sure we don't render too quickly
                if msecs_since_epoch() - self.time_of_last_draw > self.min_time_between_frames:
                    self.grid.apply_rule(self.rule)
                    self.render()
