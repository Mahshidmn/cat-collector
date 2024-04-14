from django.contrib import admin
from .models import Cat, Feeding, Toy, Photo

#telling admin site which models we want to do CRUD on admin side
admin.site.register(Cat)
admin.site.register(Feeding)
admin.site.register(Toy)
admin.site.register(Photo)


