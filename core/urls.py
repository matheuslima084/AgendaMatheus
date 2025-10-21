from django.urls import path
from . import views

urlpatterns = [
    path('add_contato/',views.add_contato, name='add_contato'),
    path('listar_contato/', views.listar_contato, name='listar_contato'),
    path('editarContato/<int:id>/', views.editarContato, name='editarContato'),
    path('excluirContato/<int:id>/', views.excluirContato, name='excluirContato'),
]
