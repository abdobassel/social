from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def app(request, **kwargs):
    context = {}
    return render(request, "dashboard/app.html", context=context)
