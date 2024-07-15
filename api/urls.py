from django.urls import path
from . import views

urlpatterns = [
    path('view/', views.view_bonds, name='view_bonds'),
    path('insert/', views.post_bond, name='post_bonds'),
    path('manage/<str:isin>/', views.manage_bond, name='manage_bond'),
    path('stat/', views.bond_analyzer, name='bond_analyzer')
]