import argparse
import os
from ldo.main import BaseCommand
from ldo.utils import run_command
from ldo.constants import CORE_DIR
import logging

logger = logging.getLogger(__name__)


class CoreCommand(BaseCommand):
    def register(self, subparser: argparse.ArgumentParser) -> None:
        """Register the core command and its subcommands."""
        action_subparsers = subparser.add_subparsers(dest="action", required=True)

        # Register 'rebuild' action
        rebuild_parser = action_subparsers.add_parser(
            "rebuild", help="Rebuild the core repository"
        )

    def run(self, args: argparse.Namespace) -> None:
        """Run the appropriate docker action based on the parsed arguments."""
        logger.debug(f"Running DockerCommand with args: {args}")
        action_method = getattr(self, args.action, None)
        if action_method:
            action_method()
        else:
            logger.error(f"Unknown action: {args.action}")

    def rebuild(self) -> None:
        """Rebuild the core repository."""
        os.chdir(CORE_DIR)
        run_command("git pull --rebase")
        print("Rebuilding all components")
        run_command("yarn")
        run_command("yarn build")
