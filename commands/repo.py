import argparse
import os
from ldo.main import BaseCommand
from ldo.utils import run_command
import ldo.constants as CONSTANTS
import logging

logger = logging.getLogger(__name__)


class RepoCommand(BaseCommand):
    def register(self, subparser: argparse.ArgumentParser) -> None:
        """Register the core command and its subcommands."""
        action_subparsers = subparser.add_subparsers(dest="action", required=True)

        # Register 'rebuild' action
        self.rebuild_parser = action_subparsers.add_parser(
            "update", help="Update git repos"
        )

        self.rebuild_parser.add_argument(
            dest="repos",
            nargs="*",
            help="Specify one or more repo names: 'all', 'backend', 'core', 'db', 'docker', 'liss', 'scripts'",
            metavar="repo_names",
        )

    def run(self, args: argparse.Namespace) -> None:
        """Run the appropriate docker action based on the parsed arguments."""
        if args.repos:
            self.update_repo(args.repos)
        else:
            self.rebuild_parser.error("Please specify one or more repo names to update")

    def update_repo(self, repos):
        if "backend" in repos or "all" in repos:
            logger.info("Updating backend repo")
            os.chdir(CONSTANTS.BACKEND_DIR)
            run_command("git pull --rebase")
            pass

        if "core" in repos or "all" in repos:
            os.chdir(CONSTANTS.CORE_DIR)
            logger.info("Updating core repo")
            run_command("git pull --rebase")

        if "db" in repos or "all" in repos:
            os.chdir(CONSTANTS.DB_DIR)
            logger.info("Updating db repo")
            run_command("git pull --rebase")
            pass

        if "docker" in repos or "all" in repos:
            os.chdir(CONSTANTS.DOCKER_DIR)
            logger.info("Updating docker repo")
            run_command("git pull --rebase")
            pass

        if "liss" in repos or "all" in repos:
            os.chdir(CONSTANTS.LISS_DIR)
            logger.info("Updating liss repo")
            run_command("git pull --rebase")
            pass

        if "scripts" in repos or "all" in repos:
            os.chdir(CONSTANTS.SCRIPTS_DIR)
            logger.info("Updating laudio-scripts repo")
            run_command("git pull --rebase")
            pass
