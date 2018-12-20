from django_webtest import WebTest
from django.contrib.auth.models import User
from profiles.models import UserProfile
from .models import Story, Chapter


class TestStory(WebTest):
    chapter1 = None

    def setUp(self):
        user = G(User, username='test-user')
        profile = G(UserProfile, user=user, screenname='Tester')
        story = G(Story,
            owner=user,
            worksummary='This is a <b>work</b> summary.',
            worktitle='Test Saga')
        self.chapter1 = G(Chapter,
            parent=story,
            author=user,
            chaptertext='The content of a <b>chapter</b>.',
            chaptertitle='Chapter Title')
        G(Chapter,
            parent=story,
            author=user,
            chaptertext='The content of chapter <em>two</em>.',
            chaptertitle='Second chapter title',
            chaptersummary='Summary for <u>chapter</u> two.',
            chapterorder=1)
