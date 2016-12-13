from django.db import models
from datetime import datetime


# class Counters(models.Model):
#     title = models.CharField(max_length=140, verbose_name='Name object')
#     link = models.CharField(max_length=255, verbose_name='Link')
#     date = models.DateField(auto_now=True, verbose_name='Date event', default=datetime.now)
#     hash_for_click = models.CharField(max_length=255, verbose_name='Hash for clicks')
#     hash_for_show = models.CharField(max_length=255, verbose_name='Hash for shows')
#     counter_for_click = models.IntegerField(default=0, verbose_name='Counter clicks')
#     counter_for_show = models.IntegerField(default=0, verbose_name='Counter shows')
    
#     def statistic_show(self):
#         return 

#     def statistic_cliks(self):
#         return 

#     class Meta:
#         verbose_name = "Counter"
#         verbose_name_plural = "Counters"

#     def __str__(self):
#         return 'Counter #%s' % self.id


class PhoneHitCounterQS(models.QuerySet):

    def find_for(self, obj):
        """ Поиск записей счетчика по данному объекту """
        if obj.pk:
            ct = ContentType.objects.get_for_model(obj)
            return self.filter(content_type=ct, object_id=obj.pk)
        else:
            raise ReferenceError('Object have no primary key for counter')

    def count_shows(self):
        return self.aggregate(Sum('shows'))['shows__sum'] or 0

    def count_clicks(self):
        return self.aggregate(Sum('clicks'))['clicks__sum'] or 0

class PhoneHitCounter(models.Model):

    company = models.ForeignKey(Company)

    date = models.DateField(default=datetime.now, verbose_name='Дата')

    shows = models.PositiveIntegerField(default=0, verbose_name='Количество показов')
    clicks = models.PositiveIntegerField(default=0, verbose_name='Количество кликов')

    objects = PhoneHitCounterQS.as_manager()

    def __str__(self):
        return '{0}: shows {1}, clicks {2}'.format(self.date.strftime('%d-%m-%Y'), self.shows, self.clicks)

    class Meta:
        verbose_name = _("Просмотры телефона")
        verbose_name_plural = _("Просмотры телефонов")
        permissions = (
            ("view_phone_hits", "Can see phone hits"),
        )
        unique_together = [('company', 'date')]

    def __str__(self):
        return '{0}: shows {1}, clicks {2}'.format(self.date.strftime('%d-%m-%Y'), self.shows, self.clicks)

    @classmethod
    def hit_show(cls, obj, amount=1):
        """ Увеличение значения счетчика """
        company = Company.objects.get(id=obj)
        try:
            with transaction.atomic():
                record, created = cls.objects.get_or_create(company=company, date=datetime.now())
        except IntegrityError:
            with transaction.atomic():
                record = cls.objects.get(company=company, date=datetime.now())
                record.shows += amount
                record.clean()
                record.save()

    @classmethod
    def hit_click(cls, obj, amount=1):
        """ Увеличение значения счетчика """
        company = Company.objects.get(id=obj)
        try:
            with transaction.atomic():
                record, created = cls.objects.get_or_create(company=company, date=datetime.now())
                record.clicks += amount
                record.clean()
                record.save()
        except IntegrityError:
            with transaction.atomic():
                record = cls.objects.get(company=company, date=datetime.now())
                record.clicks += amount
                record.clean()
                record.save()

    def get_absolute_url(self):
        Company.get_absolute_url(self.company)


class CompanyPhoneHits(Company):
    class Meta:
        proxy = True
        verbose_name = 'компания'
        verbose_name_plural = 'компании'
        default_permissions = ('change', )
        permissions = (('can_view_advert_phone_hits', 'Can view advert phone hits'), )