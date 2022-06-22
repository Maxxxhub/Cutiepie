from EmikoRobot import (
    dispatchar
)
__help__ = """
➻ /antiservice <on / off>
Note: If on, The bot will auto delete service messages for ex: user joined , user left etc...
"""

CLEAN_SERVICE_HANDLER = CommandHandler(
    "cleanservice", cleanservice, filters=Filters.chat_type.groups, run_async=True
  
  
  dispatcher.add_handler(CLEAN_SERVICE_HANDLER)
  
  __mod_name__ = "A-sᴇʀᴠɪᴄᴇ"
  __command_list__ = []
  __handlers__ = [
    CLEAN_SERVICE_HANDLER
  ]
