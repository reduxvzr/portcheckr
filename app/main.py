import logging
import threading
from config.validator import validate_environment_variables
from typing import Optional
from bot.core import PortCheckr
from bot.monitoring import PortMonitor

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

def main():
    try:
        # Load config
        config = validate_environment_variables()
        
        # Init components
        bot = PortCheckr(config)
        monitor = PortMonitor(config)
        
        def status_callback(current_status: bool, last_status: Optional[bool]):
            if current_status:
                if last_status is False:  # Restored service push
                    message = (f"[{config['HOST_NAME']} {config['SERVICE_NAME']}] "
                            f"[🟢 Restored] Service restored! "
                            f"Port {config['PORT']} on {config['HOST']} is available again")
                elif last_status is None:  # First check
                    message = (f"[{config['HOST_NAME']} {config['SERVICE_NAME']}] "
                            f"[🟢 Initial Status] "
                            f"Port {config['PORT']} on {config['HOST']} is available")
            else:
                message = (f"[{config['HOST_NAME']} {config['SERVICE_NAME']}] "
                        f"[🔴 Down] "
                        f"Port {config['PORT']} на {config['HOST']} UNREACHABLE!")
            
            bot.send_notification(message)
        
        # Start monitoring
        monitor_thread = threading.Thread(
            target=monitor.start_monitoring,
            args=(status_callback,),
            daemon=True
        )
        monitor_thread.start()
        
        # Start bot polling
        bot.bot.infinity_polling()
        
    except Exception as e:
        logging.critical(f"Fatal error: {e}", exc_info=True)
        exit(1)

if __name__ == "__main__":
    main()
