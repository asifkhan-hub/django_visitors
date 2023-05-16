from django.shortcuts import redirect
from django.contrib.auth import logout
from django.conf import settings
from datetime import datetime, timedelta

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            current_time = datetime.now()
            last_activity_str = request.session.get('last_activity')

            if last_activity_str:
                last_activity = datetime.fromisoformat(last_activity_str)
                if (current_time - last_activity) > timedelta(seconds=settings.SESSION_COOKIE_AGE):
                    logout(request)
                    return redirect(settings.SESSION_EXPIRE_REDIRECT)

            request.session['last_activity'] = current_time.isoformat()

        response = self.get_response(request)
        return response
