from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import View
from donation.models import Category, Institution, Donation
from donation import forms


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
        if request.user.is_authenticated:
            categories = Category.objects.all()
            institutions = Institution.objects.all()
            return render(request, 'form.html', {'categories': categories,
                                                 'institutions': institutions})
        return redirect(reverse_lazy('login'))


#class Login(View):
#    def get(self, request):
#        return render(request, 'login.html')
#
#    def post(self, request):
#        username = request.POST.get('email')
#        password = request.POST.get('password')
#        user = authenticate(request, username=username, password=password)
#        if user is None:
#            if not User.objects.get(username=username):
#                #przekazać może wiadomość?
#                message = 'Podany użytkownik nie istnieje, proszę się zarejestrować'
#            else:
#                message = 'Podane hasło jest nieprawidłowe'
#            return redirect(reverse_lazy('register') + '#register')
#        login(request, user)
#        return render(request, 'index.html')


class Register(View):
    def get(self, request):
        form = forms.RegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
        return render(request, 'register.html', {'form': form})
