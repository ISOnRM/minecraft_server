from pathlib import Path
from handlers import CoreHandler, ServerHandler

server_dir = Path("server_test")

core = CoreHandler(server_dir)
core_path = core.install_paper_core("1.21.4", "212")

server = ServerHandler(
    server_dir,
    core_path,
    (4,6)
)
server.start_server()

# server.remove_server()