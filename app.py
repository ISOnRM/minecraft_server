import argparse
from pathlib import Path

from main import Main, Config

def create_parser():
    """
    Creates the command-line argument parser with two modes:
    
    1. Config mode: Use the 'config' command to load and apply the server configuration
       from a JSON file.
       Example: python3 app.py config --file server_config.json

    2. Manual mode: Specify a server directory and then choose the subject and action.
       Example: python3 app.py manual /path/to/server_dir core install --url https://api.papermc.io/v2/projects/paper/versions/1.21.4/builds/222/downloads/paper-1.21.4-222.jar
                python3 app.py manual /path/to/server_dir server start --ram 4 6
    """
    parser = argparse.ArgumentParser(
        description="Server util -> https://github.com/ISOnRM/minecraft_server"
    )
    # Top-level subparsers for mode selection.
    mode_subparsers = parser.add_subparsers(
        title="Modes",
        dest="mode",
        required=True,
        help="Choose one of the following modes: config or manual"
    )
    
    # ----------- Config mode -----------
    config_parser = mode_subparsers.add_parser(
        "config",
        help="Load and apply server configuration from a JSON file"
    )
    config_parser.add_argument(
        "-f", "--file",
        type=Path,
        required=True,
        help="Path to the JSON configuration file"
    )
    
    # ----------- Work mode -----------
    manual_parser = mode_subparsers.add_parser(
        "manual",
        help="Operate on a specific server directory with various actions"
    )
    manual_parser.add_argument(
        "work_dir",
        help="Path to the server directory",
        type=Path
    )
    
    # Subparsers for different subjects in work mode.
    subject_subparsers = manual_parser.add_subparsers(
        title="Subjects",
        dest="subjects",
        required=True,
        help="Choose one of the following subjects: core, server, world, plugin, properties"
    )
    
    # ------------------ Core commands ------------------
    core_parser = subject_subparsers.add_parser(
        "core",
        help="Core operations: install core from URL, install Paper build, or remove core"
    )
    core_actions = core_parser.add_subparsers(
        title="Core Actions",
        dest="action",
        required=True,
        help="Available actions: install, install-paper, remove"
    )
    # Core install (using URL)
    core_install = core_actions.add_parser(
        "install",
        help="Install core using a specified URL"
    )
    core_install.add_argument(
        "--url",
        type=str,
        required=True,
        help="URL to download and install the core"
    )
    # Core install-paper (install Paper build)
    core_install_paper = core_actions.add_parser(
        "install-paper",
        help="Install a Paper server build using version and build number"
    )
    core_install_paper.add_argument(
        "--version",
        type=str,
        required=True,
        help="Minecraft version for the Paper build"
    )
    core_install_paper.add_argument(
        "--build",
        type=str,
        required=True,
        help="Build number for the Paper build"
    )
    # Core remove
    core_remove = core_actions.add_parser(
        "remove",
        help="Remove the core file; optionally specify the core name"
    )
    core_remove.add_argument(
        "--name",
        type=str,
        default=None,
        help="Name of the core file to remove (if not specified, the default core is removed)"
    )
    
    # ------------------ Server commands ------------------
    server_parser = subject_subparsers.add_parser(
        "server",
        help="Server operations: start, remove, or change the server icon"
    )
    server_actions = server_parser.add_subparsers(
        title="Server Actions",
        dest="action",
        required=True,
        help="Available actions: start, remove, icon"
    )
    # Server start
    server_start = server_actions.add_parser(
        "start",
        help="Start the server with specified options"
    )
    server_start.add_argument(
        "--ram",
        nargs=2,
        metavar=("MIN", "MAX"),
        type=int,
        help="Minimum and maximum RAM (in GB) for the server"
    )
    # Server remove
    server_remove = server_actions.add_parser(
        "remove",
        help="Remove the server installation"
    )
    # Server icon
    server_icon = server_actions.add_parser(
        "icon",
        help="Change the server icon"
    )
    server_icon.add_argument(
        "--file",
        type=Path,
        help="Path to the new icon file"
    )
    
    # ------------------ World commands ------------------
    world_parser = subject_subparsers.add_parser(
        "world",
        help="World operations: pack, unpack, remove or list worlds"
    )
    world_actions = world_parser.add_subparsers(
        title="World Actions",
        dest="action",
        required=True,
        help="Available actions: pack, unpack, remove, list"
    )
    # World pack
    world_pack = world_actions.add_parser(
        "pack",
        help="Pack the current world into an archive"
    )
    world_pack.add_argument(
        "--name",
        type=str,
        required=True,
        help="Name for the world archive"
    )
    # World unpack
    world_unpack = world_actions.add_parser(
        "unpack",
        help="Unpack a world from an archive"
    )
    world_unpack.add_argument(
        "--name",
        type=str,
        required=True,
        help="Name of the world archive to unpack"
    )
    # World remove
    world_remove = world_actions.add_parser(
        "remove",
        help="Remove an existing world"
    )
    world_remove.add_argument(
        "--name",
        type=str,
        required=True,
        help="Name of the world to remove"
    )
    # World list
    world_list = world_actions.add_parser(
        "list",
        help="List all available world archives"
    )
    
    # ------------------ Plugin commands ------------------
    plugin_parser = subject_subparsers.add_parser(
        "plugin",
        help="Plugin operations: download, bulk download, remove, toggle or list plugins"
    )
    plugin_actions = plugin_parser.add_subparsers(
        title="Plugin Actions",
        dest="action",
        required=True,
        help="Available actions: download, bulk, remove, toggle, list"
    )
    # Plugin download
    plugin_download = plugin_actions.add_parser(
        "download",
        help="Download a plugin from a specified URL"
    )
    plugin_download.add_argument(
        "--url",
        type=str,
        required=True,
        help="URL of the plugin to download"
    )
    # Plugin bulk download
    plugin_bulk = plugin_actions.add_parser(
        "bulk",
        help="Download plugins in bulk from a file containing URLs"
    )
    plugin_bulk.add_argument(
        "--file",
        type=Path,
        required=True,
        help="Path to a file with plugin URLs (one per line)"
    )
    # Plugin remove
    plugin_remove = plugin_actions.add_parser(
        "remove",
        help="Remove a plugin by name"
    )
    plugin_remove.add_argument(
        "--name",
        type=str,
        required=True,
        help="Name of the plugin to remove"
    )
    # Plugin toggle (enable/disable)
    plugin_toggle = plugin_actions.add_parser(
        "toggle",
        help="Toggle the state of a plugin (enable or disable)"
    )
    plugin_toggle.add_argument(
        "--name",
        type=str,
        required=True,
        help="Name of the plugin to toggle"
    )
    plugin_toggle.add_argument(
        "--disable",
        action="store_true",
        help="If set, disable the plugin instead of enabling it"
    )
    # Plugin list
    plugin_list = plugin_actions.add_parser(
        "list",
        help="List all installed plugins"
    )
    
    # ------------------ Properties commands ------------------
    properties_parser = subject_subparsers.add_parser(
        "properties",
        help="Server properties operations: change port or modify any property"
    )
    properties_actions = properties_parser.add_subparsers(
        title="Properties Actions",
        dest="action",
        required=True,
        help="Available actions: change-port, change-any"
    )
    # Change server port
    properties_change_port = properties_actions.add_parser(
        "change-port",
        help="Change the server port"
    )
    properties_change_port.add_argument(
        "--port",
        type=int,
        required=True,
        help="New port number for the server"
    )
    # Change any property
    properties_change_any = properties_actions.add_parser(
        "change-any",
        help="Change any property in the server configuration"
    )
    properties_change_any.add_argument(
        "--param",
        type=str,
        required=True,
        help="Name of the property to change"
    )
    properties_change_any.add_argument(
        "--value",
        type=str,
        required=True,
        help="New value for the property"
    )
    
    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.mode == "config":
        # Config mode: load configuration from the specified JSON file.
        config = Config(args.file)
        config()
    elif args.mode == "manual":
        # Manual mode: use the given work_dir to initialize Main.
        main_obj = Main(args.work_dir)
        if args.subjects == "core":
            if args.action == "install":
                main_obj.install_other_core(args.url)
            elif args.action == "install-paper":
                main_obj.install_paper_core(args.version, args.build)
            elif args.action == "remove":
                main_obj.remove_core(args.name)
        elif args.subjects == "server":
            if args.action == "start":
                core = main_obj.find_core()
                ram = tuple(args.ram) if args.ram else (2, 4)
                main_obj.start_server(core, ram)
            elif args.action == "remove":
                Main.remove_server(args.work_dir)
            elif args.action == "icon":
                main_obj.add_icon_sever(args.file)
        elif args.subjects == "world":
            if args.action == "pack":
                main_obj.pack_world(args.name)
            elif args.action == "unpack":
                main_obj.unpack_world(args.name)
            elif args.action == "remove":
                main_obj.remove_world(args.name)
            elif args.action == "list":
                main_obj.list_world()
        elif args.subjects == "plugin":
            if args.action == "download":
                main_obj.download_plugin(args.url)
            elif args.action == "bulk":
                main_obj.bulk_plugin(args.file)
            elif args.action == "remove":
                main_obj.remove_plugin(args.name)
            elif args.action == "toggle":
                main_obj.toggle_plugin(args.name, args.disable)
            elif args.action == "list":
                main_obj.get_plugin_name(display=True)
        elif args.subjects == "properties":
            if args.action == "change-port":
                main_obj.change_port_in_properties(args.port)
            elif args.action == "change-any":
                main_obj.change_any_param_in_properties(args.param, args.value)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
