from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import TemplateView
from django_navie import dash_app_code

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('django.contrib.auth.urls')),
    url('^dash_plot$', TemplateView.as_view(template_name='dash_plot.html'), name="dash_plot"),
    url('^django_plotly_dash/', include('django_plotly_dash.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('home/', TemplateView.as_view(template_name='home.html'), name='home'),
]