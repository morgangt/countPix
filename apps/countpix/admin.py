from django.contrib import admin
from apps.countpix.models import *


# class CountersAdmin(ModelAdmin):
# 	"""  """
#     list_display = ('title', 'link', 'date', 'statistic_show', 'statistic_cliks')


# admin.site.register(Counters, CountersAdmin)


class PhoneHitCounterAdmin(ModelAdmin):
    list_display = ('view_on_site', '__str__', 'shows', 'clicks')
    list_filter = [('phonehitcounter__date', DateRangeFilterWithStatistic)]

    actions = None

    def has_add_permission(self, request):
        return False

    def shows(self, obj):
        return obj.shows
    shows.short_description = 'Показы'
    shows.admin_order_field = 'shows'

    def clicks(self, obj):
        return obj.clicks
    clicks.short_description = 'Клики'
    clicks.admin_order_field = 'clicks'


class CompanyPhoneHitsAdmin(PhoneHitCounterAdmin):
    search_fields = ('title', )

    def get_queryset(self, request):
        """ Показ компаний для города админки """
        queryset = super(PhoneHitCounterAdmin, self).get_queryset(request)
        if request.city_for_admin.title_i == 'Россия':
            return queryset.all()
        return queryset.filter(models.Q(company__companycities__city=request.city_for_admin) |
                               models.Q(company__parent_company__companycities__city=request.city_for_admin)).distinct()


admin.site.register(CompanyPhoneHits, CompanyPhoneHitsAdmin)