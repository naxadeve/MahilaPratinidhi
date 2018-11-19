from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, TemplateView, ListView
from core.models import *
from .forms import UserCreateForm
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
import json


class Index(TemplateView):
    template_name="/"

    def get(self, request, *args, **kwargs):
        featured_data = MahilaPratinidhiForm.objects.all()[:9]
        news = News.objects.all()
        images = BackgroundImage.objects.all()
        image_list = []

        for item in images:
            img = item.get_absolute_image_url()
            image_list.append(img)
        
        json_list = json.dumps(image_list)

        if self.request.user.is_superuser:
            return render(request, self.template_name)
        else:
            return render(request, 'public/index.html', {'featured_data': featured_data, 'news':news, 
            'image_list':json_list})


def signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('public/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode('utf8'),
            'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = UserCreateForm()
    return render(request, 'public/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


class ExploreView(TemplateView):
    template_name = 'public/explore.html'


    def test_func(self):
        return not self.request.user.is_superuser


    def get(self, request, *args, **kwargs):
        district = District.objects.all()
        rastriyas = RastriyaShava.objects.all()
        pratinidhis = PratinidhiShava.objects.all()
        provinces = Province.objects.all()
        return render(request, self.template_name, {'districts':district, 'rastriyas':rastriyas,
        'pratinidhis':pratinidhis, 'provinces':provinces})


class MahilaPratinidhiView(TemplateView):
    template_name = 'public/lists.html'

    def get(self, request, *args, **kwargs):
        forms = MahilaPratinidhiForm.objects.filter(district_id=self.kwargs.get('district_id'))
        return render(request, self.template_name, {'forms':forms})


class ProvinceView(ListView):
    template_name = "public/lists.html"
    
    def get(self, request, *args, **kwargs):
        forms = ProvinceMahilaPratinidhiForm.objects.filter(province_id=self.kwargs.get('province_id'))
        return render(request, self.template_name, {'forms': form})


class Detail(DetailView):
    model = MahilaPratinidhiForm
    template_name = 'public/detail.html'
    context_object_name = 'form'


class DataVisualize(UserPassesTestMixin, TemplateView):
    template_name = 'public/data.html'


    def test_func(self):
        return not self.request.user.is_superuser


    def get(self, request, *args, **kwargs):
        form = MahilaPratinidhiForm.objects.all()
        total = form.count
        married = MahilaPratinidhiForm.objects.filter(marital_status='ljjflxt').count
        graduate = MahilaPratinidhiForm.objects.filter(educational_qualification__contains=':gfts').count
        return render(request, self.template_name, {'total':total, 'married':married, 'graduate':graduate})
    

class List(UserPassesTestMixin, TemplateView):
    template_name = 'public/lists.html'


    def test_func(self):
        return not self.request.user.is_superuser
    

class Tab(UserPassesTestMixin, TemplateView):
    template_name = 'public/tab.html'


    def test_func(self):
        return not self.request.user.is_superuser

