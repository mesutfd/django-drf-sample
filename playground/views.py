from django.shortcuts import render
from django.db.models import Q, F
from django.views.generic import ListView
from django.db.models.aggregates import Variance

from store.models import Product, OrderItem


# Create your views here.


def say_hello(request):
    query_set = Product.objects.filter(unit_price__lte=F('id')).order_by('id').all()

    print(query_set)

    return render(request, template_name='hello.html', context={
        'products': list(query_set) if query_set else None,
        'count': query_set.count()}
                  )

