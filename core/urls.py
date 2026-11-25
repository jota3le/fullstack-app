from django.contrib import admin
from django.urls import path
from app.views import (
    home, login_view, registro_view, logout_view,
    vender_produto, repor_estoque, deletar_produto
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('registro/', registro_view, name='registro'),
    path('logout/', logout_view, name='logout'),
    path('', home, name='home'),
    path('vender/<int:id>/', vender_produto, name='vender_produto'),
    path('repor/<int:id>/', repor_estoque, name='repor_estoque'),
    path('deletar/<int:id>/', deletar_produto, name='deletar_produto'),
]