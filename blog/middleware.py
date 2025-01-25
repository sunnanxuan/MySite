from threading import local

_thread_locals = local()

def get_current_request():
    """获取当前线程中的请求对象"""
    return getattr(_thread_locals, 'request', None)

class CRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.request = request
        response = self.get_response(request)
        return response