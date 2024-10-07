import argparse
import os
import importlib
import sys
from typing import Dict, Type
import logging
import inspect
import io
import contextlib

from base_command import BaseCommand

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class CommandRegistry:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="LDO Command-Line Interface")
        self.subparsers = self.parser.add_subparsers(dest="command", required=True)
        self.registered_commands: Dict[str, BaseCommand] = {}

    def register(self, command_name: str, command_class: Type[BaseCommand]) -> None:
        logger.debug(f"Registering command: {command_name}")
        if command_name not in self.subparsers.choices:
            subparser = self.subparsers.add_parser(command_name)
            command_instance = command_class()
            command_instance.register(subparser)
            self.registered_commands[command_name] = command_instance
            logger.debug(f"Registered command: {command_name}")
        else:
            logger.warning(f"Command {command_name} already registered. Skipping.")

    def parse_and_run(self) -> None:
        logger.debug(f"Registered commands: {list(self.registered_commands.keys())}")

        # First, parse just the command to avoid premature exit
        command_parser = argparse.ArgumentParser(add_help=False)
        command_parser.add_argument(
            "-v", "--verbose", action="store_true", help="Enable verbose output"
        )
        command_parser.add_argument("command")
        try:
            command_args, remaining_args = command_parser.parse_known_args()
            if command_args.verbose:
                logging.basicConfig(level=logging.DEBUG)
        except SystemExit:
            self.parser.print_help()
            return

        if command_args.command in self.registered_commands:
            command_instance = self.registered_commands[command_args.command]
            command_subparser = self.subparsers.choices[command_args.command]

            # Caputre the top-level failed parse error and let us handle it explicitly
            # Without capturing the stderr, we'll see two error messages
            with contextlib.redirect_stderr(io.StringIO()):
                try:
                    args = command_subparser.parse_args(remaining_args)
                    command_instance.run(args)
                except SystemExit:
                    # If parsing fails, print the help for the requested subcommand
                    self.print_subcommand_help(command_args.command, remaining_args)
                    sys.exit(0)
        else:
            self.parser.print_help()

    def print_subcommand_help(self, command: str, args: list):
        """Print help for a specific subcommand, including nested subcommands."""
        subparser = self.subparsers.choices[command]

        # Check if there are nested subparsers
        nested_subparsers = next(
            (
                action
                for action in subparser._actions
                if isinstance(action, argparse._SubParsersAction)
            ),
            None,
        )

        if nested_subparsers and args:
            # If there's a nested subparser and we have arguments, try to print help for the nested command
            nested_command = args[0]
            if nested_command in nested_subparsers.choices:
                nested_subparsers.choices[nested_command].print_help()
            else:
                subparser.print_help()
        else:
            # If no nested subparsers or no arguments, print help for the main subcommand
            subparser.print_help()


def import_and_register_commands(registry: CommandRegistry):
    commands_dir = os.path.join(os.path.dirname(__file__), "commands")
    logger.debug(f"Looking for commands in: {commands_dir}")
    for filename in os.listdir(commands_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"commands.{filename[:-3]}"
            logger.debug(f"Attempting to import module: {module_name}")
            try:
                module = importlib.import_module(module_name)
                for name, obj in inspect.getmembers(module):
                    if (
                        inspect.isclass(obj)
                        and issubclass(obj, BaseCommand)
                        and obj != BaseCommand
                    ):
                        logger.debug(f"Found command class: {name}")
                        command_name = name.lower().replace("command", "")
                        registry.register(command_name, obj)
            except Exception as e:
                logger.error(f"Error importing module {module_name}: {str(e)}")
                logger.exception("Exception details:")


def main():
    registry = CommandRegistry()
    import_and_register_commands(registry)
    registry.parse_and_run()


if __name__ == "__main__":
    main()
