from django.urls import path


from catalog import views


urlpatterns = [
    path('upload/', views.upload_data),
    path('<str:model_type>/<int:model_id>/', views.get_model_entry),
    path('<str:model_type>/', views.get_all_model_entries),
]

