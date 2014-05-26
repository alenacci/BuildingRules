from grid import Grid
from room_generator import RoomGenerator
import building

building.grid = Grid("./res/map_grid.png")
building.roomGenerator = RoomGenerator("./res/map_rooms.png")