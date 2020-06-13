from django import forms
from .models import *

class DogInfo(forms.ModelForm):
    class Meta:
        model = Image_db
        fields = ['tag', 'image']

class SearchDogForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SearchDogForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Image_db
        fields = ['tag', 'image']
        labels = {
            'tag': 'Ten giong cho',
            'image': 'Anh tim kiem',

        }
        help_texts = {
            'tag': 'tag cua loai cho muon tim thong tin.',
            'image': 'anh cua loai cho muon tim thong tin.',
        }


class SearchLostDogForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SearchLostDogForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Image_searchPost
        fields = ['dogImage', 'species', 'weight', 'height',
                  'color', 'accessory', 'location', 'time', 'status']
        widgets = {
            'time': forms.DateInput(attrs={'class':'datetime-input', 'type': 'date'}),
        }
        labels = {
            'species': 'Ten giong cho',
            'dogImage': 'Anh tim kiem',

        }


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Image_addPost
        fields = ['dogImage', 'species', 'weight', 'height',
                  'color', 'accessory', 'location', 'time', 'status']
        widgets = {
            'time': forms.DateInput(attrs={'class':'datetime-input', 'type': 'date'}),
        }
        labels = {
            'species': 'Ten giong cho',
            'dogImage': 'Anh tim kiem',
        }
