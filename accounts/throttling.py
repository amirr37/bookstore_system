from rest_framework.throttling import SimpleRateThrottle


class OTPLoginPostThrottle(SimpleRateThrottle):
    rate = '5/2m'  # 5 requests per 2 minutes for POST requests

    def get_cache_key(self, request, view):
        # Customize the cache key as needed to uniquely identify the request.
        # You can use request.user, request.META, or any other request attributes.
        return f'{self.get_ident(request)}-{view.__class__.__name__}-post'


class OTPLoginPutThrottle(SimpleRateThrottle):
    rate = '10/h'  # 10 requests per hour for PUT requests

    def get_cache_key(self, request, view):
        # Customize the cache key as needed to uniquely identify the request.
        # You can use request.user, request.META, or any other request attributes.
        return f'{self.get_ident(request)}-{view.__class__.__name__}-post'
