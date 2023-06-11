import random
import numpy as np


def get_bricks(initial_settings):
    # Set random seed
    seed = initial_settings[0]
    random.seed(seed)
    np.random.seed(seed)
    # Generate bricks
    brick_settings = initial_settings[1:]
    return Bricks(brick_settings).generate_bricks()


class Bricks:
    def __init__(self, bricks_data):
        # Unpack brick data
        [self.brick_placement, self.brick_rows, self.bricks_in_row] = bricks_data
        # Brick list
        self.bricks = []

    def generate_bricks(self):
        # Brick row loop
        for y in range(self.brick_rows):
            brick_row = []
            # Brick column loop
            for x in range(self.bricks_in_row):
                # Append new brick
                brick_row.append(self.brick_type(x, y))
            # Append new brick row
            self.bricks.append(brick_row)
        # Return new bricks
        return self.bricks

    def brick_type(self, x, y):
        # If brick placement random
        if self.brick_placement == "Random":
            # Generate random brick
            return random.randint(1, 3)
        else:
            # Alternate brick by row/column
            point = y if self.brick_placement == "Row" else x
            return 3 - (point % 3)