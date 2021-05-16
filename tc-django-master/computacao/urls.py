from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'computacao'

urlpatterns = [
                  path('', views.index, name='index'),
                  path('index/', views.index, name='index'),
                  path('automatos/', views.automatos, name='automatos'),
                  path('novo_automato/', views.novo_automato, name='novo_automato'),
                  path('edita_automato/<int:automato_id>/', views.edita_automato, name='edita_automato'),
                  path('apaga_automato/<int:automato_id>/', views.apaga_automato, name='apaga_automato'),
                  path('<int:automato_id>/automato/', views.automato, name='automato'),
                  
                  path('maquinas/',views.maquinas,name='maquinas'),
                  path('novamaquina/', views.novamaquina, name='novamaquina'),
                  path('editamaquina/<int:maquina_id>/', views.editamaquina, name='editamaquina'),
                  path('apagamaquina/<int:maquina_id>/', views.apagamaquina, name='apagamaquina'),
                  path('<int:maquina_id>/maquina/', views.maquina, name='maquina'), 

                  path('expressoes/',views.expressoes,name='expressoes'),
                  path('novaexpressao/', views.novaexpressao, name='novaexpressao'),
                  path('editaexpressao/<int:expressao_id>/', views.editaexpressao, name='editaexpressao'),
                  path('apagaexpressao/<int:expressao_id>/', views.apagaexpressao, name='apagaexpressao'),
                  path('<int:expressao_id>/expressao/', views.expressao, name='expressao')                                 
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)