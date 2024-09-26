from django.contrib import admin
from myApp.models import *

class custom_user_display(admin.ModelAdmin):
    list_display= ['username','email','usertype']
admin.site.register(custom_user)

class jobModel_display(admin.ModelAdmin):
    list_display=['job_title','salary','company_name']
admin.site.register(jobModel)


class jobApplyModel_display(admin.ModelAdmin):
    list_display=['user','job','full_name','work_experience','expected_salary']
admin.site.register(jobApplyModel)



