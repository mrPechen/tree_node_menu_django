from django.urls import path
from menu.application.views import IndexPageView, add_data

urlpatterns = [
    path('tree_menu/', IndexPageView.as_view(), name='index'),
    path('add_data', add_data)
]
