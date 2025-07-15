import json
import time
from kafka import KafkaConsumer
from behave import then

KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092']
KAFKA_TOPIC = 'alarms'

@then('an alarm with sourceId "{source_id}" and severity "{severity}" and clear false should be published on Kafka within {timeout:d} seconds')
def step_check_alarm_message_with_timeout(context, source_id, severity, timeout):
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',  # or 'latest' if you only want new messages
        enable_auto_commit=False,
        group_id=None,  # so each test run sees all messages
        value_deserializer=lambda m: json.loads(m.decode('utf-8')) if m else None,
        key_deserializer=lambda m: m.decode('utf-8') if m else None
    )

    found = False
    start_time = time.time()

    try:
        while time.time() - start_time < timeout:
            messages = consumer.poll(timeout_ms=1000)
            for _, records in messages.items():
                for message in records:
                    value = message.value
                    if not value:
                        continue

                    if (
                        value.get("sourceId") == source_id and
                        value.get("clear") is False and
                        value.get("severity", "").lower() == severity.lower()
                    ):
                        found = True
                        break
                if found:
                    break
            if found:
                break
    finally:
        consumer.close()

    assert found, (
        f"No matching alarm message found for sourceId={source_id}, "
        f"severity={severity}, clear=False within {timeout} seconds"
    )