from django.core.cache import cache
from django.conf import settings
from blog.models import Post


def get_posts_cache():
    """Кэширование постов на главной странице"""
    key = 'posts'
    if settings.CACHE_ENABLED:
        posts = cache.get(key)
        if posts is None:
            posts = Post.objects.order_by("-pk").distinct()[:3]
            cache.set(key, posts)
    else:
        posts = Post.objects.order_by("-pk").distinct()[:3]
    return posts
