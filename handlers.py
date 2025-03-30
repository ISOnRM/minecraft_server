import requests
import subprocess
import sys
import shutil
import tarfile
from pathlib import Path

import descriptors

class CoreHandler:
    """A class that handles minecraft server's core."""

    server_dir = descriptors.ServerDir("server_dir", Path)

    def __init__(
            self, server_dir: Path 
    ):
        self.server_dir = server_dir

    def find_core(self):
        cores = sorted(
            [core.resolve() for core in self.server_dir.iterdir() if core.suffix == ".jar" and not core.is_dir()],
            reverse=True
        ) # finds the first item of a list of cores (The newest core by build (?))
        return cores[0] if cores else None

    def install_paper_core(
            self, version: str, build: str
    ) -> Path:
        url = f"https://api.papermc.io/v2/projects/paper/versions/{version}/builds/{build}/downloads/paper-{version}-{build}.jar"

        # with requests.get(url, stream=True) as response:
        #     response.raise_for_status()
        #     block_size = 8192

        #     file_name = self.server_dir / url.split("/")[-1]

        #     with open(file_name, "wb") as file:
        #         for chunk in response.iter_content(chunk_size=block_size):
        #             file.write(chunk)
            
        # return file_name.resolve()

        return self.install_other_core(url=url)

    def install_other_core(
            self, url: str
    ) -> Path:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            block_size = 8192

            file_name = self.server_dir / url.split("/")[-1]

            with open(file_name, "wb") as file:
                for chunk in response.iter_content(chunk_size=block_size):
                    file.write(chunk)
            
        return file_name.resolve()

    def remove_core(
            self, name = None
    ):
        if name:
            core_file = self.server_dir / name
            if not core_file.exists():
                raise ValueError(f"{core_file} does not exist.")
            core_file.unlink()
            return
        core_file = [file.resolve() for file in self.server_dir.glob("*.jar")]
        for file in core_file:
            file.unlink()


class ServerHandler:
    """A class that handles server's start and it's entire removal."""
    server_dir = descriptors.ServerDir("server_dir", Path)
    server_core = descriptors.ServerCore("server_core", Path)
    ram = descriptors.MinMaxRam("ram", tuple)

    def __init__(
            self, server_dir, server_core, ram, java_path = "java"
    ):
        self.server_dir = server_dir
        self.server_core = server_core
        self.ram = ram
        self.java_path = java_path
        

    def _print_server(self, stop: bool):
        if stop:
            print("\033[91m" + """
==================================================
                  CTRL + C
             STOPPING THE SERVER
==================================================
""" + "\033[0m")
        else:
            print("\033[92m" + f"""
==================================================
            STARTING THE SERVER...
            Server's directory: {self.server_dir.name}
            Core: {self.server_core.name}
            Min RAM: {self.ram[0]}
            Max RAM: {self.ram[1]}
==================================================
""" + "\033[0m")


    def _eula_handling(self):
        eula = self.server_dir / "eula.txt"
        if not eula.exists():
            with open(eula, "w") as file:
                file.write("eula=true")
        


    def start_server(self):

        self._eula_handling()

        command = [
            self.java_path, f"-Xms{self.ram[0]}G", f"-Xmx{self.ram[1]}G", "-jar", str(self.server_core.name), "--nogui"
        ]

        server = subprocess.Popen(
            command, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr, text=True, cwd=self.server_dir
        )

        try:
            self._print_server(stop=False)
            server.wait()
        except KeyboardInterrupt:
            self._print_server(stop=True)
            if server.stdin:
                server.stdin.write("stop\n")
                server.stdin.flush()
            server.wait()

    @staticmethod
    def remove_server(server_dir):
        if isinstance(server_dir, Path):
            if server_dir.exists() and server_dir.is_dir():
                if [file.resolve() for file in server_dir.iterdir() if file.name == "eula.txt"]:
                    shutil.rmtree(server_dir)
                    return
        raise ValueError(f"{server_dir} is not a server dir")

class WorldHandler:
    """A class that handles worlds."""
    server_dir = descriptors.ServerDir("server_dir", Path)

    def __init__(
           self, server_dir 
    ):
        self.server_dir: Path = server_dir
        self._current_world = []

    def _get_current_world(self) -> list:
        for directory in self.server_dir.glob("world*"):
            if directory.is_dir():
                self._current_world.append(directory)
        
        return self._current_world if self._current_world else None
        
    def pack_current_world(
            self, name: str
    ) -> Path:
        archive_path = self.server_dir / Path(name).with_suffix(".tar")
        
        if not archive_path.relative_to(self.server_dir):
            raise ValueError(f"{archive_path.name} has to be in {self.server_dir}")
        
        
        current_world = self._get_current_world()
        packed_worlds = self._get_world_list()
        if packed_worlds:
            if archive_path in packed_worlds:
                raise FileExistsError(f"World with the same name exists: {archive_path}")

        if current_world:
            with tarfile.open(archive_path, mode="w") as archive:
                for dir in current_world:
                    dir_path = self.server_dir / dir
                    archive.add(dir_path, arcname=dir.name)
        
        if archive_path.exists():
            for dir in self._current_world:
                shutil.rmtree(dir)
            self._current_world.clear()
            return archive_path
    
    def _get_world_list(self):
        lst = [file.stem for file in self.server_dir.iterdir() if file.suffix == ".tar"]
        return lst
    
    def unpack_world_from_archive(
            self, name: str
    ):
        
        current_world = self._get_current_world()
        if not current_world:
            archive_path = self.server_dir / Path(name).with_suffix(".tar")

            if archive_path.exists():
                with tarfile.open(archive_path, mode="r") as archive:
                    archive.extractall(path=self.server_dir)
                archive_path.unlink()
            else:
                raise FileNotFoundError(f"World {name} was not found")
        else:
            raise FileExistsError("You have to save your current world first")


    def remove_world(
            self, name: str
    ):
        world_path = self.server_dir / Path(name).with_suffix(".tar")
        if world_path.exists():
            world_path.unlink()
        else:
            raise FileNotFoundError(f"World {name} was not found")
    
