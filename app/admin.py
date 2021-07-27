from django.contrib import admin
from .models import CarModel,Car,wheel,Fuel,Color,body,Condation,Gear,voivodeship,Cities,Message
# Register your models here.

@admin.register(CarModel)
class CarModelADmin(admin.ModelAdmin):
    prepopulated_fields={'slug' : ('name',)}
    list_display=('name','slug')

@admin.register(Car)
class CarADmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('title',)}
    list_display=('title','user','fuel','cities','body_type','color','technical_condiation','transmissions','wheel','update_date','price','is_avilable')

admin.site.register(wheel)
admin.site.register(Fuel)
admin.site.register(Color)
admin.site.register(body)
admin.site.register(Condation)
admin.site.register(Gear)
admin.site.register(voivodeship)
admin.site.register(Cities)

admin.site.register(Message)
