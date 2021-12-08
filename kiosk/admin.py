from django.contrib import admin
from .models import Customer
from .models import Order
from .models import LensType
from .models import LensMaterial
from .models import LensAddOns
from .models import LensPackage
from .models import LensPackageItem
from .models import LensDesign

admin.site.register(Customer)
admin.site.register(LensType)
admin.site.register(LensMaterial)
admin.site.register(LensAddOns)
admin.site.register(LensPackage)
admin.site.register(LensPackageItem)
admin.site.register(Order)
admin.site.register(LensDesign)
