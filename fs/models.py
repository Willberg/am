import mongoengine


# Create your models here.
class TextModel(mongoengine.Document):
    name = mongoengine.StringField(max_length=30)
    content = mongoengine.StringField(max_length=255)
