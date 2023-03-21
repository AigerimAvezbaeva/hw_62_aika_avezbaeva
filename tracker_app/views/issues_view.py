from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from tracker_app.models.issues import Issue

from tracker_app.forms import IssueForm


class GetPermissionMixin(PermissionRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name__in=['Капитан (Team Lead)', 'Менеджер проекта (Project Manager)', 'Разработчик (Developer)']).exists()


class IssueDetail(DetailView):
    template_name = 'issue_detail.html'
    model = Issue


class IssueAddView(GetPermissionMixin, CreateView):
    template_name = 'add_issue.html'
    model = Issue
    form_class = IssueForm
    permission_required = 'tracker_app.change_issue'

    def get_success_url(self):
        return reverse('issue_detail', kwargs={'pk': self.object.pk})


class IssueUpdateView(GetPermissionMixin, UpdateView):
    template_name = 'update_issue.html'
    model = Issue
    form_class = IssueForm

    def test_func(self):
        return self.request.user.groups.filter(
            name__in=['Капитан (Team Lead)', 'Менеджер проекта (Project Manager)', 'Разработчик (Developer)']).exists()

    def get_success_url(self):
        return reverse('issue_detail', kwargs={'pk': self.object.pk})


class IssueDeleteView(GetPermissionMixin, DeleteView):
    template_name = 'delete_issue.html'
    model = Issue
    success_url = reverse_lazy('index')
