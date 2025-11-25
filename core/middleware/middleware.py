from datetime import datetime, timedelta
from django.http import HttpResponseForbidden

def cookie_consent_middleware(get_response):
    def middleware(request):
        response = get_response(request)
        
        if request.method == 'POST' and 'cookie_consent' in request.POST:
            # Set the cookie to expire in 365 days (you can adjust the duration)
            expiration_date = datetime.now() + timedelta(days=365)
            response.set_cookie('cookie_consent', True, expires=expiration_date, path='/')

        return response

    return middleware


class DemoModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if '/delete/' in request.path.lower():
            html = """
            <html>
            <head>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        text-align: center;
                        background-color: #f4f4f4;
                        color: #333;
                        padding: 50px 0;
                    }
                    .error-container {
                        background-color: #fff;
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 0 0 15px rgba(0,0,0,0.1);
                        max-width: 500px;
                        margin: auto;
                    }
                </style>
            </head>
            <body>
                <div class="error-container">
                    <h2>Deletions are not allowed in demo mode.</h2>
                </div>
            </body>
            </html>
            """
            return HttpResponseForbidden(html)
        
        response = self.get_response(request)
        return response
