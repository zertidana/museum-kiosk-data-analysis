"""An example of a Kafka consumer"""

import json
import logging
import sys
from os import environ
from datetime import datetime, time

# pylint: disable=unused-variable

from dotenv import load_dotenv
from confluent_kafka import Consumer

from db_loader import get_db_connection, insert_message

LOG_FILE = "logs.txt"
LOG_FH = logging.FileHandler(LOG_FILE)
LOG_SH = logging.StreamHandler(sys.stdout)
logging.basicConfig(format='%(message)s', level=logging.INFO,
                    handlers=[LOG_SH, LOG_FH])


def is_valid_type(type_of_request: str) -> bool:
    """Checks validity of the type variable."""
    if type_of_request not in [0, 1, None]:
        logging.info(
            "INVALID⚠️ type %s is not in allowed values (0 or 1)", type_of_request)

        return False
    return True


def is_valid_val(val: str) -> bool:
    """Checking validity of val."""
    if val is None:
        logging.info("INVALID⚠️ missing val.")
        return False

    if val not in [-1, 0, 1, 2, 3, 4]:
        logging.info(
            "INVALID⚠️ val %s is not in allowed values (-1 to 4)", val)
        return False
    return True


def is_valid_site(site: str) -> bool:
    """Checks validity of the site variable."""
    if not site:
        logging.info("INVALID⚠️ missing site.")
        return False

    if not str(site).isdigit() or int(site) not in range(6):
        logging.info("INVALID⚠️ site %s is not in range(0–5)", site)
        return False
    return True


def is_valid_time(at: str) -> bool:
    """Checks validity of the time variable."""
    if not at:
        logging.info("INVALID⚠️ missing time.")
        return False

    at_clean = at.split("+")[0].split(".")[0]

    dt = datetime.fromisoformat(at_clean)
    parsed_time = dt.time()

    start = time(8, 45)
    end = time(18, 15)

    if start <= parsed_time <= end:
        return True
    logging.info("INVALID⚠️ time is out of bounds.")
    return False


def is_valid_message(message: dict) -> bool:
    """Checks validity of the message."""
    if message is None:
        logging.info("INVALID⚠️ message is None")
        return False

    if message.value() is None:
        logging.info("INVALID⚠️ missing value")
        return False
    return True


def consume_messages(consumer: Consumer, connect) -> None:
    """Decodes message and checks validity."""
    print("Listening for new messages with validation...")
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            logging.info("Kafka error: %s", msg.error())
            continue

        raw_value = msg.value().decode("utf-8")
        try:
            value = json.loads(raw_value)
        except json.JSONDecodeError:
            logging.info("INVALID JSON⚠️ %s", raw_value)
            continue

        valid = (
            is_valid_val(value.get("val")) and
            is_valid_site(value.get("site")) and
            is_valid_time(value.get("at")) and
            is_valid_type(value.get("type"))
        )

        if valid:
            insert_message(connect, value)
            print(f"✅ {raw_value}")
        else:
            print(f"⛔ {raw_value}")


if __name__ == "__main__":
    load_dotenv()
    conn = get_db_connection()

    consumer_msg = Consumer({
        "bootstrap.servers": environ["BOOTSTRAP_SERVERS"],
        "group.id": environ["GROUP"],
        "auto.offset.reset": "latest",
        "security.protocol": environ.get("SECURITY_PROTOCOL", "PLAINTEXT"),
        "sasl.mechanisms": environ.get("SASL_MECHANISM", ""),
        "sasl.username": environ.get("USERNAME", ""),
        "sasl.password": environ.get("PASSWORD", "")
    })

    consumer_msg.subscribe([environ["TOPIC"]])

    try:
        consume_messages(consumer_msg, conn)
    except KeyboardInterrupt:
        print("Stopped by user.")
    finally:
        consumer_msg.close()
