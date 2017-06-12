from django import template

# Creating a custom template tags to be used in django html templates


def divide(value, arg):
    try:
        return int(value) / int(arg)
    except (ValueError, ZeroDivisionError):
        return None


def remainder(value, arg):
    try:
        return int(value) % int(arg)
    except (ValueError, ZeroDivisionError):
        return None

# register the custom template tags to the template Library
register = template.Library()
register.filter(name='divide', filter_func=divide)
register.filter(name='remainder', filter_func=remainder)