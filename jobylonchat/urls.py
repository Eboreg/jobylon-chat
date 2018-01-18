from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from .forms import CustomAuthenticationForm
from .views import HomeView, RegisterView, MessagesListView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('login/', LoginView.as_view(template_name='login.html', authentication_form=CustomAuthenticationForm), name="login"),
    path('logout/', LogoutView.as_view(next_page='home'), name="logout"),
    path('register/', RegisterView.as_view(), name="register"),
    path('messages/<str:username>/', MessagesListView.as_view(), name="messages"),
    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
