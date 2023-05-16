# from .models import Visitor
#
# class VisitorTrackingMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         ip_address = self.get_client_ip(request)
#         visited_page = request.get_full_path()
#         if ip_address:
#             Visitor.objects.create(ip_address=ip_address, visited_page=visited_page)
#         response = self.get_response(request)
#         return response
#
#     def get_client_ip(self, request):
#         x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#         if x_forwarded_for:
#             ip = x_forwarded_for.split(',')[0]
#         else:
#             ip = request.META.get('REMOTE_ADDR')
#         return ip

from .models import Visitor
from .utils import send_visitor_notification

class VisitorTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address = self.get_client_ip(request)
        visited_page = request.get_full_path()
        if ip_address:
            visitors = Visitor.objects.filter(ip_address=ip_address, visited_page=visited_page)
            if visitors.exists():
                visitor = visitors.first()
            else:
                visitor = Visitor(ip_address=ip_address, visited_page=visited_page, notification_sent=False)
                visitor.save()
                send_visitor_notification(ip_address, visited_page)
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

