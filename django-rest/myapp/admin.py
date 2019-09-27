from django.contrib import admin

# Register your models here.
from .models import MySession
from .models import Jupyter

admin.site.register(MySession)
admin.site.register(Jupyter)
