from django.contrib import admin
from .models import Customer
from .models import LensType
from .models import LensMaterial
from .models import LensAddOns
from .models import CustomerLensPackage
from .models import LensPackage

admin.site.register(Customer)
admin.site.register(LensType)
admin.site.register(LensMaterial)
admin.site.register(LensAddOns)
admin.site.register(CustomerLensPackage)
admin.site.register(LensPackage)
