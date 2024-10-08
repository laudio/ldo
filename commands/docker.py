import argparse
import os
import time
from ldo.main import BaseCommand
from ldo.utils import run_command
from ldo.constants import DOCKER_COMPOSE_DIR
import logging

logger = logging.getLogger(__name__)


class DockerCommand(BaseCommand):
    def register(self, subparser: argparse.ArgumentParser) -> None:
        """Register the docker command and its subcommands."""
        logger.debug("Registering DockerCommand")
        action_subparsers = subparser.add_subparsers(dest="action", required=True)
        for action in ["up", "down", "restart"]:
            action_parser = action_subparsers.add_parser(
                action, help=f"Bring Docker container(s) {action}"
            )
            action_parser.add_argument(
                "containers", nargs="*", help="Optional container names"
            )
        action_subparsers.add_parser(
            "start", help="Start Docker without any container argument"
        )

    def run(self, args: argparse.Namespace) -> None:
        """Run the appropriate docker action based on the parsed arguments."""
        logger.debug(f"Running DockerCommand with args: {args}")
        action_method = getattr(self, args.action, None)
        if action_method:
            action_method(args.containers if hasattr(args, "containers") else None)
        else:
            logger.error(f"Unknown action: {args.action}")

    def up(self, *containers: list[str] | None) -> None:
        self._docker_compose_action("up -d", *containers)
        if containers and containers[0] and "vault" in containers[0]:
            # Wait for the container to start
            time.sleep(2)
            run_command("./vault/vault.sh unseal")

    def down(self, *containers: list[str] | None) -> None:
        self._docker_compose_action("down", *containers or [])

    def restart(self, *containers: list[str] | None) -> None:
        self._docker_compose_action("restart", *containers or [])
        if containers and containers[0] and "vault" in containers[0]:
            # Wait for the container to start
            time.sleep(2)
            run_command("./vault/vault.sh unseal")

    def start(self, _) -> None:
        self.up(["vault"])
        self.up(["mssql", "redis"])
        self.up([])

    def _docker_compose_action(self, action: str, containers: list[str] | None) -> None:
        container_str = " ".join(containers or [])
        print(
            f"{action.capitalize()}ing {container_str if container_str else 'all containers'}..."
        )
        os.chdir(DOCKER_COMPOSE_DIR)
        run_command(f"docker-compose {action} {container_str}")
