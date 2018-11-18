import rules


@rules.predicate
def can_edit_story(user, story):
    if story.author.pk == user.pk:
        return True
    return False


@rules.predicate
def can_delete_story(user, story):
    if story.author.pk == user.pk:
        return True
    return False


rules.add_perm('stories.change_story', can_edit_story)
rules.add_perm('stories.delete_story', can_delete_story)
