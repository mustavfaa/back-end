from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from . import models


class MyModelAdmin(admin.ModelAdmin):
    class Media:
        css = {
            "all": ("assets/css/select2.css",)
        }
        js = (
            "assets/js/libs/jquery/jquery-1.11.2.min.js",
            "js/my_script.js",
        )


class ActivateAdmin(MyModelAdmin):
    list_display = (
        'user',
        'date_added',
        'admin_banned',
        'sended',
        'new_method')


class TeacherScaleSettingsAdmin(MyModelAdmin):
    list_display = (
        'status',
        'destination',
        'scale',
    )


admin.site.register(models.TeacherScaleSettings, TeacherScaleSettingsAdmin)
admin.site.register(models.Place)
admin.site.register(models.WorkType)
admin.site.register(models.CurrentWorkTimeLine)


class PortfolioStatementAdmin(MyModelAdmin):
    list_display = (
        'portfolio', 'status',
        # 'positions',
        'attestation', 'school', 'checked', 'not_checked'

    )
    list_filter = ['deleted']


admin.site.register(models.PortfolioStatement, PortfolioStatementAdmin)


class AnaliticQueryAdmin(MyModelAdmin):
    list_display = (
        'sort',
        'name', 'query_text'

    )


admin.site.register(models.AnaliticQuery, AnaliticQueryAdmin)


class KandidatInline(admin.TabularInline):
    model = models.Kandidat
    extra = 0


admin.site.register(models.SchoolTypeGroup)


# class PortfolioAdmin(MyModelAdmin):
#     list_display = (
#         'name',
#         'deleted',
#         'iin',
#         'sex',
#         'user',
#         'phone',
#         'check',
#         'phone_checked',
#         'email_checked',
#         'blocked',
#
#     )
#     list_filter = [
#         'blocked',
#         'sex',
#         'email_checked',
#         'main_expert',
#         'uo_admin',
#         'uo_operator'
#     ]
#     search_fields = [
#         'name_ru',
#         'name_kk',
#         'name_en',
#         'user__username'
#     ]
#     inlines = [KandidatInline, ]

class PortfolioAdmin(MyModelAdmin):
    pass


admin.site.register(models.Portfolio, PortfolioAdmin)


class BlockHistoryAdmin(MyModelAdmin):
    list_display = (
        'portfolio',
        'who',
        'date_added',
        'status',

    )
    list_filter = [
        'status'
    ]
    search_fields = [
        'portfolio__name_ru',
        'who__first_name',
        'who__last_name',
        'who__username'
    ]


class KandidatHistoryAdmin(MyModelAdmin):
    list_display = (
        'kandidat',
        'who',
        'date_added',
        'status',
    )
    search_fields = [
        'kandidat__portfolio__name_ru',
        'who__first_name',
        'who__last_name',
        'who__username'
    ]


class KandidatVerdiktHistoryAdmin(MyModelAdmin):
    list_display = (
        'kandidat',
        'who',
        'date_added',
        'verdikt',
    )
    search_fields = [
        'kandidat__portfolio__name_ru',
        'who__first_name',
        'who__last_name',
        'who__username'
    ]


admin.site.register(models.KandidatVerdiktHistory, KandidatVerdiktHistoryAdmin)
admin.site.register(models.KandidatStatusHistory, KandidatHistoryAdmin)
admin.site.register(models.BlockHistory, BlockHistoryAdmin)
admin.site.register(models.EducationType)
admin.site.register(models.TeacherCategory)
admin.site.register(models.StudentTypeOfAchievement)
admin.site.register(models.Scale)
admin.site.register(models.Activate, ActivateAdmin)
admin.site.register(models.ComputerSkills)
admin.site.register(models.ForgetPasswordRec)
admin.site.register(models.Subject)
admin.site.register(models.DateObjects)

admin.site.register(models.Verdikt)
admin.site.register(models.TypeOfAchievement)
admin.site.register(models.CourseTheme)

admin.site.register(models.PortfolioListOfView)


class StatementProtocolAdmin(MyModelAdmin):
    list_display = (
        'school', 'author', 'attestation', 'checked', 'not_checked'

    )
    list_filter = ['deleted']


