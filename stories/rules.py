import rules


@rules.predicate
def can_edit_story(user, story):
    return  story.author.pk == user.pk


@rules.predicate
def can_delete_story(user, story):
    return story.author.pk == user.pk


@rules.predicate
def can_edit_comment(user, comment):
    return user.pk == comment.author.pk


@rules.predicate
def can_delete_comment(user, comment):
    return user.pk == comment.author.pk


rules.add_rule('can_delete_comment', can_delete_comment)
rules.add_perm('stories.change_story', can_edit_story)
rules.add_perm('comment.change_comment', can_edit_comment)

