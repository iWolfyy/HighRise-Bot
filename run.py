from flask import Flask
from threading import Thread
from highrise.__main__ import *
from config import BOT_ID, ROOM_ID, BOT_UID
import random
import time
import traceback
import logging
from importlib import import_module
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

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
        
        logging.info(f"🌐 WebServer running on port {self.port}")
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
            logging.error(f"❌ Error loading bot class: {e}")
            raise e

    def run_loop(self) -> None:
        logging.info("🚀 Starting Bot Loop...")
        while True:
            try:
                # Attempt to run the Highrise bot
                arun(main(self.definitions))
            except Exception as e:
                error_str = str(e)
                logging.error(f"\n--- [BOT CRASHED] ---")
                logging.error(f"Error details: {error_str}")
                
                # Check for DNS/Internet failure
                if "Temporary failure in name resolution" in error_str or "gaierror" in error_str:
                    logging.warning("📡 NETWORK ERROR: DNS failure. Waiting 60s...")
                    time.sleep(60) # Increased to save CPU
                
                # Check for rate limits
                elif "429" in error_str:
                    logging.warning("⏳ RATE LIMITED: Waiting 90s...")
                    time.sleep(90) # Increased to satisfy hosting limits
                
                # Catch-all for any other error (CRITICAL for CPU protection)
                else:
                    logging.error(f"⚠️ GENERAL ERROR: {error_str}")
                    # NEVER set this lower than 20-30 seconds on free hosting
                    logging.info("Restarting in 30 seconds to prevent CPU spike...")
                    time.sleep(30) 
                
                logging.info("🔄 Attempting to reconnect...\n")

if __name__ == "__main__":
    # 1. Start Web Server
    try:
        WebServer().keep_alive()
    except Exception as e:
        logging.error(f"Failed to start web server: {e}")
    
    # 2. Start the Bot
    try:
        bot_runner = RunBot()
        bot_runner.run_loop()
    except KeyboardInterrupt:
        logging.info("Stopping bot...")
    except Exception as e:
        logging.critical(f"Fatal error in main loop: {e}")