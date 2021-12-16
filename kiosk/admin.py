from django.contrib import admin
from .models import Customer
from .models import Order
from .models import LensType
from .models import LensMaterial
from .models import LensAddOns
from .models import LensDesign
from .models import LensDesignItem
from .models import MagnificationLevel

admin.site.register(Customer)
admin.site.register(LensType)
admin.site.register(LensMaterial)
admin.site.register(LensAddOns)
admin.site.register(Order)
admin.site.register(LensDesign)
admin.site.register(LensDesignItem)
admin.site.register(MagnificationLevel)
