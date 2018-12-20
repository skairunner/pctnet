from django.contrib.auth.models import User
from django.urls import reverse

from django_webtest import WebTest
from django_dynamic_fixture import G

from profiles.models import UserProfile
from .models import Story, Chapter


class TestStory(WebTest):
    chapter1 = None

    def setUp(self):
        author = G(User, username='author')
        notauthor = G(User, username='other-user')
        G(UserProfile, user=author, screenname='Author')
        G(UserProfile, user=notauthor, screenname='Reader')
        story = G(Story,
            owner=author,
            worksummary='This is a <b>work</b> summary.',
            worktitle='Test Saga')
        self.chapter1 = G(Chapter,
            parent=story,
            author=author,
            chaptertext='The content of a <b>chapter</b>.',
            chaptertitle='Chapter Title')
        G(Chapter,
            parent=story,
            author=author,
            chaptertext='The content of chapter <em>two</em>.',
            chaptertitle='Second chapter title',
            chaptersummary='Summary for <u>chapter</u> two.',
            chapterorder=1)

    # Edit button should only appear for authorized
    def test_edit_button_permissions(self):
        res = self.app.get(self.chapter1.get_absolute_url(), user='author')
        sel = res.html.select_one('.edit-chapter')
        self.assertIsNotNone(sel, 'Could not find edit chapter button')
        res = self.app.get(self.chapter1.get_absolute_url(), user='other-user')
        sel = res.html.select_one('.edit-chapter')
        self.assertIsNone(sel, 'Unauthorized edit chapter button')

    # The actual view should also only appear for authorized
    def test_edit_view_auth_protected(self):
        # Should have edit permission
        editurl = reverse('editchapter', args=[self.chapter1.pk])
        res = self.app.get(editurl, user='author')
        self.assertIn('200', res.status, 'Could not view authorized chapter edit page')
        # Should not have edit permission
        res = self.app.get(editurl, user='other-user', expect_errors=True)
        self.assertIn('403', res.status, 'Illegally accessed unauthorized chapter edit page')
