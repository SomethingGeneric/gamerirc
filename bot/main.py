# System
import subprocess, os

# Pip
import pydle
import duckduckgo

# Me
from util import doshell

admins = ["ratthew"]
channels = ["##gamerthebot", "##gamerthebot-schizo", "##gamerthebot-flood"]


class MyOwnBot(pydle.Client):
    async def on_connect(self):
        for chan in channels:
            await self.join(chan)

    async def on_message(self, target, source, message):
        # don't respond to our own messages, as this leads to a positive feedback loop
        if source != self.nickname:
            try:
                # await self.message(target, f"{source}: {message}")
                if (
                    source in admins
                    and "die" in message
                    and (self.nickname in message or message[0] == "$")
                ):
                    await self.message(target, "RIP me. Shutting down.")
                    await self.disconnect()
                elif (
                    self.nickname in message or message[0] == "$"
                ) and "stats" in message:
                    print("Lol if only i was smart")
                    await self.message(target, f"{source}: Haha someday")
                    return
                elif (
                    self.nickname in message or message[0] == "$"
                ) and "help" in message:
                    await self.message(
                        target,
                        f"{source}: I'll get around to a help command at some point.",
                    )
                    return
                elif (
                    self.nickname in message or message[0] == "$"
                ) and "kernel" in message:
                    mine = subprocess.check_output(["uname", "-r"]).decode().strip()
                    await self.message(target, f"{source}: I have version {mine}.")
                    return
                elif (
                    self.nickname in message or message[0] == "$"
                ) and "duck" in message:
                    query = (
                        message.replace(f"{self.nickname}:", "")
                        .replace(f"{self.nickname},", "")
                        .replace("duck: ", "")
                        .replace("duck, ", "")
                        .replace("duck", "")
                        .replace("$", "")
                    )
                    await self.message(
                        target, f"{source}: results: '{duckduckgo.get_zci(query)}'."
                    )
                    return
                elif message[0] == "$" or (
                    self.nickname in message and "shell: " in message
                ):
                    cmd = (
                        message.replace(self.nickname + ": shell: ", "")
                        .replace("rm", "")
                        .replace("mv", "")
                        .replace("'", "")
                        .replace('"', "")
                    )
                    # await self.message(target, f"{source}, running {cmd}.")
                    res = await doshell(source, cmd)
                    await self.message(target, f"{source}: Result: '{res}'")
                    return
            except Exception as e:
                await self.message(target, f"{source}: Error: '{str(e)}'")


client = MyOwnBot("gamerbot", realname="Gamer The Bot")
client.run("tungsten.libera.chat", tls=True, tls_verify=False)
