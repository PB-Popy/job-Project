from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from myProject.views import *
from myProject.commonviews import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',loginPage,name='loginPage'),
    path('signupPage',signupPage,name='signupPage'),
    path('jobfeedPage',jobfeedPage,name='jobfeedPage'),
    path('logoutPage',logoutPage,name='logoutPage'),
    path('addjobPage',addjobPage,name='addjobPage'),
    path('apply_now/<str:apply_id>',apply_now,name='apply_now'),
    path('changepassword',changepassword,name='changepassword'),
    path('search',search,name='search'),
    path('appliedjob',appliedjob,name='appliedjob'),
    path('createdjob',createdjob,name='createdjob'),
    path('viewjobPage/<str:view_id>/',viewjobPage,name='viewjobPage'),
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
