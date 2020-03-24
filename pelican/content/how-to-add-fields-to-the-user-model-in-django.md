Title: How to add fields to the User model in Django
Date: 2020-03-11 13:06
Category: Django
Tags: Django
Slug: how-to-add-fields-to-the-user-model-in-django
Authors: Carol Padiernos
Summary: This article assumes that you've done at least a beginner's tutorial on Django and you want to customize the built-in User model by adding more fields. These fields will be common among all the users. For example, if you want all users to have a "nickname" field, etc. I'll cover how to adjust your Admin views as well so that you can view, update, and add users with those added fields included.

##Setup
Create a project as you normally would:
```console
django-admin startproject myproject
```
---
**NOTE** 

Do all the following steps BEFORE you do any 'python manage.py makemigrations' or 'python manage.py migrate'!

---
Create an application where you want to have your extended User model. In this case, we make an "accounts" application:
```console
cd myproject
python manage.py startapp accounts
```
<br/>
##Models
Open your accounts models.py file, and add your User model. In our case, CustomUser:
```python
# models.py

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    pass
```
<br/>
##Settings
Add that app to myproject settings.py installed apps:
```python
# settings.py

INSTALLED_APPS = [
    ...
    ...
    'accounts', 
]
```

And then add to the bottom of the same file:
```python
# settings.py

AUTH_USER_MODEL = 'accounts.CustomUser'
```

---
**NOTE**

You can now run 'python manage.py makemigrations' and then 'python manage.py migrate' if you want to add fields later on.

---
<br/>
##Models
To add fields to your model that you want to share among all the users, just include them in the CustomUser model. For example:
```python
# models.py

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    mailing_address = models.CharField(max_length=200, blank=True)
```
<br/>
##Admin
To be able to see the new CustomUser in the Admin site, you'll need to update your accounts application admin.py file:
```python
# admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    pass
    
admin.site.register(CustomUser, CustomUserAdmin)
```


---
**NOTE**

Don't forget to also 'python manage.py createsuperuser' so you can access the admin.

---


You'll notice that the user list view has the usual headings - email address, first name, last name, staff status. 

<br/>
##Admin list view
To add the fields as additional headings, you can use list_display:
```python
# admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff',
        'is_teacher', 'is_student', 'mailing_address'
        )
        
admin.site.register(CustomUser, CustomUserAdmin)
```
<br/>
##Admin detail view
The user detail view will have username, password, first name, last name, email address, active, staff status, superuser status, groups, user permissions, last login, and date joined.

To add your new fields to the detail view, you'll need to use fieldsets. The below will emulate the original view with the new fields at the bottom.

```python
# admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('is_student', 'is_teacher', 'mailing_address')
        })
    )
    
admin.site.register(CustomUser, CustomUserAdmin)
```
<br/>
##Admin add view
When you try to add a user, only username, password and password confirmation are available inputs. To have the new fields included as inputs, you can use add_fieldsets.

```python
# admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('is_student', 'is_teacher', 'mailing_address')
        })
    )
    
admin.site.register(CustomUser, CustomUserAdmin)
```


---
**NOTE**

Use "password1" and "password2" in "fields" to create and confirm the password.

---
<br/>
##Admin complete
The complete admin file should look like this:

```python
# admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff',
        'is_teacher', 'is_student', 'mailing_address'
        )
    
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('is_student', 'is_teacher', 'mailing_address')
        })
    )
    
    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('is_student', 'is_teacher', 'mailing_address')
        })
    )
    
admin.site.register(CustomUser, CustomUserAdmin)
```
