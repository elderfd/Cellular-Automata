# User-input variables ###################################

# Simulation settings ------------------------------------
# Give the size of the grid to simulate on
number_of_rows_in_grid = 100
number_of_columns_in_grid = 100

# The maximum FPS the simulation will be displayed at
fps = 30

# Gives colouring rule for images
# This matches a cell state value to an RGB colour
colour_rule = {
    # Syntax is - cell value: (R, G, B)
    1: (0, 0, 0),
    0: (255, 255, 255)
}
# ------------------------------------------------------

# Rules to use in the model
def game_of_life(current_state, list_of_neighbour_states):
    total = sum(list_of_neighbour_states)

    if current_state == 0:
        if total == 3:
            return 1
        else:
            return 0
    else:
        if total < 2 or total > 3:
            return 0
        else:
            return 1

rule_set = game_of_life
