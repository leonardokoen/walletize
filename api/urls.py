from django.urls import path, include

#include signin and signup views
urlpatterns = [
        path('signin/', include('api.signin.urls')),
        path('signup/', include('api.signup.urls')),
        path('token_refresh/', include('api.token_refresh.urls')),
        path('activate/', include('api.activation.urls'))

   ]