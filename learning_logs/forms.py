from django import forms

from .models import Entry, Topic


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('text',)
        labels = {'text': 'Название темы'}


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ('text',)
        labels = {'text': 'Запись'}
        widgets = {'text': forms.Textarea(attrs={'rows': 8})}
