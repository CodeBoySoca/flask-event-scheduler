from mongoengine import Document, StringField, DateField, DateTimeField, IntField, ListField, EmbeddedDocumentField, EmbeddedDocument, connect
import datetime
from bson import ObjectId
from dotenv import load_dotenv
import os

load_dotenv('.env')
connect('event-scheduler')


class Location(EmbeddedDocument):
    address1 = StringField()
    address2 = StringField()
    city = StringField()
    state = StringField()
    country = StringField()
    postal_code = StringField()

class EventDate(EmbeddedDocument):
    start_time = DateTimeField()
    end_time = DateTimeField()


class Notification(EmbeddedDocument):
    message = StringField()
    notification_type = StringField(default='')
    notification_date = DateTimeField(datetime.datetime.utcnow().strftime('%m-%d-%Y'))

    def get(email):
        return User.objects(email=email)


class Event(EmbeddedDocument):
    event_id = IntField()
    event_name = StringField()
    venue = StringField()
    location = EmbeddedDocumentField(Location)
    event_date = DateTimeField(datetime.datetime.utcnow().strftime('%m-%d-%Y'))
    event_time = ListField(EmbeddedDocumentField(EventDate))
    description = StringField()
    likes = IntField()
    notifications = ListField(EmbeddedDocumentField(Notification))
    privacy = StringField()
    subscribers = ListField()
    attendees = ListField()
    frequency = StringField()

    def add_event(event):
        Event(**event).save()
        return 200, 'ok'
    
    def delete_event(event_id):
        Event.objects(event_id=event_id).delete()
        return 204, 'ok'
    
    def update_event(event_id):
        Event.objects(event_id=event_id).update()
        return 204, 'update'
    
    def get(event_id):
        return Event.objects(event_id=event_id)
    
    def get_notifications(user_id):
        user_notification = User.objects(user_id=ObjectId(user_id))
        return user_notification


class User(Document):
    name = StringField(required=True)
    email = StringField(required=True)
    password = StringField(required=True)
    account_creation_date = DateField(datetime.datetime.utcnow().strftime('%m-%d-%Y'))
    image = StringField()
    event = ListField(EmbeddedDocumentField(Event)) 

    def create(user):
        User(**user).save()
        return 200, 'ok'

    def delete(user_id):
        User.objects(_id=ObjectId(user_id)).delete()
        return 204, 'deleted'
    
    def update(user_id):
        User.objects(_id=ObjectId(user_id)).update()
        return 204, 'updated'

    def get(user_id):
        return User.objects(_id=ObjectId(user_id))
    
    def check_email(email):
        return User.objects(email=email)

    def check_account(user):
        return User.objects(email=user['email']) 