admin.site.register(models.StatementProtocol, StatementProtocolAdmin)
admin.site.register(models.StatementProtocolRecord)


class UserActivityAdmin(MyModelAdmin):
    list_display = (
        'user',
        'date',
    )


class KlassAdmin(MyModelAdmin):
    list_display = (
        'id',
        'name', 'sort', 'klass_type'
    )
    list_editable = ['sort', 'klass_type']


admin.site.register(models.Klass, KlassAdmin)


# class AttestationUserInline(admin.TabularInline):
#     model = models.TeacherAttestationUser
#     extra = 0
#
#
# class TeacherAttestationAdmin(MyModelAdmin):
#     inlines = [AttestationUserInline]


class TestingAdmin(MyModelAdmin):
    list_display = (
        'kandidat',
        'tester',
        'date_begin',
        'date_end'
    )
    search_fields = [
        'kandidat__portfolio__name_ru',
        'tester__username'
    ]
    list_filter = ['kandidat__status']


class TeacherAttestationUserAdmin(MyModelAdmin):
    list_display = (
        'user',
        'portfolio_expert',
    )


class ProtocolAdmin(MyModelAdmin):
    list_display = (
        'kandidat',
        'tester', 'file'
    )


admin.site.register(models.Protocol, ProtocolAdmin)
admin.site.register(models.Testing, TestingAdmin)
admin.site.register(models.TestingPortfolioBonus)
admin.site.register(models.TestingUpwork)
admin.site.register(models.TestingPortfolioBonusStudent)
admin.site.register(models.TestingPortfolioListOfView)
admin.site.register(models.TeacherScale)
# admin.site.register(models.Diagram)
# admin.site.register(models.DiagramType)
admin.site.register(models.TeacherAttestation)
admin.site.register(models.TeacherAttestationUser, TeacherAttestationUserAdmin)
admin.site.register(models.UserActivity, UserActivityAdmin)
admin.site.register(models.Quality)
admin.site.register(models.Language)
admin.site.register(models.EnglishLevel)

admin.site.register(models.TeacherStatus)


class PortfolioEducationAdmin(MyModelAdmin):
    list_display = (
        'portfolio',
        'date_begin',
        'date_end',
        'alma_mater', 'speciality_handmade',
        'deleted')


admin.site.register(models.PortfolioEducation, PortfolioEducationAdmin)


class KandidatOdmin(MyModelAdmin):
    list_display = (
        'portfolio',
        'status',
        'verdikt',
        'svid_num'
    )
    list_filter = ['verdikt', 'status']
    search_fields = ['portfolio__name_ru',
                     'portfolio__user__first_name',
                     'portfolio__user__last_name']


admin.site.register(models.Kandidat, KandidatOdmin)


class AlmaMaterAdmin(MyModelAdmin):
    list_display = (
        'id',
        'name',
        'short_code',
        'school_type',
        'user',
        'place',
        'sort',
        'address',
        'author',
        'has_access_to_ekitaphana',
        'jew',
        'iinbin',
        'region',
        'deleted'
    )

    list_filter = [
        'deleted',
        'nash',
        'has_access_to_ekitaphana',
        'school_type',
        'jew',
    ]
    list_editable = [
        'has_access_to_ekitaphana',
        'jew',
        'iinbin',
        'region',
        'school_type'
    ]
    search_fields = [
        'name_ru',
        'name_en',
        'name_kk',
        'address'
    ]


class RegProcAdmin(MyModelAdmin):
    list_display = (
        'date_added',
        'user',
        'email_sended',
        'email_checked',
        'last_try',
    )


class TelegAdmin(MyModelAdmin):
    list_display = (
        'date_added',
        'sended',
    )


class TeacherAttestationUserHistoryAdmin(MyModelAdmin):
    list_display = (
        'attestation',
        'user',
        'portfolio_expert',
        'operation',
        'date_added'
    )
    search_fields = [
        'attestation__name_ru',
        'user__username',
        'user__first_name',
        'user__last_name',
        'portfolio_expert__name_ru',
        'portfolio_expert__user__username',
        'operation',
    ]


admin.site.register(models.TeacherAttestationUserHistory, TeacherAttestationUserHistoryAdmin)
admin.site.register(models.TelegramMessage, TelegAdmin)
admin.site.register(models.RegistrationProcess, RegProcAdmin)
admin.site.register(models.AlmaMater, AlmaMaterAdmin)
admin.site.register(models.Speciality)
admin.site.register(models.Position)


class CourseTypeAdmin(MyModelAdmin):
    list_display = (
        'name',
        'must_vid',
        'must_subject',
        # 'must_english_level',

    )


admin.site.register(models.CourseType, CourseTypeAdmin)
admin.site.register(models.CourseVid)


# admin.site.register(models.CourseSubject)


class PortfolioWorkTimeLineAdmin(MyModelAdmin):
    list_display = (
        'portfolio',
        'date_begin',
        'date_end',
        'education',
        'school',
        'positions',
        'current',
        'deleted',
        'changer')

    list_filter = [
        'deleted',
        # 'school',
        'current',
        'slave',
        'school__nash'
    ]
    search_fields = [
        'portfolio__name_ru',
        'school__name_ru',
        'positions__name_ru'
    ]


class PhoneActivateAdmin(MyModelAdmin):
    list_display = (
        'user',
        'code')


# admin.site.register(models.CourseLevelled)
# admin.site.register(models.CourseOSODO)
# admin.site.register(models.CourseTrener)
# admin.site.register(models.CourseOSOSO)
# admin.site.register(models.CourseOSOTIPO)
# admin.site.register(models.CourseLevelledTIPO)
# admin.site.register(models.CourseCenter)
# admin.site.register(models.CourseDestination)
# admin.site.register(models.CourseLevel)
# admin.site.register(models.CourseLevelTIPO)
admin.site.register(models.PhoneActivate, PhoneActivateAdmin)
admin.site.register(models.PortfolioWorkTimeLine, PortfolioWorkTimeLineAdmin)


class UpworkAdmin(MyModelAdmin):
    list_display = (
        'portfolio',
        'date_added',
        'deleted')
    search_fields = [
        'portfolio__name_ru'
    ]


admin.site.register(models.Upwork, UpworkAdmin)


class PortfolioAttestationAdmin(MyModelAdmin):
    list_display = (
        'portfolio',
        'date',
        'deleted')
    search_fields = [
        'portfolio__name_ru'
    ]


admin.site.register(models.Attestation, PortfolioAttestationAdmin)


class StudenTtableAdmin(MyModelAdmin):
    list_display = (
        'portfolio',
        'persent',
        'deleted')


admin.site.register(models.StudenTtable, StudenTtableAdmin)


class ListObservationsAdmin(MyModelAdmin):
    list_display = (
        'portfolio',
        'deleted')


admin.site.register(models.ListObservations, ListObservationsAdmin)
admin.site.register(models.Sex)


class PortfolioPortfolioBonusAdmin(MyModelAdmin):
    list_display = (
        'portfolio',
        'date',
        'date_added',
        'image',
        'deleted')
    search_fields = [
        'portfolio__name_ru',
        'image'
    ]


admin.site.register(models.PortfolioBonus, PortfolioPortfolioBonusAdmin)


class PortfolioPortfolioBonusStudentAdmin(MyModelAdmin):
    list_display = (
        'portfolio',
        'date',
        'deleted')


admin.site.register(models.PortfolioBonusStudent, PortfolioPortfolioBonusStudentAdmin)

admin.site.register(models.Degree)


class SchoolTypeAdmin(MyModelAdmin):
    list_display = (
        'name',
        'group',
        'sort',
        'show_at_site',
        'deleted')

    list_filter = ['deleted']


admin.site.register(models.SchoolType, SchoolTypeAdmin)


class SchoolBonusAdmin(MyModelAdmin):
    list_display = (
        'date',
        'image',
        'school',
        'achievements',
    )

    list_filter = ['deleted']


class SomeModelAdmin(SummernoteModelAdmin):
    summernote_fields = 'text'


admin.site.register(models.Note, SomeModelAdmin)
admin.site.register(models.News, SomeModelAdmin)
admin.site.register(models.AdsAttestation, SomeModelAdmin)
admin.site.register(models.ChangeEmailTask)
admin.site.register(models.Region)
admin.site.register(models.Webinar)
