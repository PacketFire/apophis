import sys
import core.client


def start_bot():
    if len(sys.argv) == 3:
        bot = core.client.Bot()
        bot.run(sys.argv[2])
    else:
        print("To start bot a token is required.")


if __name__ == "__main__":
    start_bot()