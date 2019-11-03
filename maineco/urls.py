from django.contrib.auth.views import LoginView
from django.urls import path, include
from django.contrib.auth.decorators import user_passes_test
from maineco.views import *
from users.views import *
from django.conf.urls.static import static

app_name = 'maineco'

urlpatterns = [
                  path('', main, name='main'),
                  path('about/', about, name='about'),
                  path('login/', user_passes_test(lambda u: u.is_anonymous, '/personal-data')(
                      LoginView.as_view(template_name='login.html')), name="login"),
                  path('logout/', logout, name='logout'),
                  path('signup/', signup, name='signup'),
                  path('signup/update', signup_user, name='signup_user'),
                  path('signup/verification/<hash_code>', validate_hash, name='hash_code'),
                  path('joinevent/', join_event, name='join_event'),

                  path('personal-data/', include('users.urls'))

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
