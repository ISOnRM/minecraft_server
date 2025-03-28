from pathlib import Path

from handlers import ModHandler


server_dir = Path("server_test")
plugins_dir = server_dir / Path("plugins")
test = ModHandler(server_dir)
# lst = test.download_plugins_bulk(plugins_dir / "test_list")
# for i in lst:
#     print(i.name)
# test.remove_all_plugins()
# test.toggle_plugin("Chunky-Bukkit-1_4_28", disable=False)
# lst = test.get_plugin_names()
# for i in lst:
#     print(i)