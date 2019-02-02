from athena_code.models import Repo, Fork, Branch, Code, Configuration

from django.contrib import admin

# Register your models here.
admin.site.register(Repo)
admin.site.register(Fork)
admin.site.register(Branch)
admin.site.register(Code)
admin.site.register(Configuration)