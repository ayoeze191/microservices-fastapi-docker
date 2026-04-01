import pika
import json
import time

def process_order(ch, method, properties, body):
    order = json.loads(body)
    product_id = order["product_id"]
    print(f"Processing order for product_id: {product_id}", flush=True)
    time.sleep(1)
    print(f"Order processed for product_id: {product_id} ✅", flush=True)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_consumer():
    print("Starting consumer...", flush=True)
    time.sleep(15)  # 👈 wait 15 seconds for RabbitMQ to fully boot
    
    while True:
        try:
            print("Trying to connect to RabbitMQ...", flush=True)
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host='rabbitmq',
                    connection_attempts=10,
                    retry_delay=5
                )
            )
            channel = connection.channel()
            channel.queue_declare(queue='order_queue', durable=True)
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(
                queue='order_queue',
                on_message_callback=process_order
            )
            print("Consumer waiting for orders... ✅", flush=True)
            channel.start_consuming()

        except Exception as e:
            print(f"RabbitMQ not ready, retrying in 5s... {e}", flush=True)
            time.sleep(5)

if __name__ == "__main__":
    start_consumer()