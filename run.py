from flask import Flask
from threading import Thread
from highrise.__main__ import *
from config import BOT_ID, ROOM_ID, BOT_UID
import random
import time
import traceback
import logging
from importlib import import_module

class WebServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.port = random.randint(8000, 9000)

        @self.app.route('/')
        def index() -> str:
            return f"Alive on port {self.port}"

    def run(self) -> None:
        # Heavily suppress Flask logging to save CPU/IO
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        
        print(f"🌐 WebServer running on port {self.port}")
        # Use threaded=True to handle requests efficiently
        self.app.run(host='0.0.0.0', port=self.port, debug=False, use_reloader=False)

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
                
                # Check for DNS/Internet failure
                if "Temporary failure in name resolution" in error_str or "gaierror" in error_str:
                    print("📡 NETWORK ERROR: DNS failure. Waiting 60s...")
                    time.sleep(60) # Increased to save CPU
                
                # Check for rate limits
                elif "429" in error_str:
                    print("⏳ RATE LIMITED: Waiting 90s...")
                    time.sleep(90) # Increased to satisfy hosting limits
                
                # Catch-all for any other error (CRITICAL for CPU protection)
                else:
                    print(f"⚠️ GENERAL ERROR: {error_str}")
                    # NEVER set this lower than 20-30 seconds on free hosting
                    print("Restarting in 30 seconds to prevent CPU spike...")
                    time.sleep(30) 
                
                print("🔄 Attempting to reconnect...\n")

if __name__ == "__main__":
    # 1. Start Web Server
    WebServer().keep_alive()
    
    # 2. Start the Bot
    try:
        bot_runner = RunBot()
        bot_runner.run_loop()
    except KeyboardInterrupt:
        print("Stopping bot...")