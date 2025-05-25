from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import transaction
from .forms import RouteStep1Form, RoutePointForm, RouteStep3Form
from .models import Route, RoutePoint
import json
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage


@login_required
def create_route_step1_view(request):
    if request.method == 'POST':
        form = RouteStep1Form(request.POST, request.FILES)
        if form.is_valid():
            # Сохраняем данные в сессии
            route_data = {
                'title': form.cleaned_data['title'],
                'description': form.cleaned_data['description'],
            }

            # Сохраняем фото во временную папку, если есть
            if form.cleaned_data.get('photo'):
                fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'temp'))
                photo = form.cleaned_data['photo']
                filename = fs.save(photo.name, photo)
                route_data['has_photo'] = True
                request.session['temp_photo_path'] = filename  # Сохраняем путь к файлу

            request.session['route_data'] = route_data
            request.session['route_points'] = []

            messages.success(request, 'Основная информация сохранена!')
            return redirect('routes:create_route_step2')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = RouteStep1Form()

    return render(request, 'routes/create_route.html', {'form': form})


@login_required
def create_route_step2_view(request):
    route_data = request.session.get('route_data', {})
    if not route_data:
        messages.error(request, 'Данные первого шага не найдены. Начните сначала.')
        return redirect('routes:create_route_step1')

    points = request.session.get('route_points', [])

    if request.method == 'POST':
        if request.content_type == 'application/json':
            # AJAX запрос для добавления/удаления точек
            data = json.loads(request.body)
            action = data.get('action')

            if action == 'add_point':
                point_data = data.get('point', {})
                points.append({
                    'id': len(points),
                    'name': point_data.get('name', ''),
                    'point_type': point_data.get('point_type', 'intermediate'),
                    'address': point_data.get('address', ''),
                    'description': point_data.get('description', ''),
                    'latitude': point_data.get('latitude'),
                    'longitude': point_data.get('longitude'),
                })
                request.session['route_points'] = points
                return JsonResponse({'success': True, 'points_count': len(points)})

            elif action == 'remove_point':
                point_id = data.get('point_id')
                points = [p for p in points if p['id'] != point_id]
                # Переиндексируем
                for i, point in enumerate(points):
                    point['id'] = i
                request.session['route_points'] = points
                return JsonResponse({'success': True, 'points_count': len(points)})

        else:
            # Обычная отправка формы - переход к шагу 3
            points = request.session.get('route_points', [])

            # Валидация точек
            if not points:
                messages.error(request, 'Добавьте хотя бы одну точку маршрута.')
                return render(request, 'routes/create_route_step2.html', {
                    'route_data': route_data,
                    'points': points
                })

            # Проверяем наличие начальной и конечной точек
            point_types = [p['point_type'] for p in points]
            if 'start' not in point_types:
                messages.error(request, 'Необходимо добавить начальную точку маршрута.')
                return render(request, 'routes/create_route_step2.html', {
                    'route_data': route_data,
                    'points': points
                })

            if 'end' not in point_types:
                messages.error(request, 'Необходимо добавить конечную точку маршрута.')
                return render(request, 'routes/create_route_step2.html', {
                    'route_data': route_data,
                    'points': points
                })

            # Проверяем уникальность start и end точек
            start_count = point_types.count('start')
            end_count = point_types.count('end')

            if start_count > 1:
                messages.error(request, 'Может быть только одна начальная точка.')
                return render(request, 'routes/create_route_step2.html', {
                    'route_data': route_data,
                    'points': points
                })

            if end_count > 1:
                messages.error(request, 'Может быть только одна конечная точка.')
                return render(request, 'routes/create_route_step2.html', {
                    'route_data': route_data,
                    'points': points
                })

            messages.success(request, 'Точки маршрута сохранены!')
            return redirect('routes:create_route_step3')

    return render(request, 'routes/create_route_step2.html', {
        'route_data': route_data,
        'points': points,
        'points_json': json.dumps(points)
    })


@login_required
def create_route_step3_view(request):
    route_data = request.session.get('route_data', {})
    points = request.session.get('route_points', [])

    if not route_data or not points:
        messages.error(request, 'Данные предыдущих шагов не найдены.')
        return redirect('routes:create_route_step1')

    if request.method == 'POST':
        form = RouteStep3Form(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Создаем маршрут
                    route = Route.objects.create(
                        user=request.user,
                        title=route_data['title'],
                        description=route_data['description'],
                        travel_date=form.cleaned_data['travel_date'],
                        route_type=form.cleaned_data['route_type']
                    )

                    # Добавляем фото, если есть
                    if route_data.get('has_photo') and 'temp_photo_path' in request.session:
                        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'temp'))
                        temp_photo_path = request.session['temp_photo_path']
                        # Перемещаем файл из временной папки
                        with fs.open(temp_photo_path) as temp_file:
                            route.photo.save(temp_photo_path, temp_file, save=True)
                        # Удаляем временный файл
                        fs.delete(temp_photo_path)

                    # Создаем точки маршрута
                    for i, point_data in enumerate(points):
                        RoutePoint.objects.create(
                            route=route,
                            name=point_data['name'],
                            point_type=point_data['point_type'],
                            address=point_data.get('address', ''),
                            description=point_data.get('description', ''),
                            latitude=point_data.get('latitude'),
                            longitude=point_data.get('longitude'),
                            order=i
                        )

                    # Очищаем сессию
                    request.session.pop('route_data', None)
                    request.session.pop('route_points', None)
                    request.session.pop('temp_photo_path', None)

                    messages.success(request, f'Маршрут "{route.title}" успешно создан!')
                    return redirect('profiles:profile')

            except Exception as e:
                messages.error(request, f'Ошибка при создании маршрута: {str(e)}')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = RouteStep3Form()

    return render(request, 'routes/create_route_step3.html', {
        'form': form,
        'route_data': route_data,
        'points': points
    })


@login_required
def route_preview_view(request):
    """Предварительный просмотр маршрута перед сохранением"""
    route_data = request.session.get('route_data', {})
    points = request.session.get('route_points', [])

    if not route_data or not points:
        messages.error(request, 'Данные маршрута не найдены.')
        return redirect('routes:create_route_step1')

    return render(request, 'routes/route_preview.html', {
        'route_data': route_data,
        'points': points
    })