import traceback
import json
from pathlib import Path

import handlers


class Main:
    """Easiest abstraction"""
    # Here be no descriptor cuz i already have them in handlers
    def __init__(
            self,
            server_dir: Path,
    ):
    
        self.server_dir = server_dir


        self._core_handler = handlers.CoreHandler(self.server_dir)
        self._server_handler = None
        self._world_handler = handlers.WorldHandler(self.server_dir)
        self._mod_handler = handlers.ModHandler(self.server_dir)
        self._properties_handler = handlers.PropertiesHandler(self.server_dir)

    def _init_server_handler(
            self,
            server_dir: Path, #self.server_dir,
            server_core: Path,
            ram: tuple,
            java_path: Path | str = "java"
    ):
        if not self._server_handler:
            self._server_handler = handlers.ServerHandler(
                self.server_dir,
                server_core,
                ram,
                java_path
            )
        
    @staticmethod
    def catch_exceptions(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(
                    f"Exception in {func.__name__}: {e}"
                )
                traceback.print_exc()
        return wrapper


    # Core Handler Shi-
    @catch_exceptions
    def find_core(self):
        core = self._core_handler.find_core()
        return core
    
    @catch_exceptions
    def install_paper_core(
            self, version: str, build: str
    ):
        downloaded_core = self._core_handler.install_paper_core(version, build)
        return downloaded_core

    @catch_exceptions
    def install_other_core(
        self, url: str
    ):
        downloaded_core = self._core_handler.install_other_core(url)
        return downloaded_core
    
    @catch_exceptions
    def remove_core(
        self, name = None
    ):
        self._core_handler.remove_core(name)

    # Server Handler Shi-
    @catch_exceptions
    def start_server(
        self,
        server_core,
        ram,
        java_path = "java"
    ):
        self._init_server_handler(
            self.server_dir,
            server_core,
            ram,
            java_path = "java"
        )
        
        self._server_handler.start_server()

    @catch_exceptions
    def add_icon_sever(
        self,
        image_file
    ):
        self._server_handler.add_server_icon(image_file)

    @staticmethod
    @catch_exceptions
    def remove_server(server_dir):
        handlers.ServerHandler.remove_server(server_dir)


    # World Handler Shi-
    @catch_exceptions
    def pack_world(self, name: str) -> Path:
        packed_world = self._world_handler.pack_current_world(name)
        return packed_world
    
    @catch_exceptions
    def unpack_world(self, name: str):
        self._world_handler.unpack_world_from_archive(name)

    @catch_exceptions
    def remove_world(self, name: str):
        self._world_handler.remove_world(name)

    @catch_exceptions
    def list_world(self):
        for world in self._world_handler._get_world_list():
            print(world)

    # Mod Handler Shi-

    @catch_exceptions
    def download_plugin(self, url: str) -> Path:
        downloaded_plugin = self._mod_handler.download_plugin(url)
        return downloaded_plugin

    @catch_exceptions
    def bulk_plugin(self, file_name: Path) -> list:
        list_of_plugin_paths = self._mod_handler.download_plugins_bulk(file_name)
        return list_of_plugin_paths
    
    @catch_exceptions
    def remove_plugin(self, name: str):
        self._mod_handler.remove_plugin(name)

    @catch_exceptions
    def remove_each_plugin(self):
        self._mod_handler.remove_all_plugins()

    @catch_exceptions
    def toggle_plugin(
        self, name: str, disable: bool
    ):
        self._mod_handler.toggle_plugin(name, disable)

    @catch_exceptions
    def get_plugin_name(self, display: bool) -> list:
        list_of_plugin_names = self._mod_handler.get_plugin_names()

        if display:
            for plugin_name in list_of_plugin_names:
                print(plugin_name)

        return list_of_plugin_names
    

    # Propereties Hanlder shi-

    @catch_exceptions
    def change_port_in_properties(self, new_port):
        self._properties_handler.change_port(new_port)

    @catch_exceptions
    def change_any_param_in_properties(self, param, new_value):
        
        self._properties_handler \
        ._change_param(
            param, new_value
        )

class Config:
    def __init__(
            self,
            config: Path = Path("server_config.json")
    ):
        config = config.resolve()
        if not config.exists():
            raise FileNotFoundError
        
        self.config = config

        self._main = None

    def _get_config(self):
        try:
            with open(self.config, "r") as config:
                data = json.load(config)
        except json.JSONDecodeError:
            print("Corrupted json file")
        
        self._data = data
    
    def _load_main(self):
        
        if self._data:
            self._main = Main(
                server_dir=Path(self._data["server"]["server_dir"])
            )
        
            
    def _load_core(self) -> Path:
        if not self._main:
            raise ValueError
        
        core = self._main.find_core()

        if not core:
            url = self._data["server"]["server_core"]["url"]
            version, build = self._data["server"]["server_core"]["version"], self._data["server"]["server_core"]["build"]

            if url:
                core_path = self._main.install_other_core(url)
            elif version and build:
                core_path = self._main.install_paper_core(version, build)
            else:
                raise ValueError
            
            return core_path

        return core
    
    
    def __call__(self):
        self._get_config()
        self._load_main()
        core = self._load_core()
        self._main.start_server(
            core,
            (self._data["server"]["ram"][0], self._data["server"]["ram"][1]),
            self._data["server"]["java_path"]
        )