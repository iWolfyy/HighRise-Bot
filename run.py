from flask import Flask
from threading import Thread
from highrise.__main__ import *
from config import BOT_ID, ROOM_ID, BOT_UID
import random
import time
import traceback
from importlib import import_module

class WebServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.port = random.randint(8000, 9000)  # 🎯 Random available port

        @self.app.route('/')
        def index() -> str:
            return f"Alive on port {self.port}"

    def run(self) -> None:
        # Suppress Flask logging to keep console clean
        import logging
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        
        print(f"🌐 WebServer running on port {self.port}")
        self.app.run(host='0.0.0.0', port=self.port)

    def keep_alive(self):
        t = Thread(target=self.run)
        t.daemon = True
        t.start()

class RunBot:
    room_id = ROOM_ID
    bot_token = BOT_ID
    bot_file = "main"
    bot_class = "Bot"

    def __init__(self) -> None:
        try:
            bot_module = import_module(self.bot_file)
            bot_instance = getattr(bot_module, self.bot_class)()
            self.definitions = [
                BotDefinition(bot_instance, self.room_id, self.bot_token)
            ]
        except Exception as e:
            print(f"❌ Error loading bot class: {e}")
            raise e

    def run_loop(self) -> None:
        print("🚀 Starting Bot Loop...")
        while True:
            try:
                # Attempt to run the Highrise bot
                arun(main(self.definitions))
            except Exception as e:
                error_str = str(e)
                print("\n--- [BOT CRASHED] ---")
                
                # Check for DNS/Internet failure (The error you provided)
                if "Temporary failure in name resolution" in error_str or "gaierror" in error_str:
                    print("📡 NETWORK ERROR: Server cannot find the internet (DNS failure).")
                    print("Retrying in 30 seconds... (Check your hosting provider if this persists)")
                    time.sleep(30)
                
                # Check for rate limits or session errors
                elif "429" in error_str:
                    print("⏳ RATE LIMITED: Highrise is blocking connections temporarily.")
                    print("Waiting 60 seconds before retrying...")
                    time.sleep(60)
                
                else:
                    print("⚠️ GENERAL ERROR DETECTED:")
                    traceback.print_exc()
                    print("Restarting in 5 seconds...")
                    time.sleep(5)
                
                print("🔄 Attempting to reconnect...\n")
                continue

if __name__ == "__main__":
    # 1. Start Web Server (for UptimeRobot/Keep-Alive)
    WebServer().keep_alive()
    
    # 2. Start the Bot
    bot_runner = RunBot()
    bot_runner.run_loop()