from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator

class PersonalInfo(Model):
    id = fields.IntField(pk=True)
    first_name = fields.CharField(max_length=50)
    middle_name = fields.CharField(max_length=50, null=True)
    last_name = fields.CharField(max_length=50)
    date_of_birth = fields.DateField()
    sex = fields.CharField(max_length=1)  # Add sex field with choices
    age = fields.IntField(null=True)
    address = fields.TextField()
    registration_number = fields.CharField(max_length=20)
    mobile_number = fields.CharField(max_length=15)
    landline_number = fields.CharField(max_length=15, null=True)
    past_registration_info = fields.TextField(null=True)
    fees_status = fields.BooleanField(default=False)
    
    
    
class SummerCamp(Model):
    id = fields.IntField(pk=True)
    personal_info = fields.ForeignKeyField("models.PersonalInfo", related_name="summer_camps")
    class_name = fields.CharField(max_length=50)
    division = fields.CharField(max_length=10)

PersonalInfo_pydantic = pydantic_model_creator(PersonalInfo, name="PersonalInfo")
PersonalInfo_request = pydantic_model_creator(PersonalInfo, name="PersonalInfoRequest", exclude_readonly=True)


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=255)

    class Meta:
        table = "users"