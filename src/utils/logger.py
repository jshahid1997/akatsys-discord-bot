"""
Logging utility for the Discord News Bot.
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

class Logger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')
            
        # Create formatters
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # File handler
        log_file = f'logs/newsbot_{datetime.now().strftime("%Y%m%d")}.log'
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10485760,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(logging.INFO)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message):
        """Log info level message."""
        self.logger.info(message)
    
    def error(self, message, exc_info=True):
        """Log error level message with exception info."""
        self.logger.error(message, exc_info=exc_info)
    
    def warning(self, message):
        """Log warning level message."""
        self.logger.warning(message)
    
    def debug(self, message):
        """Log debug level message."""
        self.logger.debug(message) 