Title: Function based views and their class based view equivalents in Django (Pt 1)
Date: 2020-03-10 10:00
Category: Django
Tags: Django
Slug: function-based-views-and-their-class-based-view-equivalents-in-django-part-one
Authors: Carol Padiernos
Summary: This article assumes you've done a tutorial in Django, are comfortable using function based views and want to start using class based views in your project. You should also have experience with creating a login for users. I'll give you typical use cases for function based views and discuss their class based view equivalents including: list, detail,login required list, login required detail, filtered list, viewer specific list, logged in users with restricted views list, and lists that have addional context.

##Setup
Create a project and application as you normally would. In our case, we are making a *toys* application.
```console
django-admin startproject myproject
cd myproject
python manage.py startapp toys
```
<br/>
##Models
Create the model by opening up your *toys* application *models.py* file:
```python
# models.py

from django.db import models
from django.contrib.auth.models import User

class Toy(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL,
        null=True, related_name='toys')

    def __str__(self):
        return f'{self.name}'
```
<br/>

---
**NOTE**

Do the usual - update admin.py file to register the Toy model, add toy application to settings.py file, 'python manage.py makemigrations', 'python manage.py migrate', 'python manage.py createsuperuser'.

---

<br/>
Create a couple of toys with users/owners. Make some usernames that start with the letter "t" because we'll work with them later.

##Urls
Our set up will involve having a separate *urls.py* file for the *toys* application, so set up the *myproject* project *urls.py* file to include the below:
```python
# urls.py

from django.urls import path, include

urlpatterns = [
    ...
    path('', include('toys.urls')),
]
```
<br/>
##List (anyone can see the toys)

###Urls
Create a *toys* application *urls.py* file and add the following:
```python
# urls.py

from django.urls import path

from . import views

urlpatterns = [
    path('fbv-toys/', views.toy_list,
        name='fbv=toy-list'),
    path('cbv-toys/', views.ToyListView.as_view(),
        name='cbv-toy-list'),
]
```
###Views
*Toys* application *views.py* file:
```python
# views.py

# function based view

from .models import Toy

def toy_list(request):
    toy_list = Toy.objects.all()
    context = {'toy_list' : toy_list}
    return render(request, 'toys/toy_list.html', context)
    
# class based view

from django.views import generic

class ToyListView(generic.ListView):
    model = Toy
    context_object_name = 'toy_list'
    template_name = 'toys/toy_list.html'
```
In the class based view, the default **context_object_name** is **'<lowercase_model_class_name\>_list'** i.e. 'toy_list' in our case, so we don't need to specify. However, it's good practice to name it.

Also in the class based view, the default **template_name** is **'<app_name\>/<lowercase_model_class_name\>_list.html'**, i.e. 'toys/toy_list.html' in our case, so we don't need to specify. If we specify a *template_name*, it will look for that template. If we specify a *template_name* that doesn't exist, the class based view will still look for the default *<app_name\>/<lowercase_model_class_name\>_list.html*.

###Templates
Our *context/context_object_name* is the same for both views so we can use the same template. Create the below *toy_list.html* file and place it in *'toys/templates/toys'* folder, where the first 'toys' is our application folder.
```python
# under 'toys/templates/toys'
# toy_list.html

{% for toy in  toy_list %}
  <ul>
    <li>{{ toy.name }} - {{ toy.owner }}</li>
  </ul>
{% endfor %}
```
<br/>
##Detail (anyone can see this toy)

###Urls
Add these paths to the *toys* application *urls.py* file. Note I'm just adding them via '+=' on the bottom of my file:
```python
# urls.py

urlpatterns += [
    path('fbv-toys/<int:toy_pk>/', views.toy_detail,
        name='fbv-toy-detail'),
    path('cbv-toys/<int:toy_pk>/', views.ToyDetailView.as_view(),
        name='cbv-toy-detail'),
]
```

