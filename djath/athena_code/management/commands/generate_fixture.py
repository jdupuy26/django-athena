import json

import requests
from athena_code.models import Branch
from athena_code.models import Code
from athena_code.models import Fork
from athena_code.models import Repo
from django.conf import settings
from django.core.management.base import BaseCommand

# get GH url for api request
GH_URLS = settings.GH_URLS
GH_USERS = settings.GH_USERS


class Command(BaseCommand):
    help = "Generate fixture to populate db with initial values"

    def handle(self, *args, **kwargs):
        # get the repo
        for GH_URL in GH_URLS:
            rr = requests.get(GH_URL)
            if rr.ok:
                repo = json.loads(rr.text or rr.content)
                myrepo, create = Repo.objects.get_or_create(
                    name=repo["name"], url=repo["html_url"], data=repo
                )
                # get all the forks
                rf = requests.get(GH_URL + "/forks" + "?page2&per_page=100")
                if rf.ok:
                    forks = json.loads(rf.text or rf.content)
                    for fork in forks:
                        if fork["owner"]["login"] in GH_USERS:
                            mycode, create = Code.objects.get_or_create(
                                name=fork["full_name"],
                                path=settings.BASE_DIR + "/" + fork["full_name"].replace("/", "-"),
                            )
                            myfork, create = Fork.objects.get_or_create(
                                name=fork["full_name"],
                                url=fork["html_url"],
                                repo=myrepo,
                                code=mycode,
                                data=fork,
                            )
                            self.stdout.write(
                                "[generate_fixture]: Added fork '{}' to the db".format(myfork.name)
                            )
                            # now get branches of the fork
                            rb = requests.get(myfork.data["branches_url"].replace("{/branch}", ""))
                            if rb.ok:
                                branches = json.loads(rb.text or rb.content)
                                for branch in branches:
                                    mybranch, create = Branch.objects.get_or_create(
                                        name=fork["owner"]["login"] + "-" + branch["name"],
                                        repo=myrepo,
                                        fork=myfork,
                                        data=branch,
                                    )
                            else:
                                self.stdout.write(
                                    "[generate_fixture]: Request at url: '{}' not valid".format(
                                        myfork.data["branches_url"].replace("{/branch}", "")
                                    )
                                )
                else:
                    self.stdout.write(
                        "[generate_fixture]: Request at url: '{}' not valid".format(
                            GH_URL + "/forks"
                        )
                    )
            else:
                self.stdout.write(
                    "[generate_fixture]: Request at url: '{}' not valid".format(GH_URL)
                )
