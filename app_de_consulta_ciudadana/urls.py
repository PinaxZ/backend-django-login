"""
URL configuration for app_de_consulta_ciudadana project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('logtest/', views.log_in),
    path('', views.homepage, name='home'),
    path('singup/', views.singup, name='singup'),
    path('consulta/', views.consulta, name='consulta'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('create/task/', views.createTask, name='createTask'),
    path('consulta/<int:task_id>/', views.detalles_de_tareas, name='detalles_de_tareas'),
    path('consulta/<int:task_id>/complete', views.complete_task, name='complete_task'),
    path('consulta/<int:task_id>/delete', views.delete_task, name='delete_task'),
    path('consulta_completed/', views.consulta_completadas, name='consulta_completed'),
    path('api/auth/login/', views.login_api, name='login_api'),

]