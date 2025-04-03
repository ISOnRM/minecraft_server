from pathlib import Path

class ServerDir:
    def __init__(
            self, attr_name, type
    ):
        self.attr_name = '_' + attr_name
        self.type = type

    def __get__(self, instance, owner):
        if not instance:
            return self
        return getattr(instance, self.attr_name, None)
    
    def __set__(self, instance, value: Path):

        if not isinstance(value, self.type):
            raise ValueError(f"{value} is of wrong type")
        value = value.resolve()
        script_directory = Path(__file__).parent.resolve()

        if not value.relative_to(script_directory):
            raise ValueError(f"{value} has to be in {script_directory}")
        
        if value.exists():
            if not value.is_dir():
                raise ValueError(f"{value} is not a directory")
        else:
            value.mkdir()

        setattr(instance, self.attr_name, value)

    
class ServerCore:
    def __init__(
            self, attr_name, type
    ):
        self.attr_name = '_' + attr_name
        self.type = type
        

    def __get__(self, instance, owner):
        if not instance:
            return self
        return getattr(instance, self.attr_name, None)
    
    def __set__(self, instance, value):
        server_dir = instance.server_dir
        value = value.resolve()

        if not server_dir:
            raise ValueError(f"Instance has to have a server_dir")
        
        if not value.is_relative_to(server_dir):
            raise ValueError(f"{value} is not in {server_dir}")
        
        setattr(instance, self.attr_name, value)

class MinMaxRam:
    def __init__(
            self, attr_name, type
    ):
        self.attr_name = '_' + attr_name
        self.type = type

    def __get__(self, instance, owner):
        if not instance:
            return self
        return getattr(instance, self.attr_name, None)
    
    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            raise ValueError(f"{value} is of wrong type")
        if len(value) != 2:
            raise ValueError("Wrong amount of items")
        
        value = tuple(map(abs, value))
        
        min_ram, max_ram = value

        if min_ram < max_ram:
            setattr(instance, self.attr_name, value)
        else:
            raise ValueError("Minimal value has to be smaller than the maximum value. Duh")