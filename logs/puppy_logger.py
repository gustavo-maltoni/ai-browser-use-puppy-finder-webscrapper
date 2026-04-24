import logging

def puppy_logger() -> logging.Logger:
    # Define a new information logger
    logger = logging.getLogger('puppy')
    logger.setLevel(logging.INFO)

    # Create the logger format
    logger_format = '%(asctime)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(logger_format, datefmt='%Y-%m-%d %H:%M:%S')

    # Create a handler to save logs in a file
    file_handler = logging.FileHandler('puppy.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Create a handler to show logs in console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger