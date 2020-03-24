Title: Function based views and their class based view equivalents in Django (Pt 2)
Date: 2020-03-23 14:29
Category: Django
Tags: Django
Slug: function-based-views-and-their-class-based-view-equivalents-in-django-part-two
Authors: Carol Padiernos
Summary: This article assumes you've done a tutorial in Django, are comfortable using function based views and want to start using class based views in your project. I'll be discussing function based views and their equivalent class based views when working with forms. This includes creating, updating, and deleting objects, intializing forms, and manipulating data after a form's data is found to be valid.

We're continuing with our *toys* application from [Function based views and their class based view equivalents in Django (Pt 1)](https://cpadiernos.github.io/function-based-views-and-their-class-based-view-equivalents-in-django-part-one.html)

# Create

Add the below paths to the *toys* application *urls.py* file:
```python
# urls.py

urlpatterns += [
    path('fbv-toys/new/', views.create_toy,
        name='fbv-toy-create'),
    path('cbv-toys/new/', views.ToyCreateView.as_view(),
       name='cbv-toy-create'),
]
```
<br/>

---
**NOTE**

Put all the paths in this article BEFORE *path('fbv-toys/<str:username\>/',...)* from the previous article.

---

<br/>
Create a *forms.py* file in the *toys* application. Note we'll be using a *ModelForm*:
```python
# forms.py

from django import forms

from .models import Toy

class ToyForm(forms.ModelForm):
    class Meta:
        model = Toy
        fields = ('name', 'owner', 'is_birthday_present')
```

Make the views that plan to use that form:
```python
# views.py

# function based view

from django.shortcuts import redirect

from .forms import ToyForm

def create_toy(request):
    if request.method == 'POST':
        form = ToyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fbv-toy-list')
    else:
        form = ToyForm()
    
    return render(request, 'toys/toy_form.html' , {'form': form})
    
# class based view

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

class ToyCreateView(CreateView):
    model = Toy
    form_class = ToyForm
    success_url = reverse_lazy('cbv-toy-list') # you can also simply put '/cbv-toys/' but its better practice to reference the url name
    template_name = 'toys/toy_form.html'
    
# alternate class based view

class ToyCreateView(CreateView):
    model = Toy
    fields = ('name', 'owner', 'is_birthday_present')
    success_url = reverse_lazy('cbv-toy-list') 
    template_name = 'toys/toy_form.html'
    
# another alternate class based view

class ToyCreateView(CreateView):
    model = Toy
    form_class = ToyForm
    template_name = 'toys/toy_form.html'
    
    def get_success_url(self):
        return reverse('cbv-toy-list')
```

For the class based view, you don't have to specify a **form_class**, and you can simply use the **fields** field to specify the fields you want.

For our class based view, notice we are specifying our **success_url** and using *reverse_lazy*. We can also simply use the url path, ie. '/cbv-toys/'. Alternatively we can override the **get_success_url** method if we plan to do anything more fancy. i.e. grabbing the pk in the url to use in the redirect url.

After successful creation, the class based view defaults to calling the **get_absolute_url** method defined in your model, so if you do not want to include a **success_url** in your view, then update your model to include the below. This will redirect us to the detail page of our newly created object.
```python
# models.py

from django.urls import reverse

class Toy(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL,
        null=True, related_name='toys')
    is_birthday_present = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'
        
    def get_absolute_url(self):
        return reverse('cbv-toy-detail', kwargs={'toy_pk': self.pk})
```

Lastly, the class based view defaults to looking up **<model_name\>_form.html**, i.e. in our case *toy_form.html*, so you don't have to specify the **template_name** unless you plan to name your file differently.

Create *toy_form.html* and place it in the *'toys/templates/toys/'* folder:
```html
# in 'toys/templates/toys/'
# toy_form.html

<form action="" method="post">
  # make sure to include {% csrf_token %}
  {{ form.as_p }}
  <input type="submit" value="Submit">
</form>
```
<br/>

---
**NOTE**

Remember to include <form\> and </form\> and the <input\> button with your {{form}}.
 
---
<br/>
# Update

Add more paths to your *urls.py* file:
```python
# urls.py

urlpatterns += [
    path('fbv-toys/<int:toy_pk>/edit/', views.update_toy,
        name='fbv-toy-update'),
    path('cbv-toys/<int:toy_pk>/edit/', views.ToyUpdateView.as_view(),
        name='cbv-toy-update'),
]
```
We'll use the same form we used before, i.e. ToyForm.

Add these views:
```python
# views.py

# function based view

def update_toy(request, toy_pk):
    toy = get_object_or_404(Toy, pk=toy_pk)
    if request.method == 'POST':
        form = ToyForm(request.POST, instance=toy)
        if form.is_valid():
            form.save()
            return redirect('fbv-toy-list')
    else:
        form = ToyForm(instance=toy)
        
    return render(request, 'toys/toy_form.html', {'form': form})

# class based view

from django.views.generic.edit import UpdateView

class ToyUpdateView(UpdateView):
    model = Toy
    form_class = ToyForm
    success_url = reverse_lazy('cbv-toy-list')
    pk_url_kwarg = 'toy_pk'
    template_name = 'toys/toy_form.html'
```
As with DetailView, for CreateView the default **pk_url_kwarg** is **'pk'** and you'll have to set path to *('cbv-toys/<int:pk\>/edit/'....)* if you don't want to specify. In our case, we specified *'toy_pk'* and so we set path to *('cbv-toys/<int:toy_pk\>/edit/'....)*.

Like above, you can define **form_class**, or specify fields in **fields**. You can specifying the **success_url** using *reverse_lazy* or use url path, or override the **get_success_url**. Also like above, after successful creation, the class based view defaults to calling the **get_absolute_url** method defined in your model, and it defaults to looking up **<model_name\>_form.html**.
<br/>
<br/>

# Delete

Set up the paths:

```python
# urls.py

urlpatterns += [
    path('fbv-toys/<int:toy_pk>/delete/', views.delete_toy,
        name='fbv-toy-delete'),
    path('cbv-toys/<int:toy_pk>/delete/', views.ToyDeleteView.as_view(),
        name='cbv-toy-delete'),
]
```

No forms are needed since we are deleting an item.

Update the views:
```python
# views

# function based view

def delete_toy(request, toy_pk):
    toy = get_object_or_404(Toy, pk=toy_pk)
    if request.method == 'POST':
        toy.delete()
        return redirect('cbv-toy-list')
        
    return render(request, 'toys/toy_confirm_delete.html')

# class based view

from django.views.generic.edit import DeleteView

class ToyDeleteView(DeleteView):
    model = Toy
    pk_url_kwarg = 'toy_pk'
    success_url = reverse_lazy('cbv-toy-list')
    template_name = 'toys/toy_confirm_delete.html'
```
The default **pk_url_kwarg** is **'pk'** and you'll have to set path to *('cbv-toys/<int:pk\>/delete/'....)* if you don't want to specify.

The default template is **<model_name\>_confirm_delete.html** so you don't have to specify.

It is *required* to specify the **success_url** (or override the **get_success_url**) because you will get an error if there isn't something there.

You'll need to make an html file to confirm the deletion:
```html
# in 'toys/templates/toys/'
# toy_confirm_delete.html

<form method="POST"> 
  # make sure to include {% csrf_token %}
  Are you sure you want to delete this item? 
  <input type="submit" value="Yes" /> 
</form> 
```
<br/>

---
**NOTE**

Remember to include <form\> and </form\> and the <input\> button with your {{form}}.
 
---
<br/>

# Initial values

Let's make all of the newly created toys legos unless the input is changed.

Add your urls:
```python
# urls.py

urlpatterns += [
    path('fbv-toys/new-lego/', views.create_lego_toy,
        name='fbv-toy-create-lego'),
    path('cbv-toys/new-lego/', views.LegoToyCreateView.as_view(),
        name='cbv-toy-create-lego'),
]
```
Add to the *toys* application *views.py* file:
```python
# views.py

# function based view

def create_lego_toy(request):
    if request.method == 'POST':
        form = ToyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fbv-toy-list')
    else:
        initial = {
            'name': 'lego'
        }
        form = ToyForm(initial=initial)
    
    return render(request, 'toys/toy_form.html', {'form': form})
    
# class based view

class LegoToyCreateView(CreateView):
    model = Toy
    form_class = ToyForm
    initial = {'name': 'lego'}
    success_url = reverse_lazy('cbv-toy-list')

# alternate class based view

class LegoToyCreateView(CreateView):
    model = Toy
    form_class = ToyForm
    success_url = reverse_lazy('cbv-toy-list')
    
    def get_initial(self):
        return {'name': 'lego'}
```
<br/>

# Making changes after validation

Let's make all newly created toys marked as birthday presents once submitted.

Update your *urls.py* file:
```python
urlpatterns += [
    path('fbv-toys/new-birthday/', views.create_birthday_toy,
        name='fbv-toy-create-birthday'),
    path('cbv-toys/new-birthday/', views.BirthdayToyCreateView.as_view(),
        name='cbc-toy-create-birtday')
]
```
Then *views.py*:
```python
# views.py

# function based view

def create_birthday_toy(request):
    if request.method == 'POST':
        form = ToyForm(request.POST)
        if form.is_valid():
            toy = form.save(commit=False)
            toy.is_birthday_present = True
            toy.save()
            return redirect('fbv-toy-list')
    else:
        form = ToyForm()
    
    return render(request, 'toys/toy_form.html', {'form': form})
    
# class based view

class BirthdayToyCreateView(CreateView):
    model = Toy
    form_class = ToyForm
    success_url = reverse_lazy('cbv-toy-list')
    
    def form_valid(self, form):
        form.instance.is_birthday_present = True
        return super().form_valid(form)
```
