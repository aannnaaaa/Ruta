from django.db import models
from django.contrib.auth.models import User


class Route(models.Model):
    ROUTE_TYPE_CHOICES = [
        ('public', 'Публичный'),
        ('private', 'Приватный'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='routes')
    title = models.CharField(max_length=100, verbose_name="Название маршрута")
    description = models.TextField(verbose_name="Описание")
    photo = models.ImageField(upload_to='route_photos/', null=True, blank=True, verbose_name="Фото маршрута")
    travel_date = models.DateField(verbose_name="Дата поездки")
    route_type = models.CharField(
        max_length=20,
        choices=ROUTE_TYPE_CHOICES,
        default='public',
        verbose_name="Тип маршрута"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Маршрут"
        verbose_name_plural = "Маршруты"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def start_point(self):
        return self.points.filter(point_type='start').first()

    @property
    def end_point(self):
        return self.points.filter(point_type='end').first()

    @property
    def intermediate_points(self):
        return self.points.filter(point_type='intermediate').order_by('order')

    @property
    def total_points(self):
        return self.points.count()


class RoutePoint(models.Model):
    POINT_TYPE_CHOICES = [
        ('start', 'Начальная точка'),
        ('intermediate', 'Промежуточная точка'),
        ('end', 'Конечная точка'),
    ]

    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='points')
    name = models.CharField(max_length=100, verbose_name="Название точки")
    point_type = models.CharField(
        max_length=20,
        choices=POINT_TYPE_CHOICES,
        verbose_name="Тип точки"
    )
    address = models.CharField(max_length=255, blank=True, verbose_name="Адрес")
    description = models.TextField(blank=True, verbose_name="Описание")
    photo = models.ImageField(upload_to='point_photos/', null=True, blank=True, verbose_name="Фото точки")
    latitude = models.FloatField(null=True, blank=True, verbose_name="Широта")
    longitude = models.FloatField(null=True, blank=True, verbose_name="Долгота")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Точка маршрута"
        verbose_name_plural = "Точки маршрута"
        ordering = ['order']
        unique_together = [['route', 'point_type']]  # Для start и end должна быть только одна

    def __str__(self):
        return f"{self.name} ({self.get_point_type_display()}) - {self.route.title}"