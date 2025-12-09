from web_dashboard import app

# Vercel serverless function handler
def handler(request):
    return app(request.environ, lambda *args: None)
