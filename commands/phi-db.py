import os
import argparse
from ldo.main import BaseCommand
from ldo.utils import run_command
from ldo.constants import DOCKER_COMPOSE_DIR

class PHIDBCommand(BaseCommand):
    def register(self, subparser: argparse.ArgumentParser) -> None:
        """Register the core command and its subcommands."""
        action_subparsers = subparser.add_subparsers(dest="action", required=True)

        action_parser = action_subparsers.add_parser(
            "migrate",
            help="Run migrations to PHI DB"
        )
        action_parser.add_argument(
          "service",  choices=["form", "patient"], nargs="?", help="Service names using PHI DB"
        )


    def run(self, args: argparse.Namespace) -> None:
        """Run the appropriate core action based on the parsed arguments."""
        if args.action == "migrate":
          if args.service[0] is None:
            print(f"Unknown or empty service. Migration will run for both services.")
          
          self.client_migrate(args.service[0])
        else:
            print(f"Unknown action: {args.action}")

    def migrate(self, service) -> None:
        os.chdir(DOCKER_COMPOSE_DIR)

        if service == "form":
          docker_command = "docker-compose exec -T phidb bash -c 'yarn form:migrate'"
        elif service == "patient":
          docker_command = "docker-compose exec -T phidb bash -c 'yarn patient:migrate'"
        else:
          docker_command = "docker-compose exec -T phidb bash -c 'yarn form:migrate && yarn patient:migrate'"

        run_command(docker_command)
