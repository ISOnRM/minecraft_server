from pathlib import Path
import main
server = main.Main(Path("server_test"))
server.install_paper_core("1.21.4", "222")
core = server.find_core()
server.start_server(core, (4, 6))
# server.remove_server(core.parent)