from rest_framework import serializers

from .models import Branch
from .models import Code
from .models import Configuration
from .models import Fork
from .models import Repo


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"


class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = "__all__"


class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = "__all__"


class ForkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fork
        fields = "__all__"


class RepoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repo
        fields = "__all__"