###Views
Add these views to *toys* application *views.py*:
```python
# views.py

# function based view

from django.shortcuts import get_object_or_404

def toy_detail(request, toy_pk):
    toy_detail = get_object_or_404(Toy, pk=toy_pk)
    context = {'toy_detail': toy_detail}
    return render(request, 'toys/toy_detail.html', context)

# class based view

class ToyDetailView(generic.DetailView):
    model = Toy
    context_object_name = 'toy_detail'
    template_name = 'toys/toy_detail.html'
    pk_url_kwarg = 'toy_pk'
```
In the class based view, the default **context_object_name** is **<lowercase_model_class_name\>** i.e. 'toy'. Note it's **not** *<lowercase_model_class_name\>_detail*. I specified 'toy_detail' here though for consistency with the template, which we discuss next.

Also in the class based view, **template_name** defaults to **'<app_name\>/<lowercase_model_class_name\>_detail.html'** i.e. 'toys/toy_detail.html' in our case, so we don't need to specify. If we specify a **template_name**, the view will look for that template.

Unlike the ListView we spoke about earlier, if we specify a *template_name* that doesn't exist, this class based view will get a TemplateDoesNotExist error.

Lastly, the default **pk_url_kwarg** is **'pk'** and you'll have to set path to **('cbv-toys/<int:pk\>'....)** if you don't want to specify. In our case, we specified *'toy_pk'* and so we set path to *('cbv-toys/<int:toy_pk\>'....)*.

###Templates
Create another template file called *toy_detail.html* in the same folder as our *toy_list.html* and put the below info in it:
```python
# under toys/templates/toys
# toy_detail.html

{{ toy_detail.name }} - {{ toy_detail.owner }}
```
<br/>
##Login required
---
**SHORT VERSION** 

Instead of using **login_required** decorator in function based view, inherit **LoginRequiredMixin** class in the class based view. Make sure it's in *leftmost* position in the inheritance list!

---
<br/>
##List that requires login (only the logged in users can see all the toys)
To test this out, we'll want to create a way to login with different users. Go to any tutorial, I recommend the [Django Tutorial Part 8: User authentication and permissions](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Authentication) on Mozilla. Skip to the section *Setting up your authentication views*.

###Urls
Add this to the bottom of the *toys* application *urls.py* file:
```python
# urls.py

urlpatterns += [
    path('login-fbv-toys/', views.login_required_toy_list,
        name='login-fbv-toy-list'),
    path('login-cbv-toys/', views.LoginRequiredToyListView.as_view(),
       name='login-cbv-toy-list'),
]
```

###Views
*Toys* application *views.py*:
```python
# views.py

# function based view

from django.contrib.auth.decorators import login_required

@login_required
def login_required_toy_list(request):
    toy_list = Toy.objects.all()
    context = {'toy_list' : toy_list}
    return render(request, 'toys/toy_list.html', context)

# class based view

from django.contrib.auth.mixins import LoginRequiredMixin

class LoginRequiredToyListView(LoginRequiredMixin, generic.ListView):
    model = Toy
    context_object_name = 'toy_list'
    template_name = 'toys/toy_list.html'
```
<br/>
##Detail that requires login (only logged in users can see this toy)

###Urls
```python
# urls.py

urlpatterns += [
    path('login-fbv-toys/<int:toy_pk>/', views.login_required_toy_detail,
        name='login-fbv-toy-detail'),
    path('login-cbv-toys/<int:toy_pk>/', views.LoginRequiredToyDetailView.as_view(),
        name='login-cbv-toy-detail'),
]
```

###Views
```python
# views.py

# function based view

from django.contrib.auth.decorators import login_required

@login_required
def login_required_toy_detail(request, toy_pk):
    toy_detail = get_object_or_404(Toy, pk=toy_pk)
    context = {'toy_detail': toy_detail}
    return render(request, 'toys/toy_detail.html', context)

# class based view

from django.contrib.auth.mixins import LoginRequiredMixin

class LoginRequiredToyDetailView(LoginRequiredMixin, generic.DetailView):
    model = Toy
    context_object_name = 'toy_detail'
    template_name = 'toys/toy_detail.html'
    pk_url_kwarg = 'toy_pk'
```
<br/>
## List filtered by object characteristic (only the toys that were given on birthdays)

###Models
Update *toys* *models.py* so that we have another field that we can filter by:
```python
# models.py
class Toy(models.Model):
    ...
    is_birthday_present = models.BooleanField(default=False)
```
<br/>
---
**NOTE**

