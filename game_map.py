class GameMap:
    def __init__(self, name, layout):
        self.name = name
        self.layout = layout
        self.player_x = 1
        self.player_y = 1

    def display(self):
        print(f"\n=== {self.name} ===")

        for y, row in enumerate(self.layout):
            line = ""
            for x, cell in enumerate(row):
                if x == self.player_x and y == self.player_y:
                    line += "@ "
                else:
                    line += cell + " "
            print(line)

    def move(self, direction):
        moves = {
            "w": (0, -1),
            "s": (0, 1),
            "a": (-1, 0),
            "d": (1, 0)
        }

        if direction not in moves:
            print("Use W, A, S or D.")
            return False

        dx, dy = moves[direction]
        nx = self.player_x + dx
        ny = self.player_y + dy

        if not (0 <= ny < len(self.layout)):
            print("Outside the map!")
            return False

        if not (0 <= nx < len(self.layout[ny])):
            print("Outside the map!")
            return False

        if self.layout[ny][nx] == "#":
            print("A wall blocks your path!")
            return False

        self.player_x = nx
        self.player_y = ny

        if self.layout[ny][nx] == "E":
            print("You reached the exit!")
            return True

        return False

FOREST = GameMap("Whispering Forest", [
    "###########",
    "#S...#....#",
    "###..#.#..#",
    "#....#.#..#",
    "#.####....#",
    "#......##E#",
    "###########"
])

DUNGEON = GameMap("Ancient Dungeon", [
    "#############",
    "#S..#.......#",
    "#.#.#.#####.#",
    "#.#...#.....#",
    "#.#####.###.#",
    "#.......#..E#",
    "#############"
])
