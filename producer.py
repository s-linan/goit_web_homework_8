import pika
import json
from faker import Faker
from connect import connect_to_db
from contacts import Contact


NUM_CONTACTS = 5


def send_contact_to_queue(contact_id, channel):
    message = {"contact_id": str(contact_id)}
    channel.basic_publish(
        exchange='task_mock',
        routing_key='task_queue',
        body=json.dumps(message).encode(),
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ))


def fake_contacts_generation(num_contacts):
    fake = Faker()
    contacts = []
    for _ in range(num_contacts):
        contact = Contact(
            full_name=fake.name(),
            email=fake.email(),
            is_active=False
        )
        contact.save()
        contacts.append(contact.id)
    return contacts


def main():
    num_contacts = NUM_CONTACTS
    connect_to_db()

    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.exchange_declare(exchange='task_mock', exchange_type='direct')
    channel.queue_declare(queue='task_queue', durable=True)
    channel.queue_bind(exchange='task_mock', queue='task_queue')

    contact_ids = fake_contacts_generation(num_contacts)

    for contact_id in contact_ids:
        send_contact_to_queue(contact_id, channel)
        print(f" [x] Sent contact_id: {contact_id}")

    connection.close()


if __name__ == '__main__':
    main()
