from django.shortcuts import render
from ..models import OperationHistory


def history_page(request):
    return render(request, "history.html")


def history_fragment(request):
    if not request.user.is_authenticated:
        return render(request, "partials/history_fragment.html", {"operations": []})

    operations = OperationHistory.objects.filter(
        user=request.user,
    ).order_by('-created_at')[:5]

    return render(request, "partials/history_fragment.html", {
        "operations": operations
    })
