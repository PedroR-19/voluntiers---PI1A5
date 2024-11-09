from django.urls import path
from . import views
from .views import data_filters

app_name = 'profiles'

urlpatterns = [
    path('register/', views.register_choice_view, name='register_choice'),
    path('register/institution/', views.institution_register_view, name='institution_register'),
    path('register/voluntier/', views.voluntier_register_view, name='voluntier_register'),

    path('login/', views.login_view, name='login'),
    path('login/create/', views.login_create, name='login_create'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('match/', views.match_view, name='match'),

    # path('ajax/filter-states/', data_filters.FilterStates.as_view(), name='filter_states'),
    # path('ajax/filter-cities/', data_filters.FilterCities.as_view(), name='filter_cities'),
    # path('ajax/filter-subcategories/', data_filters.FilterSubcategories.as_view(), name='filter_subcategories'),

    path('dashboard/position/new/', views.Dashboardposition.as_view(), name='dashboard_position_new'),
    path('dashboard/position/delete/', views.DashboardpositionDelete.as_view(), name='dashboard_position_delete'),
    path('dashboard/position/<int:id>/edit/', views.Dashboardposition.as_view(), name='dashboard_position_edit'),
    path('dashboard/position/<int:id>/applications/', views.DashboardPositionApplications.as_view(), name='dashboard_position_applications'),
]
