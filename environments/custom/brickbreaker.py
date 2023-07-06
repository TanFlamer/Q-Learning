import gym
import numpy as np
import pygame
from gym import spaces


class BrickBreakerEnv(gym.Env):
    # Env metadata
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 60}
    screen_width, screen_height = 600, 450

    def __init__(self, render_mode=None,
                 brick_placement="Row", brick_rows=3, brick_columns=8,
                 paddle_speed=10, ball_speed=5, game_mode=False):

        # Ball and paddle
        self.paddle = Paddle(paddle_speed, game_mode, self.screen_width, self.screen_height)
        self.ball = Ball(ball_speed, game_mode, self.screen_width, self.screen_height)

        # Bricks
        self.bricks = Bricks(brick_placement, brick_rows, brick_columns,
                             game_mode, self.screen_width, self.screen_height)
        self.bricks.generate_bricks()

        # Brick breaker observation
        low = np.array([0] * 5, dtype=np.float32)
        high = np.array(
            [
                self.screen_width,
                self.screen_height,
                self.screen_width,
                self.screen_height,
                brick_rows * brick_columns
            ],
            dtype=np.float32
        )

        # Spaces
        self.observation_space = spaces.Box(low, high)
        self.action_space = spaces.Discrete(3)

        # Set game render mode
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        # Used to render game
        self.window = None
        self.clock = None

    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        # Reset ball and paddle
        x_pos = self.np_random.integers(0, 520, dtype=int)
        self.paddle.reset_paddle(x_pos)
        self.ball.reset_ball(x_pos)

        # Reset bricks
        self.bricks.reset_bricks()

        if self.render_mode == "human":
            self._render_frame()

        return np.array([*self.paddle.paddle_center(), *self.ball.ball_center(),
                         len(self.bricks.brick_list)], dtype=np.float32), {}

    def step(self, action):
        # Move ball and paddle
        self.ball.move_ball()
        self.paddle.move_paddle(action)

        # Check ball collision
        paddle = self.paddle.paddle
        bricks = self.bricks.brick_list
        brick_collisions = self.ball.ball_collision(paddle, bricks)
        self.bricks.hit_bricks(brick_collisions)

        # An episode is done if the agent has reached the target
        terminated = bool(self.ball.ball_termination() or self.bricks.brick_termination())
        reward = 1

        if self.render_mode == "human":
            self._render_frame()

        return np.array([*self.paddle.paddle_center(), *self.ball.ball_center(),
                         len(self.bricks.brick_list)], dtype=np.float32), reward, terminated, False, {}

    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()

    def _render_frame(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.screen_width, self.screen_height))

        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        canvas = pygame.Surface((self.screen_width, self.screen_height))
        canvas.fill((214, 209, 245))

        # Draw game objects
        self.paddle.display_paddle(canvas)
        self.ball.display_ball(canvas)
        self.bricks.display_bricks(canvas)

        if self.render_mode == "human":
            # The following line copies our drawings from `canvas` to the visible window
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()

            # We need to ensure that human-rendering occurs at the predefined framerate.
            # The following line will automatically add a delay to keep the framerate stable.
            self.clock.tick(self.metadata["render_fps"])
        else:  # rgb_array
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
            )

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()


class Ball:
    def __init__(self, speed, game_mode, screen_width, screen_height):
        # Ball settings
        self.ball = None
        self.speed = speed
        self.diameter = 20
        self.colour = (255, 255, 255)

        # Ball direction
        self.horizontal = 0
        self.vertical = 0

        # Screen dimensions
        self.game_mode = game_mode
        self.screen_width = screen_width
        self.screen_height = screen_height

    def reset_ball(self, x):
        # Get ball direction
        self.horizontal = np.random.choice([-1, 1])
        self.vertical = 1 if self.game_mode else -1

        # Create new ball
        y = 45 if self.game_mode else self.screen_height - 45
        self.ball = pygame.Rect(x, y, self.diameter, self.diameter)

    def move_ball(self):
        # Get ball horizontal
        x = self.horizontal * self.speed
        x = min(self.screen_width - self.ball.right, x) if x >= 0 else -min(self.ball.left, abs(x))
        # Get ball vertical
        y = self.vertical * self.speed
        y = min(self.screen_height - self.ball.bottom, y) if y >= 0 else -min(self.ball.top, abs(y))
        # Move ball
        self.ball.move_ip(x, y)

    def ball_collision(self, paddle, bricks):
        # Check wall collision
        self.wall_collision()
        # Check ceiling collision
        self.ceiling_collision()
        # Check paddle collision
        self.paddle_collision(paddle)
        # Check brick collisions
        return self.brick_collision(bricks)

    def paddle_collision(self, paddle):
        # Collide with paddle
        collision = self.ball.colliderect(paddle)
        if collision: self.object_collision(paddle)

    def brick_collision(self, bricks):
        # Get brick collisions
        collisions = self.ball.collidelistall(bricks)
        brick_count = len(collisions)
        # Collision type
        if brick_count > 1:
            # Change vertical direction
            self.vertical *= -1
        elif brick_count == 1:
            # Collide with brick
            index = collisions[0]
            self.object_collision(bricks[index])
        # Return brick indices
        return collisions

    def wall_collision(self):
        # Wall collision
        if self.ball.left <= 0 or self.ball.right >= self.screen_width:
            # Change horizontal direction
            self.horizontal *= -1

    def ceiling_collision(self):
        # Ceiling collision
        if self.ball.bottom >= self.screen_height if self.game_mode else self.ball.top <= 0:
            # Change vertical direction
            self.vertical *= -1

    def object_collision(self, obj):
        # Get ball center
        ball_center = self.ball.centerx
        # Change ball direction
        if obj.left <= ball_center <= obj.right:
            self.vertical *= -1
        elif obj.left > ball_center:
            self.horizontal = -1
        else:
            self.horizontal = 1

    def ball_termination(self):
        # Check ball termination
        return self.ball.top <= 0 if self.game_mode else self.ball.bottom >= self.screen_height

    def display_ball(self, canvas):
        # Draw ball
        pygame.draw.ellipse(
            canvas,
            self.colour,
            self.ball
        )

        # Draw outline
        pygame.draw.ellipse(
            canvas,
            (0, 0, 0),
            self.ball,
            1
        )

    def ball_center(self):
        # Return paddle center
        return self.ball.center


class Paddle:
    def __init__(self, speed, game_mode, screen_width, screen_height):
        # Paddle settings
        self.paddle = None
        self.width = 80
        self.height = 10
        self.colour = (255, 182, 67)

        # Paddle movement
        self.paddle_movement = {
            0: -speed,
            1: 0,
            2: speed
        }

        # Other settings
        self.game_mode = game_mode
        self.screen_width = screen_width
        self.screen_height = screen_height

    def reset_paddle(self, x):
        y = 25 if self.game_mode else self.screen_height - 25
        self.paddle = pygame.Rect(x, y, self.width, self.height)

    def move_paddle(self, action):
        # Get paddle horizontal
        x = self.paddle_movement[action]
        x = min(self.screen_width - self.paddle.right, x) if x >= 0 else -min(self.paddle.left, abs(x))
        # Move paddle
        self.paddle.move_ip(x, 0)

    def display_paddle(self, canvas):
        # Draw paddle
        pygame.draw.rect(
            canvas,
            self.colour,
            self.paddle
        )

        # Draw outline
        pygame.draw.rect(
            canvas,
            (0, 0, 0),
            self.paddle,
            1
        )

    def paddle_center(self):
        # Return paddle center
        return self.paddle.center


class Bricks:
    def __init__(self, placement, rows, columns,
                 game_mode, screen_width, screen_height):

        # Brick generation
        self.placement = placement
        self.rows = rows
        self.columns = columns

        # Brick settings
        self.width = screen_width / columns
        self.height = 20
        self.colour = {
            1: (69, 53, 170),
            2: (237, 99, 158),
            3: (143, 225, 162)
        }

        # Other settings
        self.game_mode = game_mode
        self.screen_height = screen_height

        # Brick data
        self.brick_data = []
        self.brick_list = []
        self.brick_hits = []

    def generate_bricks(self):

        # Brick row loop
        for y in range(self.rows):

            # Brick column loop
            for x in range(self.columns):

                # Get brick coordinates
                brick_x = x * self.width
                offset = y * self.height + 50
                brick_y = self.screen_height - offset if self.game_mode else offset

                # Create brick object
                brick = pygame.Rect(brick_x, brick_y, self.width, self.height)
                self.brick_data.append((brick, self.brick_hit(x, y)))

    def brick_hit(self, column, row):
        # If brick placement random
        if self.placement == "Random":
            # Generate random brick
            return np.random.randint(1, 4)
        else:
            # Alternate brick by row/column
            point = row if self.placement == "Row" else column
            return 3 - (point % 3)

    def reset_bricks(self):
        # Clear old lists
        self.brick_list.clear()
        self.brick_hits.clear()

        # Reset brick data
        for brick, hits in self.brick_data:
            # Copy to lists
            self.brick_list.append(brick)
            self.brick_hits.append(hits)

    def hit_bricks(self, brick_collisions):
        # Loop through indices
        for index in reversed(brick_collisions):
            # Hit bricks
            self.brick_hits[index] -= 1
            # Check brick destruction
            if self.brick_hits[index] <= 0:
                # Destroy brick
                del self.brick_list[index]
                del self.brick_hits[index]

    def brick_termination(self):
        # Check if all bricks destroyed
        return len(self.brick_list) <= 0

    def display_bricks(self, canvas):
        # Loop through bricks
        for brick, hits in zip(self.brick_list, self.brick_hits):
            # Draw brick
            pygame.draw.rect(
                canvas,
                self.colour[hits],
                brick
            )

            # Draw outline
            pygame.draw.rect(
                canvas,
                (0, 0, 0),
                brick,
                1
            )
