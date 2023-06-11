import random
import tkinter as tk


class GameObject(object):
    def __init__(self, canvas, item):
        self.canvas = canvas
        self.item = item

    def get_position(self):
        return self.canvas.coords(self.item)

    def get_midpoint(self):
        coordinates = self.get_position()
        return [(coordinates[0] + coordinates[2]) / 2, (coordinates[1] + coordinates[3]) / 2]

    def move(self, x, y):
        self.canvas.move(self.item, x, y)

    def delete(self):
        self.canvas.delete(self.item)


class Ball(GameObject):
    def __init__(self, canvas, x, y, speed, game_mode, canvas_dimensions):
        # Create ball object
        self.radius = 10
        item = canvas.create_oval(x - self.radius, y - self.radius,
                                  x + self.radius, y + self.radius,
                                  fill='white')
        super(Ball, self).__init__(canvas, item)

        # Ball settings
        ball_direction = [-1, 1]
        self.direction = [random.choice(ball_direction), ball_direction[game_mode]]
        self.speed = speed

        # Other settings
        self.game_mode = game_mode
        [self.canvas_width, self.canvas_height] = canvas_dimensions

    def update_ball_position(self):
        # Get ball coordinates
        coordinates = self.get_position()
        # Check for wall collision
        self.horizontal_collision(coordinates)
        self.vertical_collision(coordinates)
        # Get new ball displacement
        x = self.direction[0] * self.speed
        y = self.direction[1] * self.speed
        # Move ball
        self.move(x, y)

    def horizontal_collision(self, coordinates):
        # If ball hits left or right wall
        if coordinates[0] <= 0 or coordinates[2] >= self.canvas_width:
            # Change horizontal direction
            self.direction[0] *= -1

    def vertical_collision(self, coordinates):
        # If ball hits top/bottom border (depends on game mode)
        if coordinates[3] >= self.canvas_height if self.game_mode else coordinates[1] <= 0:
            # Change vertical direction
            self.direction[1] *= -1

    def collide(self, game_objects):
        # Get ball midpoint
        x = self.get_midpoint()[0]

        # If more than one object
        if len(game_objects) > 1:
            # Change vertical direction
            self.direction[1] *= -1
        # If only one object
        elif len(game_objects) == 1:
            # Get object position
            game_object = game_objects[0]
            coordinates = game_object.get_position()
            # Change ball direction
            if x > coordinates[2]:
                self.direction[0] = 1
            elif x < coordinates[0]:
                self.direction[0] = -1
            else:
                self.direction[1] *= -1

        # Damage all bricks
        for game_object in game_objects:
            if isinstance(game_object, Brick):
                game_object.hit()


class Paddle(GameObject):
    def __init__(self, canvas, x, y, offset, canvas_dimensions):
        # Create paddle object
        self.width = 80
        self.height = 7
        item = canvas.create_rectangle(x - self.width / 2,
                                       y - self.height / 2,
                                       x + self.width / 2,
                                       y + self.height / 2,
                                       fill='#FFB643')
        super(Paddle, self).__init__(canvas, item)

        # Paddle settings
        self.offset = offset

        # Other settings
        [self.canvas_width, _] = canvas_dimensions

    def doNothing(self):
        # Do nothing to paddle
        super(Paddle, self).move(0, 0)

    def moveLeft(self):
        # Get paddle position
        coordinates = self.get_position()
        # If paddle does not leave left edge
        if coordinates[0] - self.offset >= 0:
            # Move paddle left
            super(Paddle, self).move(-self.offset, 0)

    def moveRight(self):
        # Get paddle position
        coordinates = self.get_position()
        # If paddle does not leave right edge
        if coordinates[2] + self.offset <= self.canvas_width:
            # Move paddle right
            super(Paddle, self).move(self.offset, 0)


class Brick(GameObject):
    # Brick colours
    COLORS = {1: '#4535AA', 2: '#ED639E', 3: '#8FE1A2'}

    def __init__(self, canvas, x, y, hits, brick_width, brick_height):
        # Create brick object
        color = Brick.COLORS[hits]
        item = canvas.create_rectangle(x - brick_width / 2,
                                       y - brick_height / 2,
                                       x + brick_width / 2,
                                       y + brick_height / 2,
                                       fill=color, tags='brick')
        super(Brick, self).__init__(canvas, item)

        # Brick settings
        self.hits = hits

    def hit(self):
        # Reduce brick health
        self.hits -= 1
        # If brick health 0
        if self.hits == 0:
            # Delete brick
            self.delete()
        else:
            # Change brick colour
            self.canvas.itemconfig(self.item, fill=Brick.COLORS[self.hits])


