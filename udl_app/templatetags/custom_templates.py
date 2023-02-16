from django import template

register = template.Library()

"""
args needs to be passed as a string instead of a dictionary.
For example {'class': 'name1', 'style': 'max-width:120px'}
should be passed as "class=name1,style=max-width:120px"
"""


@register.filter(name='add_attributes')
def add_attributes(value, args):
    kv_pairs = [kv_pair.strip() for kv_pair in args.split(',')]
    attrs_dict = {str(i.split('=')[0].strip()): str(i.split('=')[1].strip()) for i in kv_pairs}
    return value.as_widget(attrs=attrs_dict)
