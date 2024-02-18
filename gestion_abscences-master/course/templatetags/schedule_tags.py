from django import template

register = template.Library()


@register.filter
def get_course(schedule_dict, day_hour):
    day, hour = day_hour
    return schedule_dict.get(day, {}).get(hour)