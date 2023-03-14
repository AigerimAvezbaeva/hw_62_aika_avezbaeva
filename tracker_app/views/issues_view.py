from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, DetailView, CreateView, UpdateView, DeleteView
from tracker_app.models.issues import Issue

from tracker_app.forms import IssueForm


class IssueDetail(DetailView):
    template_name = 'issue_detail.html'
    model = Issue


class IssueAddView(LoginRequiredMixin, CreateView):
    template_name = 'add_issue.html'
    model = Issue
    form_class = IssueForm

    def get_success_url(self):
        return reverse('issue_detail', kwargs={'pk': self.object.pk})


class IssueUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'update_issue.html'
    model = Issue
    form_class = IssueForm

    def get_success_url(self):
        return reverse('issue_detail', kwargs={'pk': self.object.pk})


class IssueDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'delete_issue.html'
    model = Issue
    success_url = reverse_lazy('index')

