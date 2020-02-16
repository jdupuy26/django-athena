from django.urls import path

from . import views

urlpatterns = [
    path("api/repos/", views.ReposListCreate.as_view()),
    path("api/branches/", views.BranchesListCreate.as_view()),
    path("api/forks/", views.ForksListCreate.as_view()),
    path("api/codes/", views.CodesListCreate.as_view()),
    path("api/configurations/", views.ConfigurationsListCreate.as_view()),
    # path("", views.index, name="index"),
    # path("repos/", views.RepoListView.as_view(), name="repos"),
    # path("repos/<int:pk>", views.RepoDetailView.as_view(), name="repo-detail"),
    # path("forks/", views.ForkListView.as_view(), name="forks"),
    # path("forks/<int:pk>", views.ForkDetailView.as_view(), name="fork-detail"),
    # path("branches/", views.BranchListView.as_view(), name="branches"),
    # path("branches/<int:pk>", views.BranchDetailView.as_view(), name="branch-detail"),
    # path("codes/", views.CodeListView.as_view(), name="codes"),
    # path("codes/<int:pk>", views.CodeDetailView.as_view(), name="code-detail"),
    # path(
    #     "codes/<int:pk>-clone",
    #     views.CodeDetailView.as_view(template_name="athena_code/code_clone_detail.html"),
    #     name="code-clone-detail",
    # ),
    # path("configurations/", views.ConfigurationListView.as_view(), name="configurations"),
    # path(
    #     "configurations/<int:pk>",
    #     views.ConfigurationDetailView.as_view(),
    #     name="configuration-detail",
    # ),
    # path(
    # "configuration/create/", views.ConfigurationCreate.as_view(), name="configuration-create"
    # ),
    # path(
    #     "configuration/<int:pk>/update/",
    #     views.ConfigurationUpdate.as_view(),
    #     name="configuration-update",
    # ),
]
