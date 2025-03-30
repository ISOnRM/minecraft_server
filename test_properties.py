from pathlib import Path
from handlers import PropertiesHandler

server_path = Path("server_test")
test = PropertiesHandler(server_path)
test.change_port(1000)
#it works trust me