from mongoengine import Document, StringField, DateField, DateTimeField, IntField, ListField, EmbeddedDocumentField, EmbeddedDocument, ReferenceField
from datetime import datetime
from bson import ObjectId


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


class Notifications(EmbeddedDocument):
    message = StringField()
    notification_date = DateField()


class Event(EmbeddedDocument):
    event_id = IntField()
    event_name = StringField()
    venue = StringField()
    location = EmbeddedDocument(Location)
    event_date = DateField(datetime.datetime.utc)
    event_time = ListField(EmbeddedDocumentField(EventDate))
    description = StringField()
    likes = IntField()
    notifications = ListField(EmbeddedDocumentField(Notifications))
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
    

class User(Document):
    name = StringField()
    email = StringField()
    password = StringField()
    account_creation_date = DateField()
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

