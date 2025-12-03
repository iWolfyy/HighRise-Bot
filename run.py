from flask import Flask
from threading import Thread
from highrise.__main__ import *
from config import BOT_ID, ROOM_ID, BOT_UID
import random
import time
from importlib import import_module


class WebServer:

  def __init__(self):
    self.app = Flask(__name__)
    self.port = random.randint(8000, 9000)  # 🎯 Random available port

    @self.app.route('/')
    def index() -> str:
      return f"Alive on port {self.port}"  # Optional: show port

  def run(self) -> None:
    print(f"🌐 WebServer running on port {self.port}")
    self.app.run(host='0.0.0.0', port=self.port)

  def keep_alive(self):
    t = Thread(target=self.run)
    t.daemon = True  # Optional: auto-kill thread on exit
    t.start()


class RunBot:
  room_id = ROOM_ID
  bot_token = BOT_ID
  bot_file = "main"
  bot_class = "Bot"

  def __init__(self) -> None:
    self.definitions = [
        BotDefinition(
            getattr(import_module(self.bot_file), self.bot_class)(),
            self.room_id, self.bot_token)
    ]

  def run_loop(self) -> None:
    while True:
      try:
        arun(main(self.definitions))
      except Exception as e:
        import traceback
        print("Caught an exception:")
        traceback.print_exc()
        time.sleep(1)
        continue


if __name__ == "__main__":
  WebServer().keep_alive()
  RunBot().run_loop()
