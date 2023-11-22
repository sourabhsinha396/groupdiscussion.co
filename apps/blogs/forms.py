from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.utils.text import slugify

from .models import Blog


class BlogModelForm(forms.ModelForm):

    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    content = forms.CharField(widget=CKEditorUploadingWidget(config_name='minimal'))
    
    class Meta:
        model = Blog
        fields = ['title', 'slug', 'category', 'exam', 'image', 'description', 'content']

    def clean(self):
        super(BlogModelForm, self).clean()
        title = self.cleaned_data.get('title')
        slug = self.cleaned_data.get('slug')

        if not slug:
            self.cleaned_data['slug'] = slugify(title)

        return self.cleaned_data
