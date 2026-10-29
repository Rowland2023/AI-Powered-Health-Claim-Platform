from django.db import connection
from django.http import JsonResponse


def health_check(request):
    try:
        with connection.cursor() as c:
            c.execute("SELECT 1")
        return JsonResponse({"status": "ok", "db": "up"})
    except Exception as e:
        return JsonResponse({"status": "error", "db": str(e)}, status=500)
