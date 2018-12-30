import sys
import core.client


def start_cli():
    if len(sys.argv) == 3:
        cli = core.client.BotClient()
        cli.run(sys.argv[2])
    else:
        print("To start bot a token is required.")


if __name__ == "__main__":
    start_cli()