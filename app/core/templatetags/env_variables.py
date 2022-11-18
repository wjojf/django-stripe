from django import template
import os 

register = template.Library()

@register.simple_tag()
def load_env_variable(key):
    return os.environ.get(key)