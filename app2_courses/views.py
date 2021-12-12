from django.shortcuts import render, HttpResponse


# // to work with the class based views
from django.views.generic import (TemplateView, DetailView, ListView, FormView)

# to work with the CRUD functionality
from django.views.generic import ( CreateView, UpdateView, DeleteView )

from .models import Standard, Subject, Lesson

# // for forms
from .forms import LessonForm , CommentForm, ReplyForm

from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

# Create your views here.


# def index1(request):
#     return HttpResponse(" working? ")


class StandardListView(ListView):
    context_object_name = 'standards'
    model = Standard
    template_name = 'app2_courses/standard_list_view.html'


class Subject_List_View(DetailView):
    context_object_name = 'standards'
    #  context_object_name  keep this name as it is
    model = Standard
    template_name = 'app2_courses/subject_list_view.html'


class LessonListView(DetailView):
    context_object_name = 'subjects'
    #  context_object_name  keep this name as it is
    model = Subject
    template_name = 'app2_courses/lesson_list_view.html'


class LessonDetailView(DetailView, FormView):  # add FormView here to work with the comments and replies
    context_object_name = 'lessons'
    #  context_object_name  keep this name as it is
    model = Lesson
    template_name = 'app2_courses/lesson_detail_view.html'   

    # for comments and replies
    form_class = CommentForm
    second_form_class = ReplyForm



    def get_context_data(self, **kwargs):
        context = super(LessonDetailView, self).get_context_data(**kwargs)
        if 'form' not in context:
            # context['form'] = self.form_class(request=self.request)
            # this requires to change the __init__ function of reply form in forms.py

            context['form'] = self.form_class() # no need of request when we use the FormView

        if 'form2' not in context:
            # context['form2'] = self.second_form_class(request=self.request)
       # context['comments'] = Comment.objects.filter(id=self.object.id)

            context['form2'] = self.second_form_class()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'form' in request.POST:
            # form_class = self.get_form_class()
            form_class = self.form_class
            form_name = 'form'
        else:
            form_class = self.second_form_class
            form_name = 'form2'

        form = self.get_form(form_class)
        # print("the form name is : ", form)
        # print("form name: ", form_name)
        # print("form_class:",form_class)

        if form_name=='form' and form.is_valid():
            print("comment form is returned")
            return self.form_valid(form)
        elif form_name=='form2' and form.is_valid():
            print("reply form is returned")
            return self.form2_valid(form)


    def get_success_url(self):
        self.object = self.get_object()
        standard = self.object.Standard
        subject = self.object.subject
        # stay
        return reverse_lazy('app2_courses:lesson_detail',kwargs={'standard':standard.slug,
                                                             'subject':subject.slug,
                                                             'slug':self.object.slug})



    def form_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.lesson_name = self.object.comments.name
        fm.lesson_name_id = self.object.id
        fm.save()
        return HttpResponseRedirect(self.get_success_url())

    def form2_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.comment_name_id = self.request.POST.get('comment.id')
        fm.save()
        return HttpResponseRedirect(self.get_success_url())
        




#  CRUD part
class LessonCreateView(CreateView):
    form_class =  LessonForm
    context_object_name = 'subject'
    model = Subject
    template_name = 'app2_courses/lesson_create.html'


    # override the default form_valid function of the CreateView class as per our need
    # and store the inputs in our db


    def get_success_url(self):
        self.object = self.get_object()
        standard = self.object.standard
        return reverse_lazy('app2_courses:lesson_list',
        kwargs={'standard':standard.slug, 'slug':self.object.slug})  # ??
    
    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.created_by = self.request.user
        fm.Standard = self.object.standard
        fm.subject = self.object
        fm.save()
        return HttpResponseRedirect(self.get_success_url())

'''
    def form_valid(self, form, *args, **kwargs): 
        self.object = self.get_object()
        fm = form.save(commit = False)
        fm.created_by = self.request.user
        fm.standard = self.object.standard # foreign key relation with the standard
        # use fm.Standard
        # understand where to use the modelname and where to use the var name
        fm.subject = self.object
        fm.save()

        return HttpResponseRedirect(self.get_success_url() )  # define a function for get_success_url
'''


# updating

class LessonUpdateView(UpdateView):
    fields = ('name','position', 'video', 'ppt', 'Notes')
    model = Lesson
    template_name = 'app2_courses/lesson_update.html'
    context_object_name = 'lessons' #lessons ?? why not lesson


class LessonDeleteView(DeleteView):
    model = Lesson
    context_object_name = 'lessons'
    template_name = 'app2_courses/lesson_delete.html'

    # once deleted where to redirect the user 

    def get_success_url(self):
        standard = self.object.Standard
        subject = self.object.subject #Standard caps subject small
        return reverse_lazy('app2_courses:lesson_list', kwargs={'standard':standard.slug, 'slug':subject.slug})







