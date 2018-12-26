import rules


@rules.predicate
def can_edit_story(user, story):
    return story.owner.pk == user.pk


@rules.predicate
def can_edit_chapter(user, chapter):
    return can_edit_story(user, chapter.parent)


@rules.predicate
def is_chapter_author(user, chapter):
    return user == chapter.author


@rules.predicate
def is_story_owner(user, story):
    return user == story.owner


@rules.predicate
def is_chapter_story_owner(user, chapter):
    return is_story_owner(user, chapter.parent)


@rules.predicate
def can_delete_story(user, story):
    return story.owner.pk == user.pk


@rules.predicate
def can_edit_comment(user, comment):
    return user.pk == comment.author.pk


@rules.predicate
def can_delete_comment(user, comment):
    return user.pk == comment.author.pk


rules.add_rule('can_edit_comment', can_edit_comment)
rules.add_rule('can_delete_comment', can_delete_comment)
rules.add_rule('can_view_story_draft', is_story_owner)
rules.add_rule('can_view_chapter_draft', is_chapter_author | is_chapter_story_owner)
rules.add_perm('stories.change_chapter', can_edit_chapter)
rules.add_perm('stories.change_story', can_edit_story)
rules.add_perm('comment.change_comment', can_edit_comment)