class ModHandler:
    """A class that downloads mods AKA plugins on your server"""
    server_dir = descriptors.ServerDir("server_dir", Path)

    def __init__(
            self, server_dir
    ):
        self.server_dir = server_dir

        self.plugins_dir = self.server_dir / Path("plugins")
        if not self.plugins_dir.exists():
            self.plugins_dir.mkdir()
        

    def download_plugin(
            self, url: str
    ) -> Path:

        name = url.split("/")[-1]
        
        r_dot_index = name.rfind(".")
        name = name[:r_dot_index].replace(".", "_") + name[r_dot_index:]

        name = self.plugins_dir / Path(name)

        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            block_size = 4096

            with open(name, "wb") as file:
                for chunk in response.iter_content(chunk_size=block_size):
                    file.write(chunk)
            
        
        return name.resolve()
    
    def download_plugins_bulk(
            self, file_name: Path
    ) -> list:
        file_path = file_name.resolve()
        if not file_path.exists():
            raise FileNotFoundError(f"{file_path} not found")
        
        download_paths = []
        with open(file_path, "r") as file:
            for link in file:
                link = link.strip()
                if not link:
                    continue
                plugin_path = self.download_plugin(link)
                print(plugin_path)
                download_paths.append(plugin_path)

        return download_paths
    
    def remove_plugin(
            self, name:str
    ):
        path = self.plugins_dir / Path(name).with_suffix(".jar")
        if not path.exists():
            raise FileNotFoundError(f"{path} plugin does not exist")
        
        path.unlink()
        print(f"{path.name} removed.")

    def remove_all_plugins(self):
        plugins = [str(plugin.name) for plugin in self.plugins_dir.iterdir() if plugin.suffix == ".jar"]
        if not plugins:
            raise FileNotFoundError(f"No plugins found in {self.plugins_dir}")
        for file in plugins:
            self.remove_plugin(file)

    def toggle_plugin(
            self, name: str, disable: bool
    ):
        enabled: Path = self.plugins_dir / Path(name).with_suffix(".jar")
        disabled: Path = self.plugins_dir / Path(name).with_suffix(".disabled")

        if not (enabled.exists() or disabled.exists()):
            raise FileNotFoundError(f"There is no disabled nor enabled plugin with a name {name}")
       
        if disable:
            enabled.rename(disabled)
        elif not disable:
            disabled.rename(enabled)
        else:
            ValueError(f"{disable} has to be of bool value")

   # toggle all plugins

    def get_plugin_names(self) -> list:
        plugins = sorted([plugin.resolve() for plugin in self.plugins_dir.iterdir() if plugin.suffix == ".jar" or plugin.suffix == ".disabled"])
        if not plugins:
            raise FileNotFoundError(f"No plugins were found in {self.plugins_dir}")
        plugin_names = []
        for name in plugins:
            if name.suffix == ".jar":
                item = str(name.stem)
                plugin_names.append(item)
            elif name.suffix == ".disabled":
                item = f"{str(name.stem)} (disabled)"
                plugin_names.append(item)
            else:
                raise ValueError(f"Unknown item in {plugins}")
        
        return plugin_names
    
    # remove plugin directory
    # add a method that will pack uhhhhh the fkn plugins in a tar archive

class PropertiesHandler:
    """Class that handles server properties"""
    server_dir = descriptors.ServerDir("server_dir", Path)

    def __init__(
            self, server_dir
    ):
        self.server_dir = server_dir

        properties_file: Path = self.server_dir / Path("server.properties")
        if not properties_file.exists():
            raise FileNotFoundError("server properties file not found")
        self.properties_file = properties_file    

    def _read(self) -> str:
        with open(self.properties_file, "r") as file:
            return file.read()
        
    def _change(
            self,
            old: str,
            new: str
    ):
        if not isinstance(old, str) and not isinstance(new, str):
            raise ValueError("provide string arguments")
        
        text = self._read()
        text = text.replace(old, new)
        with open(self.properties_file, "w") as file:
            file.write(text)

    def _find_value(self, param: str):
        if not isinstance(param, str):
            raise ValueError("provde param of type str")
        
        with open(self.properties_file, "r") as file:
            for line in file:
                line = line.strip()
                if not line or "=" not in line:
                    continue
                key, value = line.split("=", 1)

                if key == param:
                    return value
        return None
    
    def _change_param(self, param, new_value):
        self._change(
            self._find_value(param),
            new_value
        )
    
    def change_port(self, new_port: str | int):
        self._change_param(
            "server-port",
            str(new_port)
        )
    #add more if needed, motd, icon etc