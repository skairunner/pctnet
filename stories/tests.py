from django.contrib.auth.models import User
from django.urls import reverse
import datetime

from django_webtest import WebTest
from django_dynamic_fixture import G

from profiles.models import UserProfile
from .models import Story, Chapter, Comment


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

'''
Provide an array of dicts to construct a story.
The first dict should be the story data.
Args will be provided directly to G()
'''
def make_story(author, data):
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
    out['story'].firstchapter_id = out['chapters'][0].id
    return out


def make_default_story():
    author = G(User, username='author')
    notauthor = G(User, username='other-user')
    G(UserProfile, user=author, screenname='Author')
    G(UserProfile, user=notauthor, screenname='Reader')
    out = make_story(author, DEFAULT_STORY_DATA)
    return out['story'], out['chapters'][0]


'''
Provide data as array of tuples(author, text) or
(author, text, date)
'''
def add_comments(chapter, data):
    out = []
    for comment in data:
        if len(comment) == 2:
            author, text = comment
            out.append(G(Comment, parent=chapter, author=author, commenttext=text))
        else:
            author, text, date = comment
            out.append(
                G(Comment,
                  parent=chapter,
                  author=author,
                  commenttext=text,
                  dateposted=date))
    return out


class TestStory(WebTest):
    def test_chapter_one_linked_correctly(self):
        res = self.app.get(reverse('submitstory'), user='author')
        form = res.form
        form['chaptertitle'] = 'New Story'
        form['dateposted'] = '2018-03-02'
        form['chaptertext'] = '.'
        form.submit()
        story = Story.objects.get(worktitle='New Story')
        chapter = Chapter.objects.get(parent=story)
        self.assertEqual(story.firstchapter_id, chapter.id)

    # Edit button should only appear for authorized
    def test_edit_button_permissions(self):
        story, chapter = make_default_story()
        res = self.app.get(chapter.get_absolute_url(), user='author')
        sel = res.html.select_one('.edit-chapter')
        self.assertIsNotNone(sel, 'Could not find edit chapter button')
        res = self.app.get(chapter.get_absolute_url(), user='other-user')
        sel = res.html.select_one('.edit-chapter')
        self.assertIsNone(sel, 'Unauthorized edit chapter button')

    # The actual view should also only appear for authorized
    def test_edit_view_auth_protected(self):
        story, chapter = make_default_story()
        # Should have edit permission
        editurl = reverse('editchapter', args=[chapter.pk])
        res = self.app.get(editurl, user='author')
        self.assertIn('200', res.status, 'Could not view authorized chapter edit page')
        # Should not have edit permission
        res = self.app.get(editurl, user='other-user', expect_errors=True)
        self.assertIn('403', res.status, 'Illegally accessed unauthorized chapter edit page')

    def test_markdown_processed(self):
        story, chapter = make_default_story()
        res = self.app.get(reverse('addchapter', args=[story.pk]), user='author')
        form = res.form
        form['dateposted'] = '2018-04-09'
        form['chaptertitle'] = 'Test'
        form['chaptersummary'] = '*Summary*'
        form['chaptertext'] = '**Test**'
        res = form.submit().follow()
        html = res.html
        self.assertIn('<strong>', str(html.select_one('.chaptertext')))
        self.assertIn('<em>', str(html.select_one('.chaptersummary')))

    def test_chapter_draft(self):
        story, chapter = make_default_story()
        res = self.app.get(reverse('addchapter', args=[story.pk]), user='author')
        form = res.form
        form['dateposted'] = '2017-08-09'
        form['chaptertitle'] = 'draft'
        form['chaptertext'] = '.'
        form['isdraft'] = True
        url = form.submit().headers['Location']
        res = self.app.get(url, user='author')
        self.assertIsNotNone(res.html.select_one('#draftwarning'), "Draft warning doesn't exist")
        res = self.app.get(url, user='not-author', expect_errors=True)
        self.assertIn('404', res.status, 'Operation unexpectedly succeeded')

    def test_story_draft(self):
        story, chapter = make_default_story()
        story.isdraft = True
        story.save()

        # Check all chapters of story have draft status
        for ch in story.chapter_set.all():
            res = self.app.get(ch.get_absolute_url(), user='author')
            self.assertIsNotNone(res.html.select_one('#draftwarning'), "Draft warning doesn't exist")
        # Check that all chapters 404 for others
        for ch in story.chapter_set.all():
            res = self.app.get(ch.get_absolute_url(), user='not-author', expect_errors=True)
            self.assertIn('404', res.status, 'Operation unexpectedly succeeded')

    # StoryRedirect should fail for non-author
    def test_story_redirect_draft(self):
        story, chapter = make_default_story()
        story.isdraft = True
        story.save()
        url = f'/stories/{story.id}/slug/'
        res = self.app.get(url, user='author').follow()
        self.assertIsNotNone(res.html.select_one('#draftwarning'), "Draft warning doesn't exist")
        res = self.app.get(url, user='not-author', expect_errors=True)
        self.assertIn('404', res.status)

    def test_chapter_redirect_draft(self):
        story, chapter = make_default_story()
        chapter.isdraft = True
        chapter.save()
        url = f'/stories/chapter/{chapter.pk}'
        res = self.app.get(url, user='author').follow()
        self.assertIsNotNone(res.html.select_one('#draftwarning'), "Draft warning doesn't exist")
        res = self.app.get(url, user='not-author', expect_errors=True)
        self.assertIn('404', res.status)

    def test_chapter_edit_preview(self):
        story, chapter = make_default_story()
        res = self.app.get(reverse('editchapter', args=[chapter.id]), user='author')
        form = res.form
        form['chaptertext'] = '**Different** text'
        res = form.submit('preview')
        preview = res.html.select_one('.preview')
        self.assertIn('<strong>Different</strong>', str(preview))
        generalres = self.app.get(chapter.get_absolute_url(), user='author')
        self.assertNotIn('<strong>Different</strong>', str(generalres.html))
        # Go back to the editing field
        res = res.form.submit('edit')
        self.assertIn('**Different**', str(res.html.select_one('#id_chaptertext')))
        # Go to preview and check save
        res = res.form.submit('preview')
        res.form.submit('save')
        generalres = self.app.get(chapter.get_absolute_url(), user='author')
        self.assertIn('<strong>Different</strong>', str(generalres.html))

    def test_chapter_add_preview(self):
        story, chapter = make_default_story()
        res = self.app.get(reverse('addchapter', args=[story.id]), user='author')
        form = res.form
        form['dateposted'] = '2018-08-09'
        form['chaptertext'] = 'New stuff'
        res = form.submit('preview')
        preview = res.html.select_one('.preview')
        self.assertIn('New stuff', str(preview))
        # Submit and go to results
        res = res.form.submit('submit').follow()
        self.assertIn('New stuff', str(res.html.select_one('.chaptertext')))


class TestComments(WebTest):
    def test_comments_sorted(self):
        story, chapter = make_default_story()
        author = User.objects.get(username='author')
        other = User.objects.get(username='other-user')
        add_comments(chapter, [
            (author, 'I hope you enjoy!', datetime.date(2017, 3, 2)),
            (author, 'I really do.', datetime.date(2017, 4, 2)),
            (other, 'Pretty cool!', datetime.date(2017, 5, 2))
        ])
        res = self.app.get(chapter.get_absolute_url())
        comments = res.html.select('.dateposted')
        for i in range(1, len(comments)):
            self.assertTrue(comments[i-1]['data-date'] <= comments[i]['data-date'])

    def test_comment_markdown_processed(self):
        story, chapter = make_default_story()
        res = self.app.get(chapter.get_absolute_url(), user='not-author')
        form = res.form
        form['commenttext'] = 'I *love* this!'
        res = form.submit().follow()
        html = res.html
        self.assertIn('<em>love</em>', str(html.select_one('#comments')))
