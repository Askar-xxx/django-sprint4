from django.urls import path, reverse_lazy, include
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView


urlpatterns = [
    path('',
         CreateView.as_view(
             template_name='registration/registration_form.html',
             form_class=UserCreationForm,
             success_url=reverse_lazy('blog:index'),
         ),
         name='registration',
         ),
    path('accounts/', include('django.contrib.auth.urls')),
]
