import pika
import json
from connect import connect_to_db
from contacts import Contact


def send_email(message):
    print(f" [x] Sending email: {message}")


def update_contact_status(contact_id):
    contact = Contact.objects(id=contact_id).first()
    if contact:
        if contact.is_active is False:
            contact.is_active = True
            contact.save()
        contact.save()


def callback(ch, method, properties, body):
    message = json.loads(body.decode())
    contact_id = message.get("contact_id")

    send_email("message delivered")
    update_contact_status(contact_id)

    print(f" [x] Done: {method.delivery_tag}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connect_to_db()

    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_queue', on_message_callback=callback)

    channel.start_consuming()


if __name__ == '__main__':
    main()
