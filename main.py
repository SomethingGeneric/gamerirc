import pydle

# Simple echo bot.
class MyOwnBot(pydle.Client):
    async def on_connect(self):
         await self.join('#bottest')

    async def on_message(self, target, source, message):
         # don't respond to our own messages, as this leads to a positive feedback loop
         if source != self.nickname:
            await self.message(target, message)

client = MyOwnBot('gamerbot', realname='GamerTheBot')
client.run('xhec.dev', tls=False, tls_verify=False)