import argparse
from ldo.main import BaseCommand
from ldo.utils import run_command
from ldo.constants import CORE_DIR
import os


class CoreCommand(BaseCommand):
    def register(self, subparser: argparse.ArgumentParser) -> None:
        """Register the core command and its subcommands."""
        action_subparsers = subparser.add_subparsers(dest="action", required=True)

        # Register 'rebuild' action
        rebuild_parser = action_subparsers.add_parser(
            "rebuild", help="Rebuild the core repository"
        )
        rebuild_parser.add_argument(
            "components", nargs="*", help="Optional components to rebuild"
        )

    def run(self, args: argparse.Namespace) -> None:
        """Run the appropriate core action based on the parsed arguments."""
        if args.action == "rebuild":
            self.rebuild(args.components)
        else:
            print(f"Unknown action: {args.action}")

    def rebuild(self) -> None:
        """Rebuild the core repository."""
        os.chdir(CORE_DIR)
        run_command("git pull --rebase")
        print("Rebuilding all components")
        run_command("yarn && yarn build")
