from django import template
from datetime import datetime, timedelta  # Make sure to import timedelta

register = template.Library()

# Filter to get initials of a user
@register.filter
def get_initials(user):
    if user.username and user.last_name:
        return f"{user.first_name[0]}{user.last_name[0]}".upper()
    elif user.first_name:
        return f"{user.first_name[0]}".upper()
    elif user.username:
        return f"{user.username[0]}".upper()
    return "U"  # fallback default


# Filter to calculate the time difference between check-out and check-in
@register.filter
def time_diff(check_out, check_in):
    """
    Custom filter to calculate the time difference between check-out and check-in.
    Returns the difference in hours and minutes (e.g., 3h 15m).
    """
    if not check_out or not check_in:
        return '--'

    # Convert check_in and check_out to datetime objects
    check_in_time = datetime.combine(datetime.today(), check_in)
    check_out_time = datetime.combine(datetime.today(), check_out)

    # If check_out is earlier than check_in, assume it's from the next day
    if check_out_time < check_in_time:
        check_out_time += timedelta(days=1)

    # Calculate the time difference
    time_diff = check_out_time - check_in_time
    hours, remainder = divmod(time_diff.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    return f"{hours}h {minutes}m"
