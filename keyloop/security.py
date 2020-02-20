from zope.interface import implementer

from pyramid.authentication import IAuthenticationPolicy
from pyramid.authentication import CallbackAuthenticationPolicy

# from pyramid.authentication import Everyone


from webob.cookies import CookieProfile


from keyloop.utils.signing import create_signed, retrieve_signed, BadSignatureError


class CookieProfileCache:
    def __init__(self, prefix="kloop", max_age=None):
        self.prefix = "{}_".format(prefix)
        self._cache = {}
        self.max_age = max_age

    def get_profile(self, realm):
        if realm not in self._cache:
            self._cache[realm] = CookieProfile(
                self.prefix + realm, max_age=self.max_age
            )
        return self._cache.get(realm)

    def cookie_name(self, realm):
        return self.prefix + realm


@implementer(IAuthenticationPolicy)
class KeyLoopAuthenticationPolicy(CallbackAuthenticationPolicy):
    def __init__(self, secret, cookie_prefix="kloop", max_age=None):
        self.secret = secret
        self.profiles = CookieProfileCache(prefix=cookie_prefix, max_age=max_age)

    # def _is_authorized_api_request(self, request):
    #     if self.auth_header_key in request.headers:
    #         access_token = request.headers.get(self.auth_header_key)
    #         storage = request.wla_storage
    #         return storage.check_api_key(access_token)
    #     return None

    # def _has_authorized_api_request_principals(self, request):
    #     partner = self._is_authorized_api_request(request)
    #     if partner:
    #         principals = [WLAuthenticated, "wl:p:{}".format(partner)]
    #         storage = request.wla_storage
    #         principals_ = [
    #             "wl:{}".format(i) for i in storage.get_principals(partner=partner)
    #         ]
    #         return principals + principals_
    #     return None

    def unauthenticated_userid(self, request):
        if not hasattr(request, "realm"):
            return None

        cookie = request.cookies.get(self.profiles.cookie_name(request.realm))

        if cookie is None:
            return None

        try:
            return retrieve_signed(cookie, self.secret)
        except BadSignatureError:
            return None

    # def effective_principals(self, request):
    #     principals = set([Everyone])

    #     effective_principals.append(Authenticated)
    #     effective_principals.append(userid)
    #     effective_principals.extend(groups)

    #     # api_principals = self._has_authorized_api_request_principals(request)
    #     # if api_principals:
    #     #     principals.update(api_principals)
    #     return list(principals)

    def remember(self, request, principal, **kw):

        cookie_profile = self.profiles.get_profile(request.context.realm)

        signed = create_signed(principal, self.secret)
        prof = cookie_profile(request)
        return prof.get_headers(signed, **kw)

        # kw = {}
        # kw["domains"] = domains
        # if max_age is not None:
        #     kw["max_age"] = max_age

        # from webob.cookies import CookieProfile
        # cp = CookieProfile('debonzi_c')
        # prof = cp(request)
        # prof.get_headers('123123', **kw)
        # >>> [('Set-Cookie', 'debonzi_c=IjEyMzEyMyI=; Path=/')]

    def forget(self, request):
        if not hasattr(request, "realm"):
            return []

        cookie_profile = self.profiles.get_profile(request.realm)

        prof = cookie_profile(request)
        return prof.get_headers(None)
