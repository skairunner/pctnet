from django.contrib.auth.models import User
from django.urls import reverse

from django_webtest import WebTest
from django_dynamic_fixture import G

from profiles.models import UserProfile
from .models import Story, Chapter


DEFAULT_STORY_DATA = [
    {
        'worksummary': 'This is a **work** summary.',
        'worktitle': 'Test Saga'
    }, {
        'chaptertext': 'The content of a *chapter*.',
        'chaptertitle': 'Chapter Title'
    }, {
        'chaptertext': 'The content of chapter <em>two</em>.',
        'chaptertitle': 'Second chapter title'
    }]


class TestStory(WebTest):
    '''
    Provide an array of dicts to construct a story.
    The first dict should be the story data.
    Args will be provided directly to G()
    '''
    def make_story(self, author, data):
        out = {}
        out['story'] = G(Story, owner=author, **data[0])
        out['chapters'] = []
        for i, attrs in enumerate(data[1:]):
            out['chapters'].append(
                G(Chapter,
                  author=author,
                  parent=out['story'],
                  chapterorder=i,
                  **attrs))
        return out

    def make_default_story(self):
        author = G(User, username='author')
        notauthor = G(User, username='other-user')
        G(UserProfile, user=author, screenname='Author')
        G(UserProfile, user=notauthor, screenname='Reader')
        out = self.make_story(author, DEFAULT_STORY_DATA)
        return out['story'], out['chapters'][0]

    # Edit button should only appear for authorized
    def test_edit_button_permissions(self):
        story, chapter = self.make_default_story()
        res = self.app.get(chapter.get_absolute_url(), user='author')
        sel = res.html.select_one('.edit-chapter')
        self.assertIsNotNone(sel, 'Could not find edit chapter button')
        res = self.app.get(chapter.get_absolute_url(), user='other-user')
        sel = res.html.select_one('.edit-chapter')
        self.assertIsNone(sel, 'Unauthorized edit chapter button')

    # The actual view should also only appear for authorized
    def test_edit_view_auth_protected(self):
        story, chapter = self.make_default_story()
        # Should have edit permission
        editurl = reverse('editchapter', args=[chapter.pk])
        res = self.app.get(editurl, user='author')
        self.assertIn('200', res.status, 'Could not view authorized chapter edit page')
        # Should not have edit permission
        res = self.app.get(editurl, user='other-user', expect_errors=True)
        self.assertIn('403', res.status, 'Illegally accessed unauthorized chapter edit page')
