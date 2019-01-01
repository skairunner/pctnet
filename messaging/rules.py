import rules

def is_member_of_groupchat(user, group):
    return group.members.filter(pk=user.pk).exists()


def is_groupchat_owner(user, group):
    return user.pk == group.owner.pk


# 'can view' also means can send messages
rules.add_perm('messaging.view_privatemessagegroup', is_member_of_groupchat)
# 'can edit' means adding new members or changing the groupchat name
rules.add_rule('can_edit_groupchat', is_groupchat_owner)
