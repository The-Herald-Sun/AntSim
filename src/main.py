# TODO enum for held items
import os
import time
import utils
from random import randint, random, choice


class Sim:
    TICK_RATE = 20  # ticks per second
    TICK_TIME = 1.0 / TICK_RATE

    def __init__(self, size: tuple[int, int]) -> None:
        self.size = size
        self._ants = []
        self._food = []
        self._entities = []
        # Could be a fun idea. Leave for later.
        # self.pheremone_map = [
        #     [[0.0, 0.0] for _ in range(self.size[0])] for _ in range(self.size[1])
        # ]
        pass

    def random_coordinates(self) -> tuple[int, int]:
        return (randint(0, self.size[0] - 1), randint(0, self.size[1] - 1))

    def addAnt(self, ant):
        self._entities.append(ant)
        self._ants.append(ant)

    def addFood(self, food):
        self._food.append(food)

    def run(self):
        while True:
            start = time.time()

            for entity in self._entities:
                entity.tick()
            self.render()

            elapsed_time = time.time() - start
            time.sleep(self.TICK_TIME - elapsed_time)
            pass
        pass

    def move_food(self):
        for food in self._food:
            food.location = self.random_coordinates()

    def render(self):
        screen = [[" " for _ in range(self.size[0])] for _ in range(self.size[1])]
        # print("Size: ", self.size)
        # print("Screen List: ", len(screen), len(screen[0]))
        # print(screen)

        for ant in self._ants:
            screen[ant.location[1]][ant.location[0]] = ant.display

        for food in self._food:
            screen[food.location[1]][food.location[0]] = "f"

        stringed = ""
        for column in screen:
            for line in column:
                stringed += line
            stringed += "\n"

        print(stringed[:-1], end="")

    def get_random_food(self):
        return choice(self._food)


class Entity:
    def __init__(self, location: tuple[int, int]) -> None:
        self.location = location
        # self._sim = sim
        # self._sim
        pass

    def tick(self):
        pass


# TODO implement better handling of axis selection
class Ant(Entity):
    MOVE_WEIGHT = 0.75  # likelyhood ant moves towards target
    AXIS_SELECTION_WEIGHT_OFFSET = 0.1
    MOVE_DISTANCE = 1

    def __init__(
        self, location: tuple[int, int], target: Entity, sim: Sim, display: str = "A"
    ) -> None:
        super().__init__(location)
        self.target = target
        self._sim = sim
        self._holding = None
        self.display = display
        pass

    @property
    def holding(self):
        return self._holding

    @holding.setter
    def holding(self, value):
        self._holding = value

    def move(self):
        # find target direction in each axis
        # randomly select axis
        # weighted randomly chose to move towards or away
        #
        # if self.target.location == self.location:
        #     self._sim.move_food()  # fun idea
        #     return

        directions = (
            -1 if self.target.location[0] < self.location[0] else 1,
            -1 if self.target.location[1] < self.location[1] else 1,
        )

        if random() > self.MOVE_WEIGHT:
            directions = directions[0] * -1, directions[1] * -1

        column_move = 0
        line_move = 0

        if self.target.location[0] == self.location[0]:
            axis_selection_weight_offset = self.AXIS_SELECTION_WEIGHT_OFFSET * 1
        elif self.target.location[1] == self.location[1]:
            axis_selection_weight_offset = self.AXIS_SELECTION_WEIGHT_OFFSET * -1
        else:
            axis_selection_weight_offset = 0.0

        match random() > 0.5 + axis_selection_weight_offset:
            case True:
                column_move = self.MOVE_DISTANCE * directions[0]
            case False:
                line_move = self.MOVE_DISTANCE * directions[1]

        self.location = (
            utils.clamp(
                self.location[0] + column_move,
                min_val=0,
                max_val=self._sim.size[0] - 1,
            ),
            utils.clamp(
                self.location[1] + line_move, min_val=0, max_val=self._sim.size[1] - 1
            ),
        )
        pass

    def get_direction(self):
        pass

    def tick(self) -> None:
        self.move()
        pass


class Worker(Ant):
    def __init__(self, location, target, sim, queen, display: str = "W") -> None:
        super().__init__(location, target, sim, display)
        self._queen = queen

    def tick(self):
        if self.holding is None:
            self.target = self._sim.get_random_food()
            pass

        if self.location == self.target.location:
            match self.target:
                case Food():
                    self.holding = "food"
                    self.target = self._queen
                    pass
                case Queen():
                    self.holding = None
                    self.target = self._sim.get_random_food()
                    pass

        super().move()


class Queen(Ant):
    ON_TARGET_MOVE_CHANCE = 0.1

    def __init__(self, location, target, sim, display: str = "Q") -> None:
        super().__init__(location, target, sim, display)

    def move(self):
        if self.target.location == self.location:
            if random() < self.ON_TARGET_MOVE_CHANCE:
                super().move()
        else:
            super().move()

    def tick(self):
        self.move()


class Food(Entity):
    def __init__(self, location) -> None:
        super().__init__(location)
        pass


class Nest(Entity):
    def __init__(self, location) -> None:
        super().__init__(location)


def main():
    columns, lines = os.get_terminal_size()
    print(columns, lines)
    sim = Sim(size=(columns, lines))

    nest = Nest(sim.random_coordinates())

    queen = Queen(location=sim.random_coordinates(), target=nest, sim=sim)
    sim.addAnt(queen)

    food = Food(sim.random_coordinates())
    sim.addFood(food)

    workers = [
        Worker(location=sim.random_coordinates(), target=food, sim=sim, queen=queen)
        for _ in range(20)
    ]

    for ant in workers:
        sim.addAnt(ant)

    # ant_loc = (randint(0, columns - 1), randint(0, lines - 1))
    # print("ant_loc: ", ant_loc)
    # targ = food.location
    # game.addAnt(Ant(location=ant_loc, target=targ))

    sim.run()


if __name__ == "__main__":
    try:
        main()
        pass
    except KeyboardInterrupt:
        print("\nClosing")
        pass
    pass
