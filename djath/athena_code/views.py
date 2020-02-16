from rest_framework import generics

from .models import Branch
from .models import Code
from .models import Configuration
from .models import Fork
from .models import Repo
from .serializers import BranchSerializer
from .serializers import CodeSerializer
from .serializers import ConfigurationSerializer
from .serializers import ForkSerializer
from .serializers import RepoSerializer


# Create your views here.
# def index(request):
#     """ View function for the athena_code page of the site."""
#     #
#     # # Generate counts of some of the main objects
#     # num_codes = Code.objects.all().count()
#     # num_configurations = Configuration.objects.all().count()
#     #
#     # context = {"num_codes": num_codes, "num_configurations": num_configurations}
#     #
#     # # render HTML template index.html with the data in context
#     # return render(request, "index.html", context=context)
#     pass


# ---------- API VIEWS
class ReposListCreate(generics.ListCreateAPIView):
    queryset = Repo.objects.all()
    serializer_class = RepoSerializer


class ForksListCreate(generics.ListCreateAPIView):
    queryset = Fork.objects.all()
    serializer_class = ForkSerializer


class BranchesListCreate(generics.ListCreateAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class CodesListCreate(generics.ListCreateAPIView):
    queryset = Code.objects.all()
    serializer_class = CodeSerializer


class ConfigurationsListCreate(generics.ListCreateAPIView):
    queryset = Configuration.objects.all()
    serializer_class = ConfigurationSerializer


# --------- Other Views
# class RepoListView(generic.ListView):
#     model = Repo
#
#
# class RepoDetailView(generic.DetailView):
#     model = Repo
#
#
# class ForkListView(generic.ListView):
#     model = Fork
#
#
# class ForkDetailView(generic.DetailView):
#     model = Fork
#
#
# class BranchListView(generic.ListView):
#     model = Branch
#
#
# class BranchDetailView(generic.DetailView):
#     model = Branch
#
#
# class CodeListView(generic.ListView):
#     model = Code
#
#     def get_context_data(self, **kwargs):
#         context = super(CodeListView, self).get_context_data(**kwargs)
#         context["configurations"] = Configuration.objects.all()
#         return context
#
#
# class CodeDetailView(generic.DetailView):
#     model = Code
#
#
# class ConfigurationListView(generic.ListView):
#     model = Configuration
#
#
# class ConfigurationDetailView(generic.DetailView):
#     model = Configuration
#
#
# class ConfigurationCreate(generic.CreateView):
#     model = Configuration
#     fields = "__all__"
#
#
# class ConfigurationUpdate(generic.UpdateView):
#     model = Configuration
#     fields = "__all__"
