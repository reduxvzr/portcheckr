import os
import logging
from typing import Dict

logger = logging.getLogger(__name__)

def validate_environment_variables() -> Dict[str, str]:
    """
    Validate and return all required environment variables.
    Returns dictionary with all validated variables.
    Raises ValueError if any required variable is missing.
    """
    env_vars = {}
    
    try:
        # Required variables
        env_vars['API_TOKEN'] = os.getenv('TELEGRAM_BOT_API_TOKEN')
        if not env_vars['API_TOKEN']:
            raise ValueError("TELEGRAM_BOT_API_TOKEN environment variable is not set!")
        
        env_vars['CHAT_ID'] = os.getenv('TELEGRAM_CHAT_ID')
        if not env_vars['CHAT_ID']:
            raise ValueError("TELEGRAM_CHAT_ID environment variable is not set!")
        
        env_vars['PORT'] = os.getenv('PORT')
        if not env_vars['PORT']:
            raise ValueError("PORT environment variable is not set!")
        
        # Optional variables with warnings/defaults
        env_vars['HOST'] = os.getenv('HOST', '127.0.0.1')
        if not os.getenv('HOST'):
            logger.warning("HOST environment variable is not set! Using default '127.0.0.1'")
        
        env_vars['HOST_NAME'] = os.getenv('HOST_NAME', env_vars['HOST'])
        if not os.getenv('HOST_NAME'):
            logger.warning("HOST_NAME environment variable is not set! Using hostname as default")

        env_vars['SERVICE_NAME'] = os.getenv('SERVICE_NAME', '')
        if not os.getenv('SERVICE_NAME'):
            logger.warning("SERVICE_NAME environment variable is not set! Using blank name of service")

        env_vars['NOTIFICATION_TIMEOUT_MINUTES'] = os.getenv('NOTIFICATION_TIMEOUT_MINUTES', 30)
        if not os.getenv('NOTIFICATION_TIMEOUT_MINUTES'):
            logger.warning("NOTIFICATION_TIMEOUT_MINUTES environment variable is not set! Using default 30 minutes")
        return env_vars

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during configuration: {e}")
        raise
