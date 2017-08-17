from django.conf import settings
from functools import wraps


class MonkeyPatchMiddleware(object):
    ''' Ensures that our monkey patching only gets called after it is safe to do so.'''

    def process_request(self, request):
        do_monkey_patch()


def do_monkey_patch():
    fix_sitetree_check_access_500s()
    never_cache_login_page()

    # Remove this function from existence
    global do_monkey_patch
    do_monkey_patch = lambda: None


def fix_sitetree_check_access_500s():
    ''' django-sitetree has a bug: https://github.com/idlesign/django-sitetree/pull/167/files
    -- it swallows the cause of all 500 errors. This swallows KeyErrors from
    the failing function. '''

    from sitetree.sitetreeapp import SiteTree

    old_check_access = SiteTree.check_access

    @wraps(SiteTree.check_access)
    def check_access(self, *a, **k):
        try:
            return old_check_access(self, *a, **k)
        except KeyError:
            return False

    SiteTree.check_access = check_access

def never_cache_login_page():
    from django.views.decorators.cache import never_cache
    from account.views import LoginView
    LoginView.get = never_cache(LoginView.get)
