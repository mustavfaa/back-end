from portfoli.models import PortfolioWorkTimeLine

LIBRARIAN = 107
LIBRARIAN_ZAM = 152


def user_schools(user):
    schools = PortfolioWorkTimeLine.objects.filter(deleted=False,
                                                   current=True,
                                                   school__has_access_to_ekitaphana=True,
                                                   checked=True,
                                                   portfolio__user=user).values('school', 'positions')
    return schools
