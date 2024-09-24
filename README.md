# LDO (Local Development Operations) Utility

LDO is a command-line interface (CLI) tool designed to streamline and standardize local development operations. It provides a flexible and extensible framework for managing various development tasks, such as Docker operations and repository management.

## Installation

*It is assumed that this repo will be in the same directory as all the other Laudio repos*

1. Clone the repository:
   ```
   git clone https://github.com/nsmith-laudio/ldo.git
   cd ldo
   ```

2. Ensure you have Python 3.x installed.

3. Make the main script executable:
   ```
   chmod +x ldo
   ```

## Usage

It is preferred to put this script in your `$PATH` so you can run it from anywhere

The general syntax for using LDO is:

```
./ldo <command> <action> [arguments]
```

For example:

```
./ldo docker up container1 container2
./ldo core rebuild
```

To see available commands:

```
./ldo
```

To see available actions for a specific command:

```
./ldo docker
```

## Available Commands

### DB

Manage Docker containers:

- `client-migrate`: Runs `yarn client:migrate` && `yarn client:sync`

Example:
```
./ldo db client-migrate
```

### Docker

Manage Docker containers:

- `up`: Bring up Docker containers
- `down`: Bring down Docker containers
- `restart`: Restart Docker containers
- `start`: Start all Docker containers in the proper order (ensuring we unseal the vault as well)

Example:
```
./ldo docker up mysql redis
```

```
./ldo docker up vault # Also unseals the vault
```

### Core

Manage the core repository:

- `rebuild`: Pull and rebuild the core repository

Example:
```
./ldo core rebuild
```

## Extending LDO

To add a new command:

1. Create a new Python file in the `commands/` directory (e.g., `commands/new_command.py`).
2. Define a class that inherits from `BaseCommand`.
3. Implement the `register` and `run` methods.

Example:

```python
from base_command import BaseCommand
import argparse

class NewCommand(BaseCommand):
    def register(self, subparser: argparse.ArgumentParser) -> None:
        subparser.add_argument("action", choices=["action1", "action2"], help="Action to perform")
        subparser.add_argument("args", nargs="*", help="Additional arguments")

    def run(self, args: argparse.Namespace) -> None:
        if args.action == "action1":
            self.action1(args.args)
        elif args.action == "action2":
            self.action2(args.args)

    def action1(self, args):
        print(f"Performing action1 with args: {args}")

    def action2(self, args):
        print(f"Performing action2 with args: {args}")
```

The new command will be automatically discovered and added to the CLI.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](LICENSE)
