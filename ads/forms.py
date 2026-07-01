from django import forms

from ads.models import Ad, Comment


class CreateForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Ad
        fields = ["title", "price", "content", "image", "tags"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
