from django.core.mail import send_mail
from django.conf import settings

def send_visitor_notification(visitor_ip, visited_page):
    subject = 'New Visitor Notification'
    message = f'A new visitor has arrived!\n\nIP Address: {visitor_ip}\nVisited Page: {visited_page}'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL])
