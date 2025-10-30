from .models import VisitorCounter

# Context processor to add visitor count to all templates
def visitor_count(request):
    counter = VisitorCounter.objects.first()
    return {
        'visitor_count': counter.total_visits if counter else 0
    }
