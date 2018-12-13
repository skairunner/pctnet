import rules


@rules.predicate
def can_edit_grouppage(user, group):
    return user in group.admins.all()


rules.add_rule('can_edit_grouppage', can_edit_grouppage)