class Game(tk.Frame):
    def __init__(self, master, game_settings, other_settings, qLearning, results):
        super(Game, self).__init__(master)

        # Save data for next loop
        self.game_settings = game_settings
        self.other_settings = other_settings
        self.qLearning = qLearning
        self.results = results

        # Unpack game data
        [self.ball_speed, self.paddle_speed, self.game_mode, self.episodes] = self.game_settings
        [self.dimensions, self.bricks, self.runs, self.exclude_failure] = self.other_settings

        # Create canvas
        [self.width, self.height] = self.dimensions
        self.canvas = tk.Canvas(self, bg='#D6D1F5', width=self.width, height=self.height, )
        self.canvas.pack()
        self.pack()

        # Game objects
        self.items = {}
        self.paddle = self.add_paddle()
        self.ball = self.add_ball()

        # Paddle movement
        self.actions = [self.paddle.moveLeft, self.paddle.moveRight, self.paddle.doNothing]

        # Game setup
        self.setup_game()
        self.canvas.focus_set()

    def setup_game(self):
        self.place_bricks()
        self.qLearning.new_episode(self.getObv())
        self.update_text()
        self.game_loop()

    def add_paddle(self):
        # Get paddle coordinates
        paddle_x = random.randint(40, self.width - 40)
        paddle_y = self.select_value(25, self.height - 25)
        # Create paddle object
        paddle = Paddle(self.canvas, paddle_x, paddle_y, self.paddle_speed, self.dimensions)
        self.items[paddle.item] = paddle
        return paddle

    def add_ball(self):
        # Get ball coordinates
        [x, y] = self.paddle.get_midpoint()
        offset = self.select_value(16, -16)
        # Create ball object
        ball = Ball(self.canvas, x, y + offset, self.ball_speed, self.game_mode, self.dimensions)
        return ball

    def place_bricks(self):
        # Brick count
        brick_rows = len(self.bricks)
        bricks_in_row = len(self.bricks[0])
        # Brick dimensions
        brick_width = self.width / bricks_in_row
        brick_height = 20
        # Brick row loop
        for y in range(brick_rows):
            # Brick column loop
            for x in range(bricks_in_row):
                # Get brick coordinates
                brick_x = (x + 0.5) * brick_width
                offset = y * brick_height + 50
                brick_y = self.select_value(self.height - offset, offset)
                # Get brick health
                hits = self.bricks[y][x]
                # Create brick object
                brick = Brick(self.canvas, brick_x, brick_y, hits, brick_width, brick_height)
                self.items[brick.item] = brick

    def select_value(self, first, second):
        # Return value based on game mode
        return first if self.game_mode else second

    def update_text(self):
        # Number of runs text
        run_text = "Runs: " + str(len(self.results) + 1)
        self.create_text(75, run_text)
        # Number of episodes text
        episode_text = "Episodes: " + str(self.qLearning.episodes)
        self.create_text(300, episode_text)
        # Number of failed runs text
        failed_text = "Failed: " + str(self.qLearning.runs - len(self.results))
        self.create_text(525, failed_text)

    def create_text(self, x, text):
        y = self.select_value(self.height - 20, 20)
        self.canvas.create_text(x, y, text=text, font=('Forte', 15))

    def getObv(self):
        # Return paddle and ball position
        return [self.paddle.get_position(), self.ball.get_position()]

    def game_loop(self):
        # Get action
        action = self.qLearning.select_action()
        # Get opposite observation
        opposite_obv = self.opposite_action(action)
        # Perform action
        self.actions[action]()
        # Check for collision
        self.check_collisions()
        # Update Q-Learning policy
        self.qLearning.update_policy(self.getObv(), opposite_obv, action, self.out_of_bounds())
        # Get number of bricks
        num_bricks = len(self.canvas.find_withtag('brick'))
        # Get number of episode
        episode = self.qLearning.episodes
        # If all bricks destroyed
        if num_bricks == 0:
            # Append result and reset run
            self.reset_run(episode, True)
            # Reset game
            self.reset_game()
        # Ball out of bounds
        elif self.out_of_bounds():
            # Check if exceed episodes
            if episode >= self.episodes:
                self.reset_run(self.episodes, False)
            # Reset game
            self.reset_game()
        else:
            # Update ball position
            self.ball.update_ball_position()
            # Next loop
            self.after(1, self.game_loop)

    def reset_run(self, episode, success):
        if success:
            # Append results if run success
            self.results.append(episode)
            print("Run %d finished in %d episodes" % (len(self.results), episode))
        else:
            # Append results if genetic algorithm
            if not self.exclude_failure: self.results.append(episode)
            print("Run failed in %d episodes" % episode)
        # Start new run
        self.qLearning.new_run()

    def reset_game(self):
        # Close window
        self.destroy()
        # Get number of runs
        num_runs = len(self.results)
        # If not enough runs
        if num_runs < self.runs:
            # Start new game
            self.__init__(self.master, self.game_settings, self.other_settings, self.qLearning, self.results)
        else:
            # Append total number of runs
            self.results.append(self.qLearning.runs)
            # Quit game
            self.master.quit()

    def check_collisions(self):
        # Get ball position
        ball_coordinates = self.ball.get_position()
        # Check ball for overlap
        items = self.canvas.find_overlapping(*ball_coordinates)
        objects = [self.items[x] for x in items if x in self.items]
        # Ball collision
        self.ball.collide(objects)

    def out_of_bounds(self):
        # Get ball coordinates
        ball_coordinates = self.ball.get_position()
        # Check if ball leaves top/bottom border (depends on game mode)
        return ball_coordinates[1] <= 0 if self.game_mode else ball_coordinates[3] >= self.height

    def opposite_action(self, action):
        # Move paddle
        def move(coordinates, dist):
            coordinates[0] += dist
            coordinates[2] += dist

        # Get paddle position
        paddle_coordinates = self.paddle.get_position()
        # Paddle offset
        offset = self.paddle.offset
        # Get opposite action
        opposite_action = 1 - action

        # If paddle does not leave left edge
        if opposite_action == 0 and paddle_coordinates[0] - offset >= 0:
            # Move paddle left
            move(paddle_coordinates, -offset)
        # If paddle does not leave right edge
        elif opposite_action == 1 and paddle_coordinates[2] + offset <= self.width:
            # Move paddle right
            move(paddle_coordinates, offset)

        # Return new paddle and ball position
        return [paddle_coordinates, self.ball.get_position()]
