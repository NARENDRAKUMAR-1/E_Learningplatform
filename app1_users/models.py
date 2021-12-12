from django.db import models

# Create your models here.

# //
from django.contrib.auth.models import User

# // handling and storing the images 
import os

# rename the file and store
def path_and_rename(instance, filename):
    upload_to = 'images/'
    # // this is a folder, make a note of folder vs a file
    ext = filename.split('.')[-1]

    if(instance.user.username):
        # filename = 'User_profile_picture/{}.{}'.format(instance.user.username, ext)
         filename = 'User_Profile_Pictures/{}.{}'.format( instance.user.username, ext )

    return os.path.join(upload_to, filename) 
    # what it does?  

# create a user model with a custom name other than user as it is already been used by the django

class user_profile(models.Model):
    # username = models.OneToOneField(User, on_delete=models.CASCADE)
    #  make it user

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length = 100, blank=True)

    profile_pic = models.ImageField( upload_to=  path_and_rename, verbose_name= 'profie picture' ,blank=True)
    
    # //user type
    teacher = 'teacher'
    student = 'student'
    parent = 'parent'

    user_types = [
        (teacher, 'teacher'),
        (student, 'student'),
        (parent, 'parent'),
    ]

    user_type = models.CharField(max_length = 15, choices=user_types, default=student)

    def __str__(self):
        return self.user.username
