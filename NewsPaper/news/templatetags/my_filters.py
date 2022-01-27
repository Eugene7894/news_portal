from django import template

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

