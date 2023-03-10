from django.urls import path
from tracker_app.views.base import IndexView
from tracker_app.views.issues_view import IssueAddView, IssueDetail, IssueUpdateView, IssueDeleteView
from tracker_app.views.projects_view import ProjectsIndexView, ProjectAddView, ProjectDetail, ProjectUpdateView, ProjectDeleteView, ProjectTasksView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('projects/', ProjectsIndexView.as_view(), name='project_index'),
    path('issue/', IndexView.as_view(), name='index'),
    path('issue/add/', IssueAddView.as_view(), name='add_issue'),
    path('projects/add/', ProjectAddView.as_view(), name='add_project'),
    path('issue/<int:pk>', IssueDetail.as_view(), name='issue_detail'),
    path('projects/<int:pk>', ProjectDetail.as_view(), name='project_detail'),
    path('issue/<int:pk>/update', IssueUpdateView.as_view(), name='update_issue'),
    path('projects/<int:pk>/update', ProjectUpdateView.as_view(), name='update_project'),
    path('projects/<int:pk>/tasks', ProjectTasksView.as_view(), name='project_tasks'),
    path('issue/<int:pk>/delete', IssueDeleteView.as_view(), name='delete_issue'),
    path('projects/<int:pk>/delete', ProjectDeleteView.as_view(), name='delete_project'),
]
