import pydle,asyncio

class MyClient(pydle.Client):
    """ This is a simple bot that will greet people as they join the channel. """

    async def on_connect(self):
        await super().on_connect()
        # Can't greet many people without joining a channel.
        await self.join('#kochira')

    async def on_join(self, channel, user):
        await super().on_join(channel, user)
        await self.message(channel, 'Hey there, {user}!', user=user)

async def main():
    client = MyClient('gamerbot')
    await client.connect('xhec.dev')
    await client.handle_forever()

if __name__ == "__main__":
    asyncio.run(main())