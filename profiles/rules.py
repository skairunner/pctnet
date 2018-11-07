import rules


@rules.predicate
def can_edit_bio(user, profile):
    if profile.user.pk == user.pk:
        return True
    return False


rules.add_perm('profiles.change_profile', can_edit_bio)
