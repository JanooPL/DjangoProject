from django import template

register = template.Library()

@register.filter
def range_filter(value):
    return range(value)

@register.filter
def index(board, i):
    return board[int(i)]