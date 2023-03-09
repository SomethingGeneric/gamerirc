import asyncio, threading, os, re
import binascii

bp = f"/gb-data/no_bash.txt"

dont = ["dd", "fallocate", "doas", "pkexec", "truncate"]


def reload_ignore():
    if os.path.exists(bp):
        ignore = []
        ids = []
        with open(bp) as f:
            ids = f.read().split("\n")
        for nid in ids:
            ignore.append(nid)


ignore = []
reload_ignore()


async def paste(text):
    paste_fn = "." + str(binascii.b2a_hex(os.urandom(15)).decode("utf-8"))
    with open(paste_fn, "w") as f:
        f.write(text)
    link = await run_command_shell(f"cat {paste_fn} | nc termbin.com 9999")
    os.remove(paste_fn)
    return link.strip()


async def pastef(fn):
    link = await run_command_shell(f"cat {fn} | nc termbin.com 9999")
    return link.strip()


async def run_command_shell(command, grc=False):
    """Run command in subprocess (shell)."""

    kill = lambda proc: proc.kill()
    # Create subprocess
    process = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    # Status
    print("Started:", command, "(pid = " + str(process.pid) + ")", flush=True)

    kill_timer = threading.Timer(60, kill, [process])

    try:
        # Wait for the subprocess to finish
        kill_timer.start()
        stdout, stderr = await process.communicate()
    except:
        kill_timer.cancel()

    # Progress
    if process.returncode == 0:
        print("Done:", command, "(pid = " + str(process.pid) + ")", flush=True)
        # Result
        result = stdout.decode().strip()
    else:
        print("Failed:", command, "(pid = " + str(process.pid) + ")", flush=True)
        # Result
        result = stderr.decode().strip()

    kill_timer.cancel()

    if not grc:
        # Return stdout
        return result.strip().rstrip()
    else:
        return process.returncode, result.strip().rstrip()


def write_ignore(uid):
    with open(bp, "a+") as f:
        f.write(str(uid) + "\n")
    reload_ignore()


def remove_ignore(uid):
    ignore.remove(uid)
    with open(bp, "w") as f:
        f.write("\n".join(ignore))
    reload_ignore()


async def doshell(user, cmd):
    rval = ""

    if " " in cmd:
        if cmd.split(" ")[0] in dont:
            rval = f"Do not `{cmd.split(' ')[0]}`"
            return rval
    elif cmd in dont:
        rval = f"Do not `{cmd}`"
        return rval

    if user in ignore:
        rval = "No more bash for you"
        return rval

    if ":(){ :|:& };:" in cmd or re.search(r"(.)\|\1&", cmd):
        rval = "No forkbombs"
        write_ignore(user)
        return rval

    un = user if user != "root" else "not_root"

    await run_command_shell("scp /bot/bin/has_user punchingbag:.")
    test_user = await run_command_shell(f"ssh punchingbag './has_user {un}'")

    if "n" in test_user:  # no user
        await run_command_shell("scp /bot/bin/mk_user punchingbag:.")
        await run_command_shell(f"ssh punchingbag './mk_user {un}'")

    temp_script_fn = "." + str(binascii.b2a_hex(os.urandom(15)).decode("utf-8"))

    with open(temp_script_fn, "w") as f:
        f.write(f"#!/usr/bin/env bash\n{cmd}")

    await run_command_shell(f"scp {temp_script_fn} {un}@punchingbag:.")

    await run_command_shell(f"ssh {un}@punchingbag 'chmod +x {temp_script_fn}'")

    output = await run_command_shell(f"ssh {un}@punchingbag './{temp_script_fn}'")

    await run_command_shell(f"ssh {un}@punchingbag 'rm {temp_script_fn}'")

    msg = ""

    if len(output) > (999 - len(cmd)):
        link = await paste(f"Command was: '{cmd}', output:\n{output}")
        msg = f"See output: {link}"
    else:
        if len(output) != 0:
            msg = f"Command `{cmd}`, output: \n----\n{output}\n----"
        else:
            msg = f"Command: `{cmd}`, but no output was returned"

    return msg
