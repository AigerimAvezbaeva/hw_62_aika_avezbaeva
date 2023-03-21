from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, BaseValidator
from django.db.models.functions import datetime

from tracker_app.models.issues import Issue
from tracker_app.models import Type
from tracker_app.models import Project


def max_len_validator(string):
    if len(string) > 5:
        raise ValidationError('Заголовок должен быть длиннее 5 символов')
    return string


class CustomLenValidator(BaseValidator):
    def __init__(self, limit_value=20):
        message = 'Максимальная длина заголовка %(limit_value)s. Вы ввели %(show_value)s'
        super().__init__(limit_value=limit_value, message=message)

    def compare(self, value, limit_value):
        return limit_value < value

    def clean(self, value):
        return len(value)


class IssueForm(forms.ModelForm):
    summary = forms.CharField(
        validators=(MinLengthValidator(
            limit_value=5,
            message='Заголовок должен быть длиннее 5 символов'),
                    (CustomLenValidator()),))
    type = forms.ModelMultipleChoiceField(queryset=Type.objects.all())


project = forms.ModelChoiceField(queryset=Project.objects.all())


class Meta:
    model = Issue

    fields = ('summary', 'project', 'description', 'status', 'type')
    labels = {
        'summary': 'Заголовок',
        'project': 'Проект',
        'description': 'Описание',
        'status': 'Статус',
        'type': 'Тип задачи'
    }


def clean_title(self):
    summary = self.cleaned_data.get('summary')
    if len(summary) < 2:
        raise ValidationError('Заголовок должен быть длиннее 2 символов')
    if Issue.objects.filter(summary=summary).exists():
        raise ValidationError('Заголовок с таким именем существует')
    return summary


class SearchForm(forms.Form):
    search = forms.CharField(max_length=20, required=False, label='Найти')


class ProjectForm(forms.ModelForm):
    name = forms.CharField(
        validators=(MinLengthValidator(
            limit_value=5,
            message='Заголовок должен быть длиннее 5 символов'),
                    (CustomLenValidator()),))

    class Meta:
        model = Project
        fields = ('name', 'description', 'completed_at')
        labels = {
            'name': 'Заголовок',
            'description': 'Описание',
            'completed_at': 'Дата выполнения'
        }


class ProjectIssueForm(forms.ModelForm):
    summary = forms.CharField(
        validators=(MinLengthValidator(
            limit_value=5,
            message='Заголовок должен быть длиннее 5 символов'),
                    (CustomLenValidator()),))
    type = forms.ModelMultipleChoiceField(queryset=Type.objects.all())
    project = forms.ModelChoiceField(queryset=Project.objects.all(), disabled=True)

    class Meta:
        model = Issue
        fields = ('summary', 'project', 'description', 'status', 'type')
        labels = {
            'summary': 'Заголовок',
            'project': 'Проект',
            'description': 'Описание',
            'status': 'Статус',
            'type': 'Тип задачи'
        }
