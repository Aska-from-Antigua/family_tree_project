"""
logging_config.py

Sets up logging with a configurable log level.
"""
import logging.config

def setup_logging(log_level=logging.DEBUG):
    """Sets up the logging configuration with the specified log level."""
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': log_level,  # Set log level from the parameter
                'formatter': 'simple',
            }
        },
        'formatters': {
            'simple': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            }
        },
        'root': {
            'handlers': ['console'],
            'level': log_level,  # Set log level for the root logger
        },
    })
