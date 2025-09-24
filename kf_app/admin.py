from django.contrib import admin
from .models import *

admin.site.is_registered(Author)
admin.site.is_registered(Book)
admin.site.is_registered(Publisher)


