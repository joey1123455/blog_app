from django.urls import path
from . import views 

app_name = 'blog'

urlpatterns = [
    path('', views.PostLists.as_view(), name='post-list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>', views.post_detail, name='post-detail'),
    path('<int:post_id>/share/', views.post_share, name='post-share'),
    path('<int:post_id>/comment/', views.post_comment, name='post-comment'),
]