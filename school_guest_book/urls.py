from django.contrib import admin
from django.urls import path
from guest.views import FormView 
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', FormView.as_view(), name='index'),
    path('', FormView.as_view(), name='form'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
