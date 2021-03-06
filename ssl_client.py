# -*- coding: utf-8 -*-
# pylint: disable=C0111,C0103,R0205

import logging
import threading
import pika
import random
import ssl
import time

LOG_FORMAT = (
    "%(levelname) -10s %(asctime)s %(name) -30s %(funcName) "
    "-35s %(lineno) -5d: %(message)s"
)
LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

stopping = False

threads = []


def do_work(i):
    while True and not stopping:
        # context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context = ssl.create_default_context()
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations(cafile="./certs/ca_certificate.pem")
        context.load_cert_chain(
            certfile="./certs/client_wildcard.local_certificate.pem",
            keyfile="./certs/client_wildcard.local_key.pem",
        )

        thread_id = threading.get_ident()
        LOGGER.info("i: %s thread id: %s", i, thread_id)
        credentials = pika.PlainCredentials("guest", "guest")
        # p = 5682 + (i % 3)
        p = 5671
        parameters = pika.ConnectionParameters(
            host="localhost",
            port=p,
            credentials=credentials,
            heartbeat=5,
            ssl_options=pika.SSLOptions(context),
        )
        connection = pika.BlockingConnection(parameters)
        connection.sleep(random.randrange(1, 5))
        connection.close()


try:
    print("ANY KEY TO STOP")
    time.sleep(1)
    for i in range(0, 4):
        t = threading.Thread(target=do_work, args=(i,))
        t.start()
        threads.append(t)
    input("...")
    stopping = True
except KeyboardInterrupt:
    stopping = True

LOGGER.info("STOPPING!")

for thread in threads:
    thread.join()
