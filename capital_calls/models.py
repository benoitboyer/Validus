from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.urls import reverse_lazy

# Create your models here.
class Fund(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class Commitment(models.Model):
    fund = models.ForeignKey(
        "Fund", on_delete=models.CASCADE, related_name="commitments"
    )
    date = models.DateField()
    amount = models.DecimalField(
        max_digits=13,
        decimal_places=2,
        validators=[MaxValueValidator(100000000000), MinValueValidator(1)],
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name = 'comitments'
    )
    def get_undraw_capital_amount(self):
        fund_investments_sum = list(self.fund_investments.aggregate(models.Sum('amount')).values()or 0.00)[0]
        if fund_investments_sum:
            undraw_amount =  self.amount - fund_investments_sum
            return undraw_amount
        return self.amount
    
    def __str__(self):
        return f"{self.fund} - {self.date} - {self.amount}"


class Call(models.Model):
    date = models.DateField()
    investment_name = models.CharField(max_length=120)
    capital_requirement = models.DecimalField(
        max_digits=13,
        decimal_places=2,
        validators=[MaxValueValidator(100000000000), MinValueValidator(1)],
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name = 'calls'
    )
    def __str__(self):
        return f"{self.investment_name} - {self.capital_requirement}"

    def get_absolute_url(self):
        return reverse_lazy("capital_calls:dashboard")


class FundInvestment(models.Model):
    call = models.ForeignKey(
        "Call", on_delete=models.CASCADE, related_name="fund_investments"
    )
    commitment = models.ForeignKey(
        "Commitment", on_delete=models.CASCADE, related_name="fund_investments"
    )
    fund = models.ForeignKey(
        "Fund", on_delete=models.CASCADE, related_name="fund_investments"
    )
    amount = models.DecimalField(
        max_digits=13,
        decimal_places=2,
        validators=[MaxValueValidator(100000000000), MinValueValidator(1)],
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name = 'fund_investments'
    )

        
    def __str__(self):
        return f"{self.call} - {self.commitment.fund} - {self.amount}"
