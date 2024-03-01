from django.urls import path
from blog.views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
from blog.apps import BlogConfig
from django.views.decorators.cache import cache_page

app_name = BlogConfig.name

urlpatterns = [
    # Посты в блоге
    path('', cache_page(60)(PostListView.as_view()), name='blog_view'),
    # Отдельный пост
    path('<int:pk>/', PostDetailView.as_view(), name='blog_detail'),
    # добавление поста через форму
    path('create/', PostCreateView.as_view(), name='blog_create'),
    # редактирование поста через форму
    path('update/<int:pk>/', PostUpdateView.as_view(), name='blog_update'),
    # удаление поста
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='blog_delete')
]
