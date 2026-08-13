from django.urls import path
from .views import home, savollar, javob, admin_panel

urlpatterns = [
    path("", home, name="home"),
    path("savollar/", savollar, name="savollar"),
    path("javob/", javob, name="javob"),
    path("admin1", admin_panel, name="admin_panel"),
]