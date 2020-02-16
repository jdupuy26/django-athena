from rest_framework import serializers

from .models import Branch
from .models import Code
from .models import Configuration
from .models import Fork
from .models import Repo


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ("name", "fork", "repo", "data")


class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = ("name", "path")


class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = ("name", "code")


class ForkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fork
        fields = ("name", "url", "data", "code", "repo")


class RepoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repo
        fields = ("name", "url", "data")
