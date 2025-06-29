from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import OperationHistory


@login_required(login_url='login')
def history_page(request):
    return render(request, "history.html")


@login_required(login_url='login')
def history_fragment(request):
    operations = OperationHistory.objects.filter(
        user=request.user,
    ).order_by('-created_at')[:5]

    return render(request, "partials/history_fragment.html", {
        "operations": operations
    })