import argparse
import os
from ldo.main import BaseCommand
from ldo.utils import run_command, copy_file
from ldo.constants import LISS_DIR

# from ldo.commands.docker import DockerCommand
import logging

logger = logging.getLogger(__name__)


class LissCommand(BaseCommand):
    def register(self, subparser: argparse.ArgumentParser) -> None:
        """Register the docker command and its subcommands."""
        logger.debug("Registering LissCommand")
        action_subparsers = subparser.add_subparsers(dest="action", required=True)
        action_subparsers.add_parser("setup", help="Setups LISS database")

    def run(self, args: argparse.Namespace) -> None:
        """Run the appropriate core action based on the parsed arguments."""
        action_method = getattr(self, args.action, None)
        if action_method:
            action_method()
        else:
            print(f"Unknown action: {args.action}")

    def setup(self) -> None:
        """Rebuild the core repository."""
        liss_db = os.path.join(LISS_DIR, "db/insights")
        os.chdir(liss_db)

        if os.path.exists(os.path.join(liss_db, ".env")):
            logger.info(".env already exists, not copying...")
        else:
            env_source = os.path.join(liss_db, ".env.example")
            env_dest = os.path.join(liss_db, ".env")
            copy_file(env_source, env_dest)

        run_command("yarn")
        run_command("yarn build")
        run_command("yarn indb:create --clientIdentifier=client1")
