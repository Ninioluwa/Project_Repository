from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from .views import IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('project/', include('repository.urls')),
    path('', IndexView.as_view(), name="home")
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
