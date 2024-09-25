import argparse
import os
from ldo.main import BaseCommand
from ldo.utils import run_command
from ldo.constants import DOCKER_COMPOSE_DIR
import logging

logger = logging.getLogger(__name__)


class VaultCommand(BaseCommand):
    def register(self, subparser: argparse.ArgumentParser) -> None:
        """Register the docker command and its subcommands."""
        logger.debug("Registering VaultCommand")
        action_subparsers = subparser.add_subparsers(dest="action", required=True)
        action_subparsers.add_parser(
            "unseal", help="Start Docker without any container argument"
        )

    def run(self, args: argparse.Namespace) -> None:
        """Run the appropriate docker action based on the parsed arguments."""
        logger.debug(f"Running VaultCommand with args: {args}")
        action_method = getattr(self, args.action, None)
        if action_method:
            action_method()
        else:
            logger.error(f"Unknown action: {args.action}")

    def unseal(self, *containers: list[str] | None) -> None:
        os.chdir(DOCKER_COMPOSE_DIR)
        run_command("./vault/vault.sh unseal")
