from athena_code.models import Branch
from athena_code.models import Code
from athena_code.models import Configuration
from athena_code.models import Fork
from athena_code.models import Repo
from django.contrib import admin

# Register your models here.
admin.site.register(Repo)
admin.site.register(Fork)
admin.site.register(Branch)
admin.site.register(Code)
admin.site.register(Configuration)
