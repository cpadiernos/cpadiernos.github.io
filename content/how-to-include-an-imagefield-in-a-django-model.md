Title: How to include an ImageField in a Django Model
Date: 2020-03-12 19:01
Category: Django
Tags: Django
Slug: how-to-include-an-imagefield-in-a-django-model
Authors: Carol Padiernos
Summary: This article assumes you've done a beginner's tutorial on Django and now you want to include an image field in your project. I'll go over how to customize where to save your images and how to serve them in development. I'll also provide implementation details for showing the image on a public facing site.

##Setup
Create a project like you normally would:
```console
django-admin startproject myproject
```

Create an application that will have a model that has an image field. In our case, we're doing an "animals" application:
```console
cd myproject
python manage.py startapp animals
```

##Model
Create a model in the animals application models.py file. Ours will be "Animal":
```python
# models.py

from django.db import models

class Animal(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='animal_images')
    
    def __str__(self):
        return f'{self.name}'
```
'animal_images' is the folder where our image will be uploaded to.

##Requirement
ImageField requires the Pillow library so you'll have to install it. On the command line enter:
```console
python -m pip install Pillow
```

##Storage
To customize where the 'animal_images' folder will be, we need to specify the MEDIA_ROOT in myproject settings.py:
```python
# settings.py

MEDIA_ROOT = os.path.join(BASE_DIR, 'myproject/media/')
```
So our file will end up in 'myproject/media/animal_images/'.

##Serving
To serve the images, we'll use Django's built-in helper function, static(). Add this to the existing myproject urls.py:
```python
# urls.py

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---
**NOTE**

django.conf.urls.static.static() is intended only for development! Not for production use.

---

To specify the url that serves the image, we need to specify MEDIA_URL in myproject settings.py:
```python
# settings.py

MEDIA_URL = '/media/'
```
If we upload an image called "image_file.jpg" via our admin, we can get it at http://127.0.0.1:8000/media/animal_images/image_file.jpg. 

You can just as easily make MEDIA_URL = '/images/' and you'll get your file at http://127.0.0.1:8000/images/animal_images/image_file.jpg

---
**NOTE**

Don't forget to register the model in the animals admin.py file, add the animals application to the installed apps in myproject settings.py, then 'python manage.py makemigrations', 'python manage.py migrate', and 'python manage.py createsuperuser' before heading to Admin.

---

**SHORT VERSION**
##Template
You can access the image file in the template by using {{ <context_object_name\>.<image_field_name\>.url }}. I.e.:
```html
<img src="{{ animal.image.url }}" alt="{{ animal.name }} image">
```
Notice we are accessing the image via its "url" property.

**DETAILS**
##Template
To view images on the site, we'll need to create a "templates" folder inside the "animals" application folder. And then another "animals" folder inside that. So you are placing the below html file in "animals/templates/animals". Name the file animal_detail.html:
```html
# animal_detail.html

<h1>{{ animal.name }}</h1>
<img src="{{ animal.image.url }}" alt="{{ animal.name }} image">
```
Notice we are accessing the image via its "url" property.

##View
We need a view that uses this html, so open up the animals application views.py file, and add the following class based view:
```python
from django.views import generic

from .models import Animal

class AnimalDetailView(generic.DetailView):
    model = Animal
    context_object_name = 'animal'
    template_name = 'animals/animal_detail.html'
```

##Url
To reach this view, we route our url to it. Create the animals application urls.py file, and add the following:
```python
# urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('animals/<int:pk>/', views.AnimalDetailView.as_view(),
        name='animal-detail'),
]
```
Notice that we are accessing the detail view by primary key, pk.

You'll also need to route your main myprojects urls file to include the animals urls, so add the below to myproject urls.py:
```python
# urls.py

from django.urls import path, include

urlpatterns = [
    ....
    path('', include('animals.urls')),
]
```
Notice that we updated 'from django.urls import path' to have 'include'.

If you added your first animal in admin, view it in your site at http://127.0.0.1:8000/animals/1.