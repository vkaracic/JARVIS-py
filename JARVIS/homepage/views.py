from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import TemplateView

from users.models import ExtendedUser


class Register(TemplateView):
    template_name = 'templates/register.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # TODO: Create better validation than this.
        if username and password and email:
            user = User.objects.create(
                username=username,
                password=make_password(password),
                email=email
            )
            ExtendedUser.objects.create(
                user=user
            )
        return redirect(reverse('login'))


class Index(TemplateView):
    template_name = 'templates/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(Index, self).get_context_data(*args, **kwargs)
        context.update({
            'username': self.request.user.username,
            'email': self.request.user.email
        })
        return context
