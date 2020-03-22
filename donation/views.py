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

    def post(self, request):
        quantity = request.POST.get('bags')
        category = request.POST.getlist('categories')
        institution = Institution.objects.get(pk=request.POST.get('organization'))
        address = request.POST.get('address')
        phone_number = request.POST.get('phone')
        city = request.POST.get('city')
        zip_code = request.POST.get('postcode')
        pick_up_date = request.POST.get('date')
        pick_up_time = request.POST.get('time')
        pick_up_comment = request.POST.get('more_info')
        user = User.objects.get(pk=request.user.id)
        donation = Donation.objects.create(quantity=quantity, institution=institution,
                                           address=address, phone_number=phone_number, city=city, zip_code=zip_code,
                                           pick_up_date=pick_up_date, pick_up_time=pick_up_time,
                                           pick_up_comment=pick_up_comment,
                                           user=user)
        donation.save()
        for element in category:
            donation.categories.add(element)
        return redirect(reverse_lazy('confirmation'))


class DonationConfirmation(View):
    def get(self, request):
        return render(request, 'form-confirmation.html')




# class Login(View):
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
