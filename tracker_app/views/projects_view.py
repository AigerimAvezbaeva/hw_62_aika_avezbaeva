from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from tracker_app.models import Project
from tracker_app.forms import ProjectForm
from tracker_app.models import Issue

from tracker_app.forms import ProjectIssueForm


class GetPermissionMixin(PermissionRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(
            name__in=['Капитан (Team Lead)', 'Менеджер проекта (Project Manager)', 'Разработчик (Developer)']).exists()


class ProjectsIndexView(ListView):
    template_name = 'projects_index.html'

    model = Project
    context_object_name = 'projects'
    ordering = ('created_at',)
    paginate_by = 10
    paginate_orphans = 1


class ProjectAddView(GetPermissionMixin, CreateView):
    template_name = 'add_project.html'
    model = Project
    form_class = ProjectForm
    groups = ['Капитан (Team Lead)']
    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.pk})



class ProjectDetail(DetailView):
    template_name = 'project_detail.html'
    model = Project


class ProjectUpdateView(GetPermissionMixin, UpdateView):
    template_name = 'update_project.html'
    form_class = ProjectForm
    model = Project

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.pk})


class ProjectDeleteView(GetPermissionMixin, DeleteView):
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


class ProjectIssueCreateView(GetPermissionMixin, CreateView):
    template_name = 'project_task_create.html'
    model = Issue
    form_class = ProjectIssueForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs.get('pk')
        project = Project.objects.get(id=project_id)
        context['project'] = project
        return context

    def form_valid(self, form):
        project_id = self.kwargs.get('pk')
        project = Project.objects.get(id=project_id)
        form.instance.project = project
        return super().form_valid(form)

    def get_initial(self):
        project_id = self.kwargs.get('pk')
        project = Project.objects.get(id=project_id)
        return {'project': project}

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse('project_tasks', kwargs={'pk': pk})
