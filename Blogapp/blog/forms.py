from django import forms
from .models import Comments, Post


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to  = forms.EmailField( required=True)
    comments = forms.CharField( max_length=50, required=False,widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comments
        fields = ('name', 'email','body')

class SearchForm(forms.Form):
    query = forms.CharField(max_length=50)


class Postform(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','body','status','tags']
        