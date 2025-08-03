import telebot
import logging
from typing import Dict

logger = logging.getLogger(__name__)

class PortCheckr:
    def __init__(self, config: Dict[str, str]):
        self.bot = telebot.TeleBot(config['API_TOKEN'])
        self.chat_id = config['CHAT_ID']
        self.host = config['HOST']
        self.port = config['PORT']
        self.host_name = config['HOST_NAME']
        self.service_name = config['SERVICE_NAME']
        self.notification_timeout_minutes = config['NOTIFICATION_TIMEOUT_MINUTES']
    
    # Function for send pushes
    def send_notification(self, message: str):
        try:
            self.bot.send_message(self.chat_id, message)
            logger.info(f"Notification sent: {message}")
        except Exception as e:
            logger.error(f"Send error: {e}")
