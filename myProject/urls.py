from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from myProject.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',loginPage,name='loginPage'),
    path('signupPage',signupPage,name='signupPage'),
    path('jobfeedPage',jobfeedPage,name='jobfeedPage'),
    path('logoutPage',logoutPage,name='logoutPage'),
    path('addjobPage',addjobPage,name='addjobPage'),
    path('apply_now/<str:apply_id>',apply_now,name='apply_now'),
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
