from django import template

register = template.Library()


@register.simple_tag
def mediapath(path):
    """Формирует относительное имя (путь) медиафайла"""
    path = str(path).split('/media/')
    media_path = '/' + 'media' + '/' + path[-1]
    return media_path


@register.filter(name='mediapath')
def mediapath(path):
    """Фильтрует полученное полное имя (путь) медиафайла"""
    path = str(path).split('/media/')
    media_path = '/' + 'media' + '/' + path[-1]
    return media_path
