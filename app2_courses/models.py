from django.db import models

# //to slugify and make url endpoints based on chapters
from django.template.defaultfilters import slugify
from django.urls import reverse
# //user model
from django.contrib.auth.models import User
import os

# for redirection
from django.urls import reverse

# Create your models here.

class Standard(models.Model):
    name = models.CharField(max_length = 100, unique = True)
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField(max_length=1000, blank = True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# // code for saving images to media as earlier
# rename the file and store
def save_subject_images(instance, filename):
    upload_to = 'images/'
    # // this is a folder, make a note of folder vs a file
    ext = filename.split('.')[-1]

    if(instance.subject_id):
        # filename = 'User_profile_picture/{}.{}'.format(instance.user.username, ext)
         filename = 'Subject_pictures/{}.{}'.format( instance.subject_id, ext )
        #  using subject_id as it will be unique 

    return os.path.join(upload_to, filename) 
    # what it does? 


class Subject(models.Model):

    subject_id = models.CharField(max_length = 50, unique=True)
    name = models.CharField(max_length = 100)
    slug = models.SlugField(null =True, blank=True)

    standard = models.ForeignKey(Standard, on_delete = models.CASCADE, related_name = 'subjects')
    #  one to many rlation between standard  and subjects as a standard can have many subjects

    image = models.ImageField(upload_to = save_subject_images, blank=True, verbose_name='subject Image')
    description = models.TextField(max_length = 200, blank=True)


    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        self.slug = slugify(self.subject_id)

        super().save(*args, **kwargs)


# /Lesson for 


def saved_lesson(instance, filename):
    upload_to = 'images/'
    # // this is a folder, make a note of folder vs a file
    ext = filename.split('.')[-1]

    if(instance.lesson_id):
        # filename = 'User_profile_picture/{}.{}'.format(instance.user.username, ext)
        filename = 'lesson_files/{}/{}.{}'.format( instance.lesson_id, instance.lesson_id, ext )
        #  using subject_id as it will be unique 

        if(os.path.exists(filename)):
            new_name = str(instance.lesson_id) + str('1')
            filename = 'lesson_images/{}/{}.{}'.format(instance.lesson_id, new_name, ext)

    return os.path.join(upload_to, filename) 


class Lesson(models.Model):
    lesson_id = models.CharField(max_length= 100, unique=True)
    Standard  =models.ForeignKey(Standard, on_delete=models.CASCADE)
    # created_by=models.ForeignKey(User, on_delete=CASCADE)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
# if user is deleted then all data created by it will also be deleted ??

    created_at = models.DateTimeField(auto_now_add  = True)

    subject =  models.ForeignKey(Subject, on_delete = models.CASCADE, related_name = "lessons")
    # a lesson can be connected to only one subject

    name = models.CharField(max_length = 100)
    position = models.PositiveSmallIntegerField(verbose_name = "chapter_no:")
    # position = models.PositiveSmallIntegerField(verbose_name="Chapter no.")
    # chapter number

    slug = models.SlugField(null=True, blank=True)

    video = models.FileField(upload_to=saved_lesson, verbose_name = "video", blank=True, null=True)
    # verbose_name? significance ?
    ppt = models.FileField(upload_to = saved_lesson, verbose_name = 'ppt', blank = True, null=True)
    Notes = models.FileField(upload_to = saved_lesson, verbose_name = 'notes', blank = True, null=True)

    class Meta:
        ordering = ['position']
        # order based on position i.e chapter no;

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


    #  To redirect the user to lesson list after he updates the lessons
    def get_absolute_url(self):
        return reverse('app2_courses:lesson_list', kwargs={'slug':self.subject.slug, 'standard': self.Standard.slug})



#  comments and replies

class Comment(models.Model):
    lesson_name = models.ForeignKey(Lesson, null=True,  on_delete=models.CASCADE, related_name='comments')
    comm_name = models.CharField(max_length = 100, blank=True)

    author = models.ForeignKey(User, on_delete = models.CASCADE)
    body = models.TextField(max_length = 500)
    date_added = models.DateTimeField(auto_now_add = True)


    def save(self, *args, **kwargs):
        self.comm_name = slugify("comment by" + "-"+str(self.author) + str(self.date_added))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.comm_name

    class Meta:
        ordering = ['date_added']  # latest first


class Reply(models.Model):
    comment_name = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name = 'replies')
    reply_body = models.TextField(max_length = 500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "reply to "+ str(self.comment_name.comm_name)

