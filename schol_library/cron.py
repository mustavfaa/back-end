from django_cron import CronJobBase, Schedule
from django.core.cache import cache
from schol_library import serializers
from .models import Edition, StudyDirections, Year, AuthorEdition, PublisherEdition, UMK, NumberBooks
from .serializers import EditionsSerializerS
from portfoli import models as p_models


class CreateCashCronJob(CronJobBase):
    RUN_EVERY_MINS = 350  # Каждый 2 минуты
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'schol_library.create_cash_cron_job'

    def do(self):
        for lang in ['ru', 'kk', 'en']:
            cache_name = 'eds' + lang
            data = cache.get(cache_name)
            if data is None:
                data = {}
                data['books'] = EditionsSerializerS(Edition.objects.all().order_by('name'), many=True).data
                data['years'] = serializers.YearSerializers(Year.objects.all().order_by('year'), many=True).data
                data['authors'] = serializers.AuthorEditionSerializers(AuthorEdition.objects.all().order_by('name'),
                                                                       many=True).data
                data['publishers'] = serializers.PublisherEditionSerializers(
                    PublisherEdition.objects.all().order_by('name_' + lang), many=True).data
                data['languages'] = serializers.LangSerializers(
                    p_models.Language.objects.all().order_by('name_' + lang), many=True).data
                data['klasss'] = serializers.KlassSerializers(p_models.Klass.objects.all(), many=True).data
                data['subjects'] = serializers.SubjectSerializers(
                    p_models.Subject.objects.all().order_by('name_' + lang), many=True).data
                data['metodology_complex'] = serializers.MetodologyComplexSerializers(
                    UMK.objects.all().order_by('name_' + lang), many=True).data
                data['study_direction'] = serializers.StudyDirectionsSerializer(
                    StudyDirections.objects.all().order_by('name_' + lang), many=True).data
                cache.set(cache_name, data, 2592000)


class DelDubelCronJob(CronJobBase):
    RUN_EVERY_MINS = 1  # Каждый 2 минуты
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'schol_library.del_dubel_cron_job'

    def do(self):

        return
        # Я ХЗ что это
        for id in Edition.objects.all().values_list('id', flat=True):
            for school_id in p_models.AlmaMater.objects.all().values_list('id', flat=True):
                num = NumberBooks.objects.filter(school_id=school_id).filter(edition_id=id)
                ids_num = num.values_list('id', flat=True)
                if len(num) > 1:
                    num1 = num[0]
                    id_num = [x for x in ids_num if x != num1.id]
                    nums = num[1:]
                    for item in nums:
                        num1.on_hands += item.on_hands
                        num1.in_warehouse += item.in_warehouse
                    num1.save()
                    NumberBooks.objects.filter(id__in=id_num).delete()
        print('Ready!')

# class NumberBooksSave(CronJobBase):
#     RUN_EVERY_MINS = 1  # Каждый 2 минуты
#     schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
#     code = 'schol_library.number_books_save_cron_job'
#
#     def do(self):
#         for i in NumberBooks.objects.filter(in_register=False)[:500]:
#             i.is_record_to_register = True
#             print('reg')
#             i.save()
