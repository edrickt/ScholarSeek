from django.contrib import admin
from django.urls import path
from search import views  # Import the views module from your search app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # Use views.index here
    path('search/', views.search_by_criteria, name='search_by_criteria'),  # Corrected path for search_by_author view
]
