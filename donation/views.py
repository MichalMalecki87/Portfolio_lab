from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.core.paginator import Paginator
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
        # paginator = Paginator(institutions_lst, 5)
        # page = request.GET.get('page')
        # institutions = paginator.get_page(page)
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


class UserPage(View):
    def get(self, request):
        if request.user:
            user = request.user
            donations = Donation.objects.filter(user=user)
            return render(request, 'user_page.html', {'donations': donations})
        return redirect(reverse_lazy('login'))


class UserDataChange(View):
    def get(self, request):
        user = request.user
        return render(request, 'user-data-change.html', {'user': user})

    def post(self, request):
        user = request.user
        success = user.check_password(request.POST.get('password'))
        if success:
            user.email = request.POST.get('user_email')
            user.username = request.POST.get('user_email')
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.save()
            message = 'Dane zostały pomyślnie zmienione'
        else:
            message = 'Wprowadź poprawne hasło'
        return render(request, 'user-data-change.html', {'user': user, 'message': message})


class UserPasswordChange(View):
    def get(self, request):
        form = forms.PasswordChangeForm(request.user)
        return render(request, 'user-password-change.html', {'form': form})

    def post(self, request):
        form = forms.PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect(reverse_lazy('user_data_change'))


class Register(View):
    def get(self, request):
        form = forms.RegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = username
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password, email=email)
            login(request, user)
            return redirect('login')
        return render(request, 'register.html', {'form': form})
