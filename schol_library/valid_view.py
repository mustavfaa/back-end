

def head_librarian(user):
    return user.groups.filter(id__in=[1, 6]).exists()


def head_science(user):
    return user.groups.filter(id__in=[2, 6]).exists()


def librarian(user):
    return user.groups.filter(id__in=[3, 6]).exists()


def llibrarian_or_head(user):
    return user.groups.filter(id__in=[1, 3, 6]).exists()


def llibrarian_or_admin(user):
    if user.is_superuser or user.groups.filter(id__in=[1, 3, 6]).exists():
        return True
    return False
