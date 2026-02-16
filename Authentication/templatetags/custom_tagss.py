from django import template

register = template.Library()


@register.filter
def get_initials(user):
    if user.first_name and user.last_name:
        return f"{user.first_name[0]}{user.last_name[0]}".upper()
    elif user.first_name:
        return f"{user.first_name[0]}".upper()
    elif user.username:
        return f"{user.username[0]}".upper()
    return "U"  # fallback default
