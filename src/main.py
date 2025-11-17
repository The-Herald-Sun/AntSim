import os
import time
from random import randint, random


class Game:
    TICK_RATE = 10  # ticks per second
    TICK_TIME = 1.0 / TICK_RATE

    def __init__(self, size: tuple[int, int]) -> None:
        self.size = size
        self.ants = []
        self.food = []
        pass

    def addAnt(self, ant):
        self.ants.append(ant)

    def addFood(self, food):
        self.food.append(food)

    def run(self):
        while True:
            start = time.time()

            for ant in self.ants:
                ant.move()
            self.render()

            elapsed_time = time.time() - start
            time.sleep(self.TICK_TIME - elapsed_time)
            pass
        pass

    def render(self):
        screen = [["*" for _ in range(self.size[0])] for _ in range(self.size[1])]
        # print("Size: ", self.size)
        # print("Screen List: ", len(screen), len(screen[0]))
        # print(screen)

        for ant in self.ants:
            screen[ant.location[1]][ant.location[0]] = "."

        for food in self.food:
            screen[food.location[1]][food.location[0]] = "a"

        stringed = ""
        for column in screen:
            for line in column:
                stringed += line
            stringed += "\n"

        print(stringed[:-1], end="")


class Entity:
    def __init__(self, location: tuple[int, int]) -> None:
        self.location = location
        pass


class Ant(Entity):
    MOVE_WEIGHT = 0.85  # likelyhood ant moves towards target
    MOVE_DISTANCE = 1

    def __init__(self, location: tuple[int, int], target: tuple[int, int]) -> None:
        super().__init__(location)
        self.target = target
        pass

    def move(self):
        # find target direction in each axis
        # randomly select axis
        # weighted randomly chose to move towards or away
        #
        if self.target == self.location:
            return

        directions = (
            -1 if self.target[0] < self.location[0] else 1,
            -1 if self.target[1] < self.location[1] else 1,
        )

        if random() > self.MOVE_WEIGHT:
            directions = directions[0] * -1, directions[1] * -1

        column_move = 0
        line_move = 0
        match randint(0, 1):
            case 0:
                column_move = self.MOVE_DISTANCE * directions[0]
            case 1:
                line_move = self.MOVE_DISTANCE * directions[1]

        self.location = (self.location[0] + column_move, self.location[1] + line_move)
        pass


class Worker(Ant):
    def __init__(self, location, target) -> None:
        super().__init__(location, target)


class Food(Entity):
    def __init__(self, location) -> None:
        super().__init__(location)
        pass


def main():
    columns, lines = os.get_terminal_size()
    print(columns, lines)
    game = Game(size=(columns, lines))

    food = Food((randint(0, columns - 1), randint(0, lines - 1)))
    game.addFood(food)

    ant_loc = (randint(0, columns - 1), randint(0, lines - 1))
    print("ant_loc: ", ant_loc)
    targ = food.location

    game.addAnt(Ant(location=ant_loc, target=targ))

    game.run()


if __name__ == "__main__":
    try:
        main()
        pass
    except KeyboardInterrupt:
        print("\nClosing")
        pass
    pass
