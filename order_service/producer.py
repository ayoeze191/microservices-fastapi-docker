import pika
import json
def publish_order(product_id: int):
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq')
    )
    channel = connection.channel()
    # Create the queue if it doesn't exist
    channel.queue_declare(queue='order_queue', durable=True)
    # The message to send
    message = json.dumps({"product_id": product_id})
    # Publish the message
    channel.basic_publish(
        exchange='',
        routing_key='order_queue',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2  # makes message survive RabbitMQ restart
        )
    )

    print(f"Published order for product_id: {product_id}")
    connection.close()