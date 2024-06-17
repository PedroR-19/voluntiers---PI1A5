# vacancies/urls.py
from django.urls import path

from . import views

app_name = 'vacancies'

urlpatterns = [
    path('', views.vacancy_list_view_home, name="home"),
    path('vacancies/search/', views.VacancyListViewSearch.as_view(), name="search"),
    path('vacancies/category/<int:category_id>/', views.VacancyListViewCategory.as_view(), name="category"),
    path('vacancies/<int:pk>/', views.VacancyDetail.as_view(), name="vacancy"),
    path('vacancy/<int:vacancy_id>/candidatar/', views.candidatar_vacancy, name='candidatar_vacancy'),
]
