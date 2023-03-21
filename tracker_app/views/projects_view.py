from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from tracker_app.models import Project
from tracker_app.forms import ProjectForm
from tracker_app.models import Issue

from tracker_app.forms import ProjectIssueForm


class ProjectsIndexView(ListView):
    template_name = 'projects_index.html'

    model = Project
    context_object_name = 'projects'
    ordering = ('created_at',)
    paginate_by = 10
    paginate_orphans = 1


class ProjectAddView(CreateView):
    template_name = 'add_project.html'
    model = Project
    form_class = ProjectForm

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.pk})


class ProjectDetail(DetailView):
    template_name = 'project_detail.html'
    model = Project


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'update_project.html'
    form_class = ProjectForm
    model = Project

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.pk})


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'project_delete.html'
    model = Project
    success_url = reverse_lazy('project_index')


class ProjectTasksView(LoginRequiredMixin, DetailView):
    template_name = 'project_tasks.html'
    model = Project
    context_object_name = 'project'
    ordering = ('created_at',)
    paginate_by = 10
    paginate_orphans = 1


class ProjectIssueCreateView(CreateView):
    model = Issue
    template_name = 'project_task_create.html'
    form_class = ProjectIssueForm


    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        issue = form.save(commit=False)
        issue.project = project
        issue.save()
        return redirect('issue_detail', pk=issue.pk)
