from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Sözlükten bir değer almak için kullanılan filtre
    Örnek: {{ is_emirleri|get_item:arac.id }}
    """
    return dictionary.get(key) 