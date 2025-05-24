from django.shortcuts import render, redirect


def home_view(request):
    """
    Динамическая главная страница:
    - Незарегистрированные -> about_page
    - Зарегистрированные -> профиль
    """
    if request.user.is_authenticated:
        return redirect('profiles:profile')
    else:
        # Показываем about_page для незарегистрированных пользователей
        return render(request, 'about_page/about.html')
