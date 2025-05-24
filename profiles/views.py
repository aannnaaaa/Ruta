from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Trip

@login_required
def profile_view(request):
    trips = Trip.objects.filter(user=request.user).order_by('-date')
    context = {
        'trips': trips,
    }
    return render(request, 'profiles/profile.html', context)

def logout_view(request):
    logout(request)
    return redirect('auth_pages:login')