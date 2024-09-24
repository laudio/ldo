import argparse
from abc import ABC, abstractmethod


class BaseCommand(ABC):
    @abstractmethod
    def register(self, subparser: argparse.ArgumentParser) -> None:
        """Register the command and its subcommands."""
        pass

    @abstractmethod
    def run(self, args: argparse.Namespace) -> None:
        """Run the command with the parsed arguments."""
        pass