Don't forget to 'python manage.py makemigrations' and 'python manage.py migrate'

---
<br/>
###Urls
```python
# urls.py
urlpatterns += [
    path('fbv-toys/birthday/', views.toy_list,
        name='fbv-toy-list'),
    path('cbv-toys/birthday/', views.ToyListView.as_view(),
       name='cbv-toy-list'),
]
```

###Views
```python
# views.py

# function based view

def birthday_toy_list(request):
    birthday_toy_list = Toy.objects.filter(is_birthday_present=True)
    context = {'toy_list' : birthday_toy_list}
    return render(request, 'toys/toy_list.html', context)

# class based view

class BirthdayToyListView(generic.ListView):
    context_object_name = 'toy_list'
    template_name = 'toys/toy_list.html'
    queryset = Toy.objects.filter(is_birthday_present=True)

# alternate class based view

class BirthdayToyListView(generic.ListView):
    context_object_name = 'toy_list'
    template_name = 'toys/toy_list.html'
    
    def get_queryset(self):
        birthday_toy_list = Toy.objects.filter(is_birthday_present=True)
        return birthday_toy_list
```
Notice for both the class based views, you don't have to also specify the model.

<br/>
## List filtered by user (only the toys that a specific kid owns)

###Urls
```python
# urls.py

urlpatterns += [
    path('fbv-toys/<str:username>/', views.user_toy_list,
        name='user-fbv-toy-list'),
    path('cbv-toys/<str:username>/', views.UserToyListView.as_view(),
       name='user-cbv-toy-list'),
]
```
---
**NOTE**

You need to put this set of paths *AFTER* the *'cbv-toys/birthday/'* path. If placed before, we would encounter *'fbv-toys/<str:username\>'* first and access the view connected to it, *user_toy_list* and *UserToyListView* respectively. The view would treat 'birthday' as a username and you would get nothing back.

---

###Views
```python
# views.py

# function based view

def user_toy_list(request, username):
    user_toy_list = Toy.objects.filter(owner__username=username)
    context = {'toy_list' : user_toy_list}
    return render(request, 'toys/toy_list.html', context)

# class based view

class UserToyListView(generic.ListView):
    context_object_name = 'toy_list'
    template_name = 'toys/toy_list.html'
    
    def get_queryset(self):
        username = self.kwargs['username']
        user_toy_list = Toy.objects.filter(owner__username=username)
        return user_toy_list
```
Notice this is basically the same as a filtered list, except, for the function based view, we access the username value via the url, and for the class based view, we grab that same value via self.kwargs.

<br/>
## List filtered by viewer (I can only see my own toys)
Most likely you'll want to filter the toy list DEPENDING on what user is VIEWING it.

###Urls
```python
# urls.py

urlpatterns += [
    path('fbv-toys/my/', views.my_toy_list,
        name='my-fbv-toy-list'),
    path('cbv-toys/my/', views.MyToyListView.as_view(),
       name='my-cbv-toy-list'),
]
```
---
**NOTE**

Remember to put this BEFORE the *'fbv-toys/<str:username\>'*. Otherwise, you'll be hitting *'fbv-toys/<str:username\>'* first and calling the associated view which will think the username is "my".

---

###Views
```python
# views.py

# function based view

def my_toy_list(request):
    username = request.user.username
    my_toy_list = Toy.objects.filter(owner__username=username) # you can filter by other user fields. ie. owner_id = request.user.id
    context = {'toy_list' : my_toy_list}
    return render(request, 'toys/toy_list.html', context)

# class based view

class MyToyListView(generic.ListView):
    context_object_name = 'toy_list'
    template_name = 'toys/toy_list.html'
    
    def get_queryset(self):
        username = self.request.user.username
        my_toy_list = Toy.objects.filter(owner__username=username)
        return my_toy_list
```

Don't forget you need to be logged in. You can combine this with the login_required to make sure it's not an anonymous user. You get no list if you're an anonymous user.
<br/>
## List filtered by user who passes a certain criteria (only users who are allowed to see all the toys can see the toys)

###Urls
```python
# urls.py

urlpatterns += [
    path('fbv-toys/secret-club/', views.secret_club_toy_list,
        name='secret-fbv-toy-list'),
    path('cbv-toys/secret-club/'), views.SecretClubToyListView.as_view(),
        name='secret-cbv-toy-list'),
]
```

###Views
```python
# views.py

# function based view

from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def name_check(user):
    # only people whose names start with a t can be in the secret club
    if user.username[0] == "t":
        return True
    else:
        raise PermissionDenied

@login_required
@user_passes_test(name_check)
def secret_club_toy_list(request):
    secret_club_toy_list = Toy.objects.all()
    context = {'toy_list': secret_club_toy_list}
    return render(request, 'toys/toy_list.html', context)

# class based view

from django.contrib.auth.mixins import UserPassesTestMixin

class SecretClubToyListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = Toy
    context_object_name = 'toy_list'
    template_name = 'toys/toy_list.html'
    
    def test_func(self):
        # only people whose names start with a t can be in the secret club
        if self.request.user.username[0] == "t":
            return True
        else:
            return False
```

Both the above views will first ask the user to login, and once logged in, it will return PermissionDenied if the user doesn't pass the test.

If you want to redirect the user after they login but don't pass the test, then you could do the below. In both views we redirect to only show the viewers' toys if they don't belong to the secret club.

```python
# views.py

# function based view

from django.contrib.auth.decorators import user_passes_test

def name_check(user):
    # only people whose names start with a t can be in the secret club
    if user.username[0] == "t":
        return True
    return False

@login_required
@user_passes_test(name_check, login_url='/fbv-toys/my/', redirect_field_name=None)
def secret_club_toy_list(request):
    secret_club_toy_list = Toy.objects.all()
    context = {'toy_list': secret_club_toy_list}
    return render(request, 'toys/toy_list.html', context)
    
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect

class SecretClubToyListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = Toy
    context_object_name = 'toy_list'
    template_name = 'toys/toy_list.html'
    
    def test_func(self):
        # only people whose names start with a t can be in the secret club
        if self.request.user.username[0] == "t":
            return True
        else:
            return False
            
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('my-cbv-toy-list')
        else:
            return super().handle_no_permission()
```
In the function based view, notice that **login_url** is the url that the user is redirected to if he/she **DOES NOT PASS** the test. The default is *settings.LOGIN_URL*.

**redirect_field_name** should be set to None. If it isn't set to none, the "?next=" will be tacked on after the *login_url*.

In the class based view, notice the handle_no_permission method. It is called by LoginRequiredMixin first, then by UserPassesTestMixin. So if you want the user to first be directed to the login, then be redirect if it does not pass, then you'll have to set it up like the above.

# Adding extra context
Set up your urls:
```python
# urls.py

urlpatterns += [
    path('fbv-toys-and-users/', views.toy_and_user_list,
        name='fbv-toy-user-list'),
    path('cbv-toys-and-users/', views.ToyUserListView.as_view(),
        name='cbv-toy-user-list'),
]
```
Add some views:
```python
# views.py

# function based view

from django.contrib.auth.models import User

def toy_and_user_list(request):
    toy_list = Toy.objects.all()
    user_list = User.objects.all()
    context = {
        'toy_list': toy_list,
        'user_list': user_list,
    }
    return render(request, 'toys/toy_list.html', context)
    
# class based view

from django.views import generic

class ToyUserListView(generic.ListView):
    model = Toy
    context_object_name = 'toy_list'
    template_name = 'toys/toy_list.html'
    extra_context = {'user_list': User.objects.all()}
    
# alternate class based view

class ToyUserListView(generic.ListView):
    model = Toy
    context_object_name = 'toy_list'
    template_name = 'toys/toy_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_list'] = User.objects.all()
        return context
```
Update your html so you can see your added context:
```python
# toy_list.html

TOYS
{% for toy in  toy_list %}
  <ul>
    <li>{{ toy.name }} - {{ toy.owner }}</li>
  </ul>
{% endfor %}

USERS
{% for user in  user_list %}
  <ul>
    <li>{{ user.username }}</li>
  </ul>
{% endfor %}
```
