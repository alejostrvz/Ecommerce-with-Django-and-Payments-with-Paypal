from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>', views.detail_product, name='post_detail'),
    path('review/<int:id>', views.create_review, name='comment_create'),
    path('delete-review/<int:id>', views.delete_review, name='post_delete'),
]