from django.urls import path

from . import views

app_name = 'profiles'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/create/', views.register_create, name='register_create'),
    path('login/', views.login_view, name='login'),
    path('login/create/', views.login_create, name='login_create'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path(
        'dashboard/vacancy/new/',
        views.DashboardVacancy.as_view(),
        name='dashboard_vacancy_new'
    ),
    path(
        'dashboard/vacancy/delete/',
        views.DashboardVacancyDelete.as_view(),
        name='dashboard_vacancy_delete'
    ),
    path(
        'dashboard/vacancy/<int:id>/edit/',
        views.DashboardVacancy.as_view(),
        name='dashboard_vacancy_edit'
    ),
]
