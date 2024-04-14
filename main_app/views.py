import os
import uuid
import boto3

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Cat, Toy, Photo

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse

from .forms import FeedingForm



# Create your views here.
def home(request):
   return render(request, 'home.html')

def about(request):
   return render(request, 'about.html')

@login_required
def cats_index(request):
   cats = Cat.objects.filter(user=request.user)
   #Another Query
   # cats = request.user.cat_set.all()
   return render(request, 'cats/index.html', {
      'cats': cats
   })

@login_required
def cats_detail(request, cat_id):
   cat = Cat.objects.get(id=cat_id)
   feeding_form = FeedingForm()
   current_toy_ids = cat.toys.all().values_list('id')
   available_toys = Toy.objects.exclude(id__in=current_toy_ids)
   return render(request, 'cats/detail.html', {
      'cat': cat, 
      'feeding_form': feeding_form,
      'available_toys': available_toys,
   })
@login_required
def add_feeding(request, cat_id):
   feeding_form = FeedingForm(request.POST) # request.POST is equivalent for req.body
   if feeding_form.is_valid():
      new_feeding = feeding_form.save(commit=False)
      new_feeding.cat_id = cat_id
      new_feeding.save()
   return redirect('detail', cat_id=cat_id)
      


 
#GET/ /cats/create AND POST /cats/create
# CatCreate class inherit from two super class LoginRequiredMixin and CreateView
# inheriting from superclass LoginRequiredMixin protects class-based views
class CatCreate(LoginRequiredMixin, CreateView):
   model = Cat
   fields = ['name', 'breed', 'description', 'age']
    # Dont handle toys in create

   #we want only authenticated user be able to create cat
   def form_valid(self, form):
      # self.request.user is the logged user, remeber user object is available when we login
      form.instance.user = self.request.user
      # let the CreateView's form_valid method
      #do its regular work which is saving the model in DB & redirect
      return super().form_valid(form)
   

class CatUpdate(LoginRequiredMixin, UpdateView):
   model = Cat
   fields = ['breed', 'description', 'age']

class CatDelete(LoginRequiredMixin, DeleteView):
   model = Cat
   success_url = '/cats/' #TODO get reverse function work

# Toy CRUD ###############################

class ToyList(LoginRequiredMixin, ListView):
   model = Toy

class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy

class ToyCreate(LoginRequiredMixin, CreateView):
   model = Toy
   fields = '__all__'

class ToyUpdate(LoginRequiredMixin, UpdateView):
   model = Toy
   fields = '__all__'

class ToyDelete(LoginRequiredMixin, DeleteView):
   model = Toy
   success_url = '/toys/' #TODO: dont hardcode ---use Reverse

@login_required
def add_toy(request, cat_id, toy_id):
   Cat.objects.get(id=cat_id).toys.add(toy_id)
   return redirect('detail', cat_id=cat_id)
@login_required
def remove_toy(request, cat_id, toy_id):
   Cat.objects.get(id=cat_id).toys.remove(toy_id)
   return redirect('detail', cat_id=cat_id)


######## Photo CRUD #############
@login_required
def add_photo(request, cat_id):
   photo_file = request.FILES.get('photo-file', None)
   if photo_file:
      s3 = boto3.client('s3')
      # Need a unique 'key' (filename)
      # It needs to keep the same file extension
      # of the file that was uploaded(.png, .jpeg, etc)
      # First part of this command generate a unique identifier +
      # and second part finds the . in the file name(ex: cat01.png and slice .png using : until the end)
      key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
      try:
         bucket = os.environ['S3_BUCKET']
         s3.upload_fileobj(photo_file, bucket, key)
         #Build the full url string
         url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
         Photo.objects.create(url=url, cat_id=cat_id)
      except Exception as e:
         print('An error occurred uploading file to S3')
         print(e)
   return redirect('detail', cat_id=cat_id)


def signup(request):
   error_message = ''
   if request.method == 'POST':
      form = UserCreationForm(request.POST)
      if form.is_valid():
         # save the user in DB
         user = form.save()
         # Authomatically log in the new user
         login(request, user)
         return redirect('index') # redirect send a GET request
      else:
         error_message = 'Invalid sign up - try again'
    #  # A bad POST or a GET request, so render signup.html with an empty form
   form = UserCreationForm()
   context = {'form': form, 'error_message': error_message}
   return render(request, 'registration/signup.html', context)
()