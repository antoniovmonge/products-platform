from .selection import Selection


def selection(request):
    return {"selection": Selection(request)}
