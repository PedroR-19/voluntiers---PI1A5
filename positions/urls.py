# positions/urls.py
from django.urls import path

from . import views

app_name = 'positions'

urlpatterns = [
    path('', views.position_list_view_home, name="home"),

    path('positions/search/', views.positionListViewSearch.as_view(), name="search"),

    path('positions/category/<int:category_id>/', views.positionListViewCategory.as_view(), name="category"),

    path('positions/<int:pk>/', views.positionDetail.as_view(), name="position"),
    
    path('position/<int:position_id>/candidatar/', views.candidatar_position, name='candidatar_position'),
]
