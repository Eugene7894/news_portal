from django import template
from ..models import Post

register = template.Library()


@register.filter(name='censor')
def censor(value):
    text_list = str(value).split()
    bad_words = ['осёл', 'лошар', 'лопух',]
    for i, word in enumerate(text_list):
        if word.strip(',') in bad_words:
            text_list[i] = '****'
    value = ' '.join(text_list)
    return value


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter(name='items_counter')
def items_counter(value):
    length = len(Post.objects.all())
    return length


# Фильтр, который заменяет все буквы кроме первой и последней на «*» у слов из списка «нежелательных». Предполагается,
# что в качестве аргумента гарантированно передается текст, и слова разделены пробелами. Можно считать, что запрещенные
# слова находятся в списке forbidden_words.
# @register.filter
# def hide_forbidden(value):
#     words = value.split()
#     result = []
#     for word in words:
#         if word in forbidden_words:
#             result.append(word[0] + "*"*(len(word)-2) + word[-1])
#         else:
#             result.append(word)
#     return " ".join(result)
