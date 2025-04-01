# Minecraft Server Linux-Like Command

In this repository you will find my application that will allow you to create and manage your Minecraft server with Linux-like commands. The CLI program is located in the `app.py` file. It uses the `argparse` library to let you handle the server's core, the server's directory, its worlds, plugins, and properties. You are also allowed to load your server from a configuration file in JSON format (an example file is provided in the repo).

---

## Loading Server via Configuration

To load your server via config you'll need to choose the server's directory name, provide a download URL for a core (or enter the version and its Paper build while leaving the URL as an empty string), set your RAM constraints, and provide the Java path on your Linux machine.

When the JSON file is set, you'll need to enter the following command:

```bash
python3 app.py config --file config_name.json
```

The program will then install the core and start the server showing the preferences on start:

```bash
$ python3 app.py config --file server_config.json

==================================================
            STARTING THE SERVER...
            Server's directory: server_test
            Core: paper-1.21.4-222.jar
            Min RAM: 1
            Max RAM: 2
==================================================

Downloading mojang_1.21.4.jar

<SNIP>

[20:17:38 INFO]: Done (9.505s)! For help, type "help"
[20:17:38 INFO]: *************************************************************************************
[20:17:38 INFO]: This is the first time you're starting this server.
[20:17:38 INFO]: It's recommended you read our 'Getting Started' documentation for guidance.
[20:17:38 INFO]: View this and more helpful information here: https://docs.papermc.io/paper/next-steps
[20:17:38 INFO]: *************************************************************************************
>
```

To stop the server, simply press **CTRL+C** to trigger a `KeyboardInterrupt` or type `stop` in the server's console:

```bash
> # Here i pressed CTRL+C
[20:18:57 INFO]: Stopping server
[20:18:57 INFO]: Saving players
[20:18:57 INFO]: Saving worlds

<SNIP>

==================================================
                  CTRL + C
             STOPPING THE SERVER
==================================================

<SNIP>

[20:18:57 INFO]: All I/O tasks to complete
[20:18:57 INFO]: [MoonriseCommon] Awaiting termination of worker pool for up to 60s...
[20:18:57 INFO]: [MoonriseCommon] Awaiting termination of I/O pool for up to 60s...
$
```

---

## Manual Mode

If you wish to manually set up your server or manage an already existing server, you will need to use manual mode.

### Setting Up the Server

```bash
$ python3 app.py manual server_test/ core install-paper --version 1.21.4 --build 222
$ cd server_test/
$ ls -1
paper-1.21.4-222.jar
plugins
server.properties
```

### Starting the Server

```bash
$ cd ..
$ python3 app.py manual server_test/ server --help
```

```text
usage: app.py manual work_dir server [-h] {start,remove,icon} ...

options:
  -h, --help           show this help message and exit

Server Actions:
  {start,remove,icon}  Available actions: start, remove, icon
    start              Start the server with specified options
    remove             Remove the server installation
    icon               Change the server icon
```

```bash
$ python3 app.py manual server_test/ server start --help
```

```text
usage: app.py manual work_dir server start [-h] [--ram MIN MAX]

options:
  -h, --help     show this help message and exit
  --ram MIN MAX  Minimum and maximum RAM (in GB) for the server
```

```bash
$ python3 app.py manual server_test/ server start --ram 2 4

==================================================
            STARTING THE SERVER...
            Server's directory: server_test
            Core: paper-1.21.4-222.jar
            Min RAM: 2
            Max RAM: 4
==================================================

Downloading mojang_1.21.4.jar

<SNIP>

[20:28:39 INFO]: Done (9.135s)! For help, type "help"
[20:28:39 INFO]: *************************************************************************************
[20:28:39 INFO]: This is the first time you're starting this server.
[20:28:39 INFO]: It's recommended you read our 'Getting Started' documentation for guidance.
[20:28:39 INFO]: View this and more helpful information here: https://docs.papermc.io/paper/next-steps
[20:28:39 INFO]: *************************************************************************************
>
```

The `app.py` will find the newest (by its name) core and start the server with the given RAM arguments. The default values for RAM are `min = 4 GB` and `max = 6 GB`.

### Managing Worlds

To work with server worlds, use the following command to see available actions:

```bash
$ python3 app.py manual server_test/ world --help
```

```text
usage: app.py manual work_dir world [-h] {pack,unpack,remove,list} ...

options:
  -h, --help            show this help message and exit

World Actions:
  {pack,unpack,remove,list}
                        Available actions: pack, unpack, remove, list
    pack                Pack the current world into an archive
    unpack              Unpack a world from an archive
    remove              Remove an existing world
    list                List all available world archives
```

### Packing a World

```bash
$ python3 app.py manual server_test/ world list
$ python3 app.py manual server_test/ world pack --name World_one
$ ls server_test/ | grep tar
World_one.tar
$ python3 app.py manual server_test/ world list
World_one
```

The command above archives the current world into a tar archive with the given name.

### Unpacking a World

```bash
$ python3 app.py manual server_test/ world list
World_one
$ python3 app.py manual server_test/ world unpack --name World_one
$ python3 app.py manual server_test/ world list
$ ls server_test/ | grep world
world
world_nether
world_the_end
```

Voilà, you have just unpacked your world.

---

## Managing Plugins

To download plugins for your server, follow these steps. For example, to add two plugins—Chunky and SkinsRestorer—create a file with their download links:

```bash
$ touch plugins.txt
$ echo "https://cdn.modrinth.com/data/TsLS8Py5/versions/4DON6SzK/SkinsRestorer.jar" > plugins.txt
$ echo "https://cdn.modrinth.com/data/fALzjamp/versions/ytBhnGfO/Chunky-Bukkit-1.4.28.jar" >> plugins.txt
$ cat plugins.txt
https://cdn.modrinth.com/data/TsLS8Py5/versions/4DON6SzK/SkinsRestorer.jar
https://cdn.modrinth.com/data/fALzjamp/versions/ytBhnGfO/Chunky-Bukkit-1.4.28.jar
```

### Bulk Downloading Plugins

```bash
$ python3 app.py manual server_test/ plugin --help
```

```text
usage: app.py manual work_dir plugin [-h] {download,bulk,remove,toggle,list} ...

options:
  -h, --help            show this help message and exit

Plugin Actions:
  {download,bulk,remove,toggle,list}
                        Available actions: download, bulk, remove, toggle, list
    download            Download a plugin from a specified URL
    bulk                Download plugins in bulk from a file containing URLs
    remove              Remove a plugin by name
    toggle              Toggle the state of a plugin (enable or disable)
    list                List all installed plugins
```

```bash
$ python3 app.py manual server_test/ plugin bulk --file plugins.txt
/home/mark/Desktop/Python_Learning/new_minecraft_server/server_test/plugins/SkinsRestorer.jar
/home/mark/Desktop/Python_Learning/new_minecraft_server/server_test/plugins/Chunky-Bukkit-1_4_28.jar
$ python3 app.py manual server_test/ plugin list
Chunky-Bukkit-1_4_28
SkinsRestorer
```

*Note: Dots in plugin filenames are replaced with underscores to prevent extension issues.*

### Toggling a Plugin

```bash
$ python3 app.py manual server_test/ plugin toggle --help
```

```text
usage: app.py manual work_dir plugin toggle [-h] --name NAME [--disable]

options:
  -h, --help   show this help message and exit
  --name NAME  Name of the plugin to toggle
  --disable    If set, disable the plugin instead of enabling it
```

```bash
$ python3 app.py manual server_test/ plugin list
Chunky-Bukkit-1_4_28
SkinsRestorer
$ python3 app.py manual server_test/ plugin toggle --name SkinsRestorer --disable
$ python3 app.py manual server_test/ plugin list
Chunky-Bukkit-1_4_28
SkinsRestorer (disabled)
$ python3 app.py manual server_test/ plugin toggle --name SkinsRestorer
$ python3 app.py manual server_test/ plugin list
Chunky-Bukkit-1_4_28
SkinsRestorer
```

---

## Editing Server Properties

To change the port or any property the server runs on, use the properties feature:

```bash
$ python3 app.py manual server_test/ properties --help
```

```text
usage: app.py manual work_dir properties [-h] {change-port,change-any} ...

options:
  -h, --help            show this help message and exit

Properties Actions:
  {change-port,change-any}
                        Available actions: change-port, change-any
    change-port         Change the server port
    change-any          Change any property in the server configuration
```

To change the server port:

```bash
$ python3 app.py manual server_test/ properties change-port --help
```

```text
usage: app.py manual work_dir properties change-port [-h] --port PORT

options:
  -h, --help   show this help message and exit
  --port PORT  New port number for the server
```

```bash
$ python3 app.py manual server_test/ properties change-port --port 7777
$ cat server_test/server.properties | grep server-port
server-port=7777
```

You can also change any property with the `change-any` feature.

---

## Removing the Server

To delete your server completely:

```bash
$ python3 app.py manual server_test/ server remove
$ ls server_test/
ls: cannot access 'server_test/': No such file or directory
```

---

## Upcoming Features

- Shortened arguments (e.g., `-p` instead of `--port`)
- Default values in some commands (e.g., port defaults to `25565`)
- Packed world compression

---

**First ever repo.**