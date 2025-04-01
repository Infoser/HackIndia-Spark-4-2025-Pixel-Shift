#urls.py
from django.urls import path
from .views import home, generate_article, save_article

urlpatterns = [
    path('', home, name='home'),
    path('generate/', generate_article, name='generate_article'),
    path('save/', save_article, name='save_article'),
]
