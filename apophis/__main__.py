import core.client


def start_bot():
    bot = core.client.Bot()
    bot.run('TOKEN')


if __name__ == "__main__":
    start_bot()