from datetime import datetime

from cmds.command import Command

usage = """Usage:
```
!insult
!insult @someone [@somebody]
!insult add a new insult
!insult del <integer>
```"""
limit = 500  # Not more than 500 characters insult


async def add_insult(context, insult, author):
    epoch = datetime.strftime(datetime.now(), "%s")

    statement = """
    insert into insults (
        insult,
        author,
        added_on
    ) values ($1, $2, $3) returning id;
    """

    return await context["db"].fetchval(
        statement, insult, str(author), str(epoch)
    )


async def fetch_random_insult(context):
    statement = """
    select insult from insults
    offset floor(random() * (select count(*) from insults)) limit 1;
    """
    return await context["db"].fetchval(statement)


async def delete_insult(context, identifier):
    statement = "delete from insults where id = $1"
    return await context["db"].execute(statement, identifier)


class InsultCommand(Command):
    async def handle(self, context, message) -> str:

        splitted = message.content.split()
        author = message.author.id

        mentioned = " ".join(["<@{}>".format(m.id) for m in message.mentions])

        # Case when only "!insult" is invoked
        if len(splitted) == 1:
            line = await fetch_random_insult(context)
            if not line:
                msg = "<@{}>, I won't do what you tell me!".format(author)
                return await message.channel.send(msg)

            return await message.channel.send(line)

        # Stopping users from getting spammed
        if "@here" in " ".join(splitted[1:]) or "@everyone" in " ".join(
            splitted[1:]
        ):
            msg = "<@{}>, thou shall not spam the server!".format(author)
            return await message.channel.send(msg)

        # When some extra parameter is passed with "!insult"
        # !insult @someone
        # !insult add
        # !insult del
        # !insult add "quote"
        # !insult del <id>
        action = splitted[1]
        remainder = splitted[2:]  # see if there's more message after action

        # Cases for !insult @someone and similar
        if action.lower() not in ("add", "del"):
            if not mentioned:
                msg = "<@{}>, invalid action '{}', usage is: {}".format(
                    author, action, usage
                )
                return await message.channel.send(msg)

            line = await fetch_random_insult(context)
            if not line:
                msg = "<@{}>, I won't do what you tell me!".format(author)
                return await message.channel.send(msg)

            msg = "{}, {}".format(mentioned, line)
            return await message.channel.send(msg)

        # User has not specified parameters
        if not remainder:
            msg = "<@{}>, insufficient parameters! {}".format(author, usage)
            return await message.channel.send(msg)

        if action.lower() == "add":
            insult = " ".join(remainder)
            if len(insult) > limit:
                msg = (
                    "It's supposed to be an insult <@{}>, not copypasta!"
                ).format(author)
                return await message.channel.send(msg)

            insult_id = await add_insult(context, insult, author)
            msg = "<@{}>, added current insult as **insult #{}**!".format(
                author, insult_id
            )
            return await message.channel.send(msg)

        # Only action that is left is delete, process it
        identifier = remainder[0]
        try:
            identifier = int(identifier)  # id is int in DB
        except ValueError:
            msg = "<@{}>, insult id should be an integer".format(
                author, identifier
            )
        else:
            status = await delete_insult(context, identifier)
            # TODO: This might fail, not now but later on
            deleted_rows = int(status.lower().replace("delete ", ""))

            msg = "<@{}>, **insult #{}** does not exist!".format(
                author, identifier
            )
            if deleted_rows > 0:
                msg = "<@{}>, **insult #{}** has been deleted!".format(
                    author, identifier
                )
        return await message.channel.send(msg)
