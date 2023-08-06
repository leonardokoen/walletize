from django.urls import path, include

#include signin and signup views
urlpatterns = [
        path('signin/', include('api.signin.urls')),
        path('signup/', include('api.signup.urls')),
   ]