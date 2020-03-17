from django.shortcuts import render

# Create your views here.
from django.views import View
from donation.models import Category, Institution, Donation


class LandingPage(View):
    def get(self, request):
        institutions = Institution.objects.all()
        bags_quantity = 0
        institutions_quantity = Institution.objects.count()
        donations = Donation.objects.all()
        for donation in donations:
            bags_quantity += donation.quantity
        return render(request, 'index.html', {'bags_quantity': bags_quantity,
                                              'institutions_quantity': institutions_quantity,
                                              'institutions': institutions})


class AddDonation(View):
    def get(self, request):
        return render(request, 'form.html')


class Login(View):
    def get(self, request):
        return render(request, 'login.html')


class Register(View):
    def get(self, request):
        return render(request, 'register.html')