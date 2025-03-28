from pathlib import Path
from handlers import WorldHandler

world_handler = WorldHandler(Path("server_test"))
world_handler.pack_current_world("world_test_1")
worlds = world_handler._get_world_list() # нарушается инкапсуляция (для теста пусть будет, а так вне класса этот метод не используется)
print(worlds)
# world_handler.unpack_world_from_archive(worlds[0])