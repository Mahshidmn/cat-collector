from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

#  A tuple of 2-tuples, we use tuple because we dont change the data in it 
MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner'),
)

 
class Toy(models.Model):
    name = models.CharField(max_length=256)
    color = models.CharField(max_length=16)

    def get_absolute_url(self):
        return reverse('toys_detail', kwargs={'pk': self.id }) # pk is equal to toy.id, Django prefers pk
    
    def __str__(self):
        return self.name

# Create your models here.
# Models are entities in ERD
class Cat(models.Model):
    #get translated as Db Table rows
    name = models.CharField(max_length=256)
    breed = models.CharField(max_length=256)
    description = models.TextField(max_length=256)
    age = models.IntegerField()
    toys = models.ManyToManyField(Toy)
    # add user_id FK column
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
       return self.name
    
    # url method that we use in base.html is a DTL and 
    # we dont model doesnt have access to it so we use rerverse method
    # Django magic to get the URL by examining the corresoponding path()
    # in simple word, go back to detail url and replace cat_id with self.id
    def get_absolute_url(self):
        return reverse('detail', kwargs={'cat_id': self.id})
    
# we have to define Cat model before Feedin model
class Feeding(models.Model):
      # the first optional positional argument overrides the label 'date'
    date = models.DateField('Feeding Date')
    meal = models.CharField(
        max_length=1, #max_length=len('Breakfast')
        choices = MEALS,
        default = MEALS[0][0]
    )
    # we want deleting a cat will delete its associated data in join  table as well
    # for example if delete a cat before deleting its Feedings without CASCADE , we get error
    # In 1:M we do this in child, and in M:M we do it in one of the models, no defrence
    cat = models.ForeignKey(Cat, on_delete = models.CASCADE)


    # get_meal_display is a Django function that get meal as tuple and 
    # returns the value for 'B' which is 'Breakfast' in the 2-tuple
    def __str__(self):
        return f"{ self.get_meal_display() } on { self.date }"
    
    class Meta:
        ordering = ['-date'] # order feeding from most recent to least
    

class Photo(models.Model):
    url = models.CharField(max_length=200)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    def __str__ (self):
        return f"Photo for cat_id: {self.cat_id} @{self.url}"



        