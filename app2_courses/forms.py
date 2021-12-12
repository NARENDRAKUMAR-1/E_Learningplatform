from django import forms
from .models import Lesson, Comment, Reply

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        # fields = ('__all__') # all the fields will be shown
        
        # specify the needed fields only
        fields = ('lesson_id','name', 'position', 'video', 'ppt', 'Notes')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        labels = {
            'body' : 'comment'
        }

        widgets={
            'body':forms.Textarea(attrs={'class':'form-control', 'rows':4, 'cols':70, 'placeholder':"enter your comment here"}),
        }

        
    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop('request', None)
    #     super(CommentForm, self).__init__(*args, **kwargs)

    # // no need after we add FormView in views of LessonDetail



class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('reply_body',)
        

        widgets = {
            'reply_body':forms.Textarea(attrs={'class':'form-control', 'rows':2, 'cols':10, 'placeholder':'enter your reply here' })
        }

    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop('request', None)
    #     super(ReplyForm, self).__init__(*args, **kwargs)

