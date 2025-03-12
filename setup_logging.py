import logging

def setup_logging():
    logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Logging setup complete.")

if __name__ == "__main__":
    setup_logging()
