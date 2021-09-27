import httplib2
from django_cron import CronJobBase, Schedule
from .models import TelegramMessage, Activate, RegistrationProcess, datetime, drop_cache, Kandidat, SendedCerts, \
    PortfolioWorkTimeLine, Portfolio, PortfolioEducation, CurrentWorkTimeLine

from django.core.mail import EmailMultiAlternatives
from django.db.models.aggregates import Count, Min
from django.shortcuts import HttpResponse


class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1  # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'portfoli.my_cron_job'  # a unique code

    def do(self):
        print('stat')
        send_telegram()
        print('1')
        send_emails()
        print('2')
        send_certs()
        print('3')
        reindex_portfolio()
        print('4')
        reindex_education()
        print('5')


def all(request):
    print('stat')
    send_telegram()
    print('1')
    send_emails()
    print('2')
    send_certs()
    print('3')
    reindex_portfolio()
    print('4')
    reindex_education()
    print('5')
    return HttpResponse('ok')


class MyCronJob1(CronJobBase):
    RUN_EVERY_MINS = 10  # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'portfoli.my_cron_job1'  # a unique code

    def do(self):
        drop_cache()
        wtl = PortfolioWorkTimeLine.objects.filter(slave=None)
        for item in wtl:
            item.slave_id = 1
            item.save()


def send_telegram():
    h = httplib2.Http(timeout=3)

    mess = TelegramMessage.objects.filter(sended=False).order_by('date_added')
    for item in mess:
        try:
            h.request(
                uri=item.text,
                method="GET",
                body='',
                headers={
                    'Content-type': 'application/json'
                })
            item.sended = True
            item.save()
            print('sended tg')
        except:
            print('sended tg error')
            break


def test_mail(request):
    pass


def send_emails():

    for act in Activate.objects.filter(sended=False,
                                       new_method=True,
                                       admin_banned=False).order_by('date_added'):
        try:
            subject, from_email, to = act.subject.replace('\n', ' '), 'noreply@eportfolio.kz', act.user.email
            text_content = 'Auto email'
            html_content = act.html_content
            email = EmailMultiAlternatives(subject, text_content, from_email, [to], )
            email.attach_alternative(html_content, 'text/html')

            result = email.send()

            act.sended = True
            act.save()

            regs = RegistrationProcess.objects.filter(user=act.user)
            for item in regs:
                item.email_sended = True
                item.last_try = datetime.datetime.now()
                item.save()


        except:
            t_mess = TelegramMessage()
            t_mess.text = "https://api.telegram.org/bot566039687:AAFeKlzKWd-_uWJWWxvheXagrxD3Ed5mIB4/sendMessage?chat_id=92941100&text=EMAIL INVALID " + act.user.email
            t_mess.save()


def send_certs():
    kandidats = Kandidat.objects.all().exclude(svid_num__in=SendedCerts.objects.all().values('code'))
    subject = 'eportfolio.kz электронное свидетельство о прохождении аттестации'

    for item in kandidats:
        if item.svid_num is None or item.svid_num == '':
            continue
        # try:
        if True:
            if item.portfolio.sex_id == 1:
                sex = 'Уважаемый'
            elif item.portfolio.sex_id == 2:
                sex = 'Уважаемая'
            else:
                sex = 'Уважаемый(ая)'

            content = '<h2>' + sex + ' ' + item.portfolio.first_name + ' ' + item.portfolio.patronymic_name + '!</h2> <h4>поздравляем Вас с прохождением аттестации, по результатам которой Вам выдано электронное свидетельство. Скачать его можно по ссылке<br><a href="https://eportfolio.kz/ru/sv/' + item.svid_num + '">https://eportfolio.kz/ru/sv/' + item.svid_num + '</a></h4>'
            subject, from_email, to = subject, 'noreply@eportfolio.kz', item.portfolio.user.email
            text_content = 'Auto email'
            html_content = content
            email = EmailMultiAlternatives(subject, text_content, from_email, [to], )
            email.attach_alternative(html_content, 'text/html')
            result = email.send()

            r = SendedCerts()
            r.code = item.svid_num
            r.save()
            print('sended')
            t_mess = TelegramMessage()
            t_mess.text = "https://api.telegram.org/bot688081397:AAE86IbNEhETS9WtNEsib4skEx6PFLU0f9I/sendMessage?chat_id=92941100&text=svidetelstvo https://eportfolio.kz/ru/sv/" + item.svid_num
            t_mess.save()


def reindex_portfolio():
    qs = Portfolio.objects.filter(reindexed=False).order_by('id')[:600]
    i = 0
    e = 0
    for item in qs:

        wtl = item.portfolioworktimeline_set.filter(deleted=False)

        categories = item.attestation_set.filter(deleted=False).order_by('-date')

        min_date_dict = wtl.aggregate(min_date=Min('date_begin'))

        if min_date_dict['min_date'] == None:
            # item.ped_stazh = int(td.days / 365.25)
            item.reindexed = True
            item.save()
            e = e + 1
            continue
        td = datetime.date.today() - min_date_dict['min_date']

        for categ in categories:
            item.current_category = categ.category
            item.category_year = categ.date
            break

        item.ped_stazh = int(td.days / 365.25)
        item.reindexed = True
        item.save()
        i = i + 1

    qs = Portfolio.objects.filter(reindexed_wtl=False).order_by('id')[:800]
    i = 0
    e = 0
    for item in qs:
        wtl = item.currentworktimeline_set.all()
        for each in wtl:
            each.delete()

        wtl = item.portfolioworktimeline_set.filter(deleted=False,
                                                    current=True,
                                                    checked=True,
                                                    portfolio__deleted=False,
                                                    uvolen=False)
        for each in wtl:
            r = CurrentWorkTimeLine()
            r.portfolio = item
            r.wtl = each
            r.save()
            e = e + 1
        item.reindexed_wtl = True
        item.save()

    t_mess = TelegramMessage()
    t_mess.text = "https://api.telegram.org/bot688081397:AAE86IbNEhETS9WtNEsib4skEx6PFLU0f9I/sendMessage?chat_id=92941100&text=Reindex " + str(i) +' '+ str(e)
    t_mess.save()


def reindex_portf(request):
    reindex_portfolio()
    return HttpResponse('ok')


def reindex_education():
    i = 0
    e = 0
    qs = PortfolioEducation.objects.filter(speciality_handmade='',
                                           deleted=False)[:600]
    for item in qs:
        sps = ''
        for sp in item.speciality.all():
            sps = sps + ' ' + sp.name_ru

        item.speciality_handmade = sps
        try:
            item.save()
            i = i + 1
        except:
            e = e + 1
            pass

    t_mess = TelegramMessage()
    t_mess.text = "https://api.telegram.org/bot688081397:AAE86IbNEhETS9WtNEsib4skEx6PFLU0f9I/sendMessage?chat_id=92941100&text=Reindex education" + str(
        i) + '     ' + str(e)
    t_mess.save()
