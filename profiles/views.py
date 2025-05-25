from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from .froms import ProfileEditForm
from .models import Trip

from django.contrib import messages

@login_required
def profile_view(request):
    trips = Trip.objects.filter(user=request.user).order_by('-date')
    context = {
        'trips': trips,
    }
    return render(request, 'profiles/profile.html', context)

@login_required
def edit_profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profiles:profile')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = ProfileEditForm(instance=profile, user=request.user)
    return render(request, 'profiles/edit_profile.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('auth_pages:login')