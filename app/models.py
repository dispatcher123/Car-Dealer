from django.core.checks import messages
from django.db import models
from account.models import CustomUser
from django.utils.text import slugify
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from ckeditor.fields import RichTextField
from django.db.models import Max
from django.db.models.signals import post_save
def current_year():
    return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)   

class CarModel(models.Model):
    name=models.CharField(max_length=250,unique=True)
    slug=models.CharField(max_length=250)


    def __str__(self):
        return self.name

    def save(self,*args, **kwargs):
        self.slug=slugify(self.name)
        super(CarModel,self).save(*args, **kwargs)


class Color(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Fuel(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
        return self.name

class body(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
        return self.name



class Condation(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Gear(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
        return self.name

class wheel(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
        return self.name


class voivodeship(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Cities(models.Model):
    name=models.CharField(max_length=250)
    voivodeship=models.ForeignKey(voivodeship,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

SUBSCRIPTION=(
    ('F','UNPAID'),
    ('M','MONHTLY'),
    ('Y','YEARLY')
)
class Car(models.Model):
    image=models.ImageField(upload_to='image')
    car_type=models.CharField(max_length=10)
    video=models.FileField(upload_to='video')
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='car_user')
    description=RichTextField()
    cities=models.ForeignKey(Cities,on_delete=models.CASCADE)
    carmodel=models.ForeignKey(CarModel,on_delete=models.CASCADE)
    title=models.CharField(max_length=250,unique=True)
    created_date=models.DateTimeField(auto_now_add=True)
    update_date=models.DateTimeField(auto_now=True)
    year = models.PositiveIntegerField(
    default=current_year(), validators=[MinValueValidator(1900), max_value_current_year])
    slug=models.SlugField(max_length=250)
    capacity_engine=models.PositiveIntegerField(default=0)
    fuel=models.ForeignKey(Fuel,on_delete=models.CASCADE)
    engine_power=models.PositiveIntegerField(default=0)
    kilometers=models.PositiveIntegerField(default=0)
    body_type=models.ForeignKey(body,on_delete=models.CASCADE)
    color=models.ForeignKey(Color,on_delete=models.CASCADE)
    technical_condiation=models.ForeignKey(Condation,on_delete=models.CASCADE)
    transmissions=models.ForeignKey(Gear,on_delete=models.CASCADE)
    wheel=models.ForeignKey(wheel,on_delete=models.CASCADE)
    is_avilable=models.BooleanField(default=False)
    expiry_date=models.DateField(null=True,blank=True)
    price=models.PositiveBigIntegerField(default=0)
    subscription=models.CharField(max_length=100,default='UNPAID',choices=SUBSCRIPTION)
    views=models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.title

    def save(self,*args, **kwargs):
        self.slug=slugify(self.title)
        super(Car,self).save(*args, **kwargs)


from django.db import models
from django.db.models import Max

# Create your models here.
class Message(models.Model):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')
	sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='from_user')
	recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='to_user')
	body = models.TextField(max_length=1000, blank=True, null=True)
	date = models.DateTimeField(auto_now_add=True)
	is_read = models.BooleanField(default=False)


	def send_message(from_user, to_user, body):
		sender_message = Message(
			user=from_user,
			sender=from_user,
			recipient=to_user,
			body=body,
			is_read=True)
		sender_message.save()

		recipient_message = Message(
			user=to_user,
			sender=from_user,
			body=body,
			recipient=from_user,)
		recipient_message.save()
		return sender_message

	def get_messages(user):
		messages = Message.objects.filter(user=user).values('recipient').annotate(last=Max('date')).order_by('-last')
		users = []
		for message in messages:
			users.append({
				'user': CustomUser.objects.get(pk=message['recipient']),
				'last': message['last'],
				'unread': Message.objects.filter(user=user, recipient__pk=message['recipient'], is_read=False).count()
				})
		return users


