import argparse
from ldo.main import BaseCommand
from ldo.utils import run_command
from ldo.constants import DOCKER_COMPOSE_DIR
import os


class DBCommand(BaseCommand):
    def register(self, subparser: argparse.ArgumentParser) -> None:
        """Register the core command and its subcommands."""
        action_subparsers = subparser.add_subparsers(dest="action", required=True)

        # Register 'migrate' action
        migrate_parser = action_subparsers.add_parser(
            "migrate",
            help="Run migration and synchronize across DBs",
        )

        # Add subparser for 'client' or 'common' argument
        migrate_subparsers = migrate_parser.add_subparsers(
            dest="migrate_type", required=True
        )

        migrate_subparsers.add_parser("client", help="Run client-specific migration")
        migrate_subparsers.add_parser("common", help="Run common migration")

    def run(self, args: argparse.Namespace) -> None:
        """Run the appropriate core action based on the parsed arguments."""
        if args.action == "migrate" and args.migrate_type:
            self.migrate(args.migrate_type)
        else:
            print(f"Unknown action: {args.action}")

    def migrate(self, migration_type) -> None:
        os.chdir(DOCKER_COMPOSE_DIR)
        docker_command = (
            f"docker-compose exec -T db bash -c 'yarn {migration_type}:sync'"
        )
        run_command(docker_command)
