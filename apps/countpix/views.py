from django.shortcuts import render
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import connection
from django.db.models import Sum
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.clickjacking import xframe_options_exempt
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
import datetime
from django.utils import timezone
from .models import *
from apps.user.models import *

from libs.decorators import ajax_required

from django.http.response import HttpResponseBadRequest


def ajax_required(f):
    """
    AJAX request required decorator
    """
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest('Expecting Ajax call')
        return f(request, *args, **kwargs)
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__

    return wrap

# def click(request):
#     if 'hsh' in request.GET:
#         hsh = request.GET['hsh']
#         try:
#             counter = Counters.objects.get(hash_for_click=hsh)
#         except ObjectDoesNotExist:
#             return HttpResponse('Error: object does not exist')
#         counter.counter_for_click = counter.counter_for_click + 1
#         counter.save()
#         return HttpResponseRedirect(counter.link)
#     else:
#         return HttpResponse('none')


# def show(request):
#     if 'hsh' in request.GET:
#         hsh = request.GET['hsh']
#         try:
#             counter = Counters.objects.get(hash_for_show=hsh)
#         except ObjectDoesNotExist:
#             return HttpResponse('Error: object does not exist')
#         counter.counter_for_show = counter.counter_for_show + 1
#         counter.save()
#         return HttpResponse('Show counted')
#     else:
#         return HttpResponse('none')from django.shortcuts import render


@ajax_required
def click_phone(request, model):
    try:
        advert = Company.objects.get(id=request.GET.get('id'))
    except model.DoesNotExist:
        pass
    else:
        PhoneHitCounter.hit_click(request.GET.get('id'))
    return JsonResponse({})