import argparse
from ldo.main import BaseCommand
from ldo.utils import run_command
from ldo.constants import DOCKER_COMPOSE_DIR
import os


class DBCommand(BaseCommand):
    def register(self, subparser: argparse.ArgumentParser) -> None:
        """Register the core command and its subcommands."""
        action_subparsers = subparser.add_subparsers(dest="action", required=True)

        # Register 'rebuild' action
        action_subparsers.add_parser(
            "client-migrate",
            help="Run client schema migrations and synchronize across all client DBs",
        )

    def run(self, args: argparse.Namespace) -> None:
        """Run the appropriate core action based on the parsed arguments."""
        if args.action == "client-migrate":
            self.client_migrate()
        else:
            print(f"Unknown action: {args.action}")

    def client_migrate(self) -> None:
        os.chdir(DOCKER_COMPOSE_DIR)
        docker_command = "docker-compose exec -T db bash -c 'yarn client:migrate && yarn client:sync'"
        run_command(docker_command)
