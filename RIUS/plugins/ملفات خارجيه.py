import os
from pathlib import Path

from telethon.tl.types import InputMessagesFilterDocument

from ..Config import Config
from ..helpers.utils import install_pip
from ..utils import load_module
from . import BOTLOG, BOTLOG_CHATID, Aio8

plugin_category = "tools"

if Config.PLUGIN_CHANNEL:

    async def install():
        documentss = await Aio8.get_messages(
            Config.PLUGIN_CHANNEL, None, filter=InputMessagesFilterDocument
        )
        total = int(documentss.total)
        for module in range(total):
            plugin_to_install = documentss[module].id
            plugin_name = documentss[module].file.name
            if os.path.exists(f"RIUS/plugins/{plugin_name}"):
                return
            downloaded_file_name = await Aio8.download_media(
                await Aio8.get_messages(Config.PLUGIN_CHANNEL, ids=plugin_to_install),
                "RIUS/plugins/",
            )
            path1 = Path(downloaded_file_name)
            shortname = path1.stem
            flag = True
            check = 0
            while flag:
                try:
                    load_module(shortname.replace(".py", ""))
                    break
                except ModuleNotFoundError as e:
                    install_pip(e.name)
                    check += 1
                    if check > 5:
                        break
            if BOTLOG:
                await Aio8.send_message(
                    BOTLOG_CHATID,
                    f"᯽︙ تـم تـنصـيب المـلف `{os.path.basename(downloaded_file_name)}` بـناجح ✅.",
                )

    Aio8.loop.create_task(install())
