from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CallForm
from .models import Call, Commitment, Fund, FundInvestment


class WelcomeView(generic.TemplateView):
    template_name = "capital_calls/welcome.html"


class DashboardView(LoginRequiredMixin,generic.ListView):
    template_name = "capital_calls/dashboard.html"
    model = FundInvestment
    context_object_name = "objects"

    def get_queryset(self):
        return FundInvestment.objects.filter(user = self.request.user)
        
    def get_context_data(self, *args, **kwargs):          
        context = super().get_context_data(*args, **kwargs)
        commitments = Commitment.objects.filter(user=self.request.user)
        funds = Fund.objects.filter(commitments__in=commitments).distinct()
        context['funds'] = funds
        return context




class NewCallView(LoginRequiredMixin,generic.CreateView):
    template_name = "capital_calls/new_call.html"
    form_class = CallForm
    model = Call

    def get_context_data(self, *args, **kwargs):          
        context = super().get_context_data(*args, **kwargs)
        context["commitments"] = Commitment.objects.filter(user=self.request.user)
        return context

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user=self.request.user
        self.object.save()
        context= self.get_context_data()
        commitments = context["commitments"]
        capital_requirement = self.object.capital_requirement
        # Create the related FundInvestments
        for commitment in commitments:
            undraw_capital = commitment.get_undraw_capital_amount()
            if capital_requirement == 0:
                break
            elif capital_requirement > undraw_capital:
                FundInvestment.objects.create(
                    call=self.object,
                    commitment=commitment,
                    fund=commitment.fund,
                    amount=undraw_capital,
                    user=self.request.user
                )
                capital_requirement -= undraw_capital
            else:
                FundInvestment.objects.create(
                    call=self.object,
                    commitment=commitment,
                    fund=commitment.fund,
                    amount=capital_requirement,
                    user=self.request.user
                )
                capital_requirement = 0 
                
        return HttpResponseRedirect(self.get_success_url())
