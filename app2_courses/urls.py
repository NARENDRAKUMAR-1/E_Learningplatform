from django.urls import path # //

from . import views

app_name = 'app2_courses'

urlpatterns = [
    path('', views.StandardListView.as_view(), name='standard_list'),
    path('<slug:slug>/', views.Subject_List_View.as_view(), name='subject_list'),
    # slug used , great

    path('<str:standard>/<slug:slug>', views.LessonListView.as_view(), name='lesson_list'),
    # Note that to uniquely track the page we are using two slugs 1 for standard and another for the slug i.e lesson


    # path('user_logout', views.user_logout, name='user_logout'),

    path('<str:standard>/<str:subject>/<slug:slug>', views.LessonDetailView.as_view(), name='lesson_detail'),
    

    # //CRUD new lesson add
    # \// modify the slug
    path('<str:standard>/<str:slug>/create/', views.LessonCreateView.as_view(), name='lesson_create'),
    #  / is important between

    path('<str:standard>/<str:subject>/<str:slug>/update/', views.LessonUpdateView.as_view(), name='lesson_update'),


    path('<str:standard>/<str:subject>/<str:slug>/delete/', views.LessonDeleteView.as_view(), name='lesson_delete'),




     
]