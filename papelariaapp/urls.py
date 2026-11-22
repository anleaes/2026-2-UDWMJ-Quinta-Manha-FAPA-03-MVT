
"""
URL configuration for papelariaapp project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),
    path('grupos-materiais/', include('grupos_materiais.urls')),
    path('materiais/', include('materiais_papelaria.urls', namespace='materiais_papelaria')),
    path('marcas/', include('marcas.urls', namespace='marcas')),
    path('funcionarios/', include('funcionarios.urls')),
    path('fornecedores/', include('fornecedores.urls')),
    path('compradores/', include('compradores.urls')),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
