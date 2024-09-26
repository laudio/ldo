import argparse
import os
import re
from ldo.main import BaseCommand
from ldo.utils import run_command, copy_file
from ldo.constants import DOCKER_COMPOSE_DIR

# from ldo.commands.docker import DockerCommand
import logging

logger = logging.getLogger(__name__)


class VaultCommand(BaseCommand):
    VAULT_SCRIPT = "./vault/vault.sh"

    def register(self, subparser: argparse.ArgumentParser) -> None:
        """Register the docker command and its subcommands."""
        logger.debug("Registering VaultCommand")
        action_subparsers = subparser.add_subparsers(dest="action", required=True)
        action_subparsers.add_parser(
            "setup", help="Setups a vault if one doesn't exist"
        )
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

    def unseal(self) -> None:
        os.chdir(DOCKER_COMPOSE_DIR)
        run_command(f"{self.VAULT_SCRIPT} unseal")

    def setup(self) -> None:
        if os.path.exists(os.path.join(DOCKER_COMPOSE_DIR, "vault", "file")):
            logger.info("Vault already setup...")
            return

        docker = DockerCommand()
        vault_config_source = os.path.join(
            DOCKER_COMPOSE_DIR, "vault", "config.json.example"
        )
        vault_config_dest = os.path.join(DOCKER_COMPOSE_DIR, "vault", "config.json")
        copy_file(vault_config_source, vault_config_dest)

        os.chdir(DOCKER_COMPOSE_DIR)
        docker.run("vault")

        try:
            output = run_command(f"{self.VAULT_SCRIPT} init", silent=True)
            vault_token = self.extract_root_token(output)
            if vault_token:
                logger.info(f"Vault token: {vault_token}")
                env_file = os.path.join(DOCKER_COMPOSE_DIR, ".env")
                self.utils.update_file(env_file, "LOCAL_VAULT_TOKEN", vault_token)
                logger.info("Vault initialized successfully.")
            else:
                logger.error("Error: Root token not found in output")
            logger.info("Vault setup completed successfully.")
        except Exception as e:
            logger.error(f"An error occurred while running vault.sh: {str(e)}")

    def extract_root_token(self, output):
        # Using regex to find the root token
        lines = output.split("\n")
        for line in lines:
            match = re.search(r"^token\s+(.*)", line)
            if match:
                return match.group(1)

        return None
