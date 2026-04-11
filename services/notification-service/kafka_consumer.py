# Kafka consumer — listens to order and escrow events and sends SMS
# Topics: order.confirmed, escrow.held, order.delivered, escrow.released

from kafka import KafkaConsumer
import json

TOPICS = [
    "order.confirmed",
    "escrow.held",
    "order.delivered",
    "escrow.released",
]

SMS_TEMPLATES = {
    "order.confirmed": "FarmLink: A buyer matched your listing of {quantity_kg}kg {crop_type} at N{price}/kg. Login to confirm.",
    "escrow.held": "FarmLink: Payment of N{amount_ngn} is secured in escrow. You can now harvest safely.",
    "order.delivered": "FarmLink: Your buyer has marked the order as delivered. Please confirm receipt.",
    "escrow.released": "FarmLink: N{amount_ngn} has been sent to your account. Transaction recorded on blockchain.",
}

def start_consumer():
    consumer = KafkaConsumer(
        *TOPICS,
        bootstrap_servers=["kafka:9092"],
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        group_id="notification-service-group",
        auto_offset_reset="earliest",
    )
    print("Notification consumer started. Listening to topics:", TOPICS)
    for message in consumer:
        topic = message.topic
        data = message.value
        print(f"Received event on {topic}: {data}")
        handle_event(topic, data)

def handle_event(topic: str, data: dict):
    template = SMS_TEMPLATES.get(topic)
    if not template:
        return
    try:
        sms_text = template.format(**data)
        phone = data.get("farmer_phone") or data.get("buyer_phone")
        print(f"Sending SMS to {phone}: {sms_text}")
        # TODO: replace with real Termii API call
    except KeyError as e:
        print(f"Missing field in event data: {e}")

if __name__ == "__main__":
    start_consumer()
