import subprocess
import time
import logging
from typing import Dict
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class PortMonitor:
    def __init__(self, config: Dict[str, str]):
        self.host = config['HOST']
        self.port = config['PORT']
        self.host_name = config['HOST_NAME']
        self.service_name = config['SERVICE_NAME']
        self.notification_timeout = int(config['NOTIFICATION_TIMEOUT_MINUTES'])
        self.notifications_paused_until = None
        self.last_status = None
        self.first_check = True
        self.consecutive_failures = 0

    # Function for port checking
    def check_port(self):
        try:
            result = subprocess.run(
                ["nc", "-zv", self.host, str(self.port)],
                capture_output=True,
                text=True,
                timeout=5
            )
            is_open = result.returncode == 0
            status = "open" if is_open else "closed"
            
            # Logging result of port check
            logger.debug(
                f"[{time.strftime('%Y-%m-%d %H:%M:%S %Z')}] "
                f"UDP port {self.port} on {self.host} {status}, "
                f"return code: {result.returncode}, "
                f"output: {result.stderr.strip() or result.stdout.strip()}"
            )
            return is_open

        except subprocess.TimeoutExpired:
            logger.error(f"Timeout checking port {self.host}:{self.port}")
            return False
        except Exception as e:
            logger.error(f"Error checking port {self.host}:{self.port}: {e}")
            return False

    def start_monitoring(self, callback):
        while True:
            current_status = self.check_port()
            
            # Check unreachables
            if not current_status:
                self.consecutive_failures += 1
            else:
                self.consecutive_failures = 0
                self.notifications_paused_until = None
            
            # If unreachables more, then 5, stop pushes for NOTIFICATION_TIMEOUT_MINUTES
            if self.consecutive_failures > 5:
                if not self.notifications_paused_until:
                    self.notifications_paused_until = datetime.now() + timedelta(minutes=self.notification_timeout)
                    logger.warning(f"Too many consecutive failures. Notifications paused until {self.notifications_paused_until}")
        
            notifications_active = True
            if self.notifications_paused_until:
                if datetime.now() < self.notifications_paused_until:
                    notifications_active = False
                else:
                    # Timeout for pushes is over
                    self.notifications_paused_until = None
                    self.consecutive_failures = 0
                    logger.info("Notification timeout expired. Resuming notifications.")

            if (notifications_active and 
                (self.first_check or 
                 not current_status or 
                 (current_status and self.last_status is False))):
                callback(current_status, self.last_status)
            
            self.last_status = current_status
            self.first_check = False
            time.sleep(30)
