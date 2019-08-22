from django.contrib import admin
from .models import Call, Commitment, Fund, FundInvestment

admin.site.register(Call)
admin.site.register(Commitment)
admin.site.register(Fund)
admin.site.register(FundInvestment)
