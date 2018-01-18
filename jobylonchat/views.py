from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin
from .forms import CustomUserCreationForm
from .forms import MessageForm
from .models import Message

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"
    http_method_names = ['get', 'post',]

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['user_list'] = User.objects.exclude(pk=self.request.user.pk)
        return context

class RegisterView(CreateView):
    template_name = "register.html"
    http_method_names = ['get', 'post',]
    form_class = CustomUserCreationForm
    success_url = '/'

class MessagesListView(LoginRequiredMixin, FormMixin, ListView):
    model = Message
    template_name = "messages.html"
    form_class = MessageForm
    http_method_names = ['get', 'post']

    def get_to_user(self):
        try:
            to_user = User.objects.get(username=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404(_('User not found'))
        return to_user
    
    def get_queryset(self):
        queryset = super().get_queryset()
        to_user = self.get_to_user()
        q = Q(to_user=to_user, from_user=self.request.user) | Q(to_user=self.request.user, from_user=to_user)
        return queryset.filter(q)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        to_user = self.get_to_user()
        context.update({'to_user': to_user})
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
#        import pdb; pdb.set_trace()
        to_user = self.get_to_user()
        if form.is_valid():
            Message.objects.create(from_user=request.user, to_user=to_user, message=form.cleaned_data['message'])
        else:
            messages.error(request, _('Please input message text'))
        return redirect('messages', username=to_user.username)
