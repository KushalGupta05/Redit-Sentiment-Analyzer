import logging
import os

def configure_logger():
    """
    Configures a logger for the Flask application.
    Logs will be written to 'logs/app.log'.
    """
    # Get a logger instance, typically named after the module where it's used
    logger = logging.getLogger(__name__)
    
    # Define the directory for logs
    log_dir = 'logs'
    # Create the log directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Define the full path for the log file
    log_file = os.path.join(log_dir, 'app.log')
    
    # Create a file handler that writes log messages to the specified file
    handler = logging.FileHandler(log_file)
    
    # Define the format for log messages
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    # Set the formatter for the handler
    handler.setFormatter(formatter)
    
    # Add the handler to the logger
    logger.addHandler(handler)
    
    # Set the logging level to INFO (or DEBUG, WARNING, ERROR, CRITICAL)
    # INFO means messages with level INFO and higher will be processed.
    logger.setLevel(logging.INFO)
    
    return logger