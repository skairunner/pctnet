from django_webtest import WebTest
from django_dynamic_fixture import G
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from .models import UserProfile


class TestProfileView(WebTest):
    lisa = None
    lisaprofile = None

    def setUp(self):
        self.lisa = lisa = G(User, username='lisa')
        screenname = 'Lisa Wilbourn'
        self.lisaprofile = G(UserProfile, user=lisa, screenname=screenname, slug=slugify(screenname))
        brian = G(User, username='brian')
        G(UserProfile, user=brian, screenname='brian', slug='brian')

    def test_redirect_to_authuser_profile_page(self):
        res = self.app.get('/user/', user='lisa')
        u = self.lisaprofile
        self.assertEqual(
            res.headers['Location'],
            reverse('viewuser', args=[u.pk, 'lisa-wilbourn']))

    # only show edit button if you're the user
    def test_profile_page_edit_button(self):
        profileurl = self.lisaprofile.get_full_url()
        res = self.app.get(profileurl, user='lisa')
        try:
            res.click('Edit')
        except IndexError:
            self.fail(f'Unexpected IndexError raised {res}')
        res = self.app.get(profileurl, user='brian')
        self.assertRaises(IndexError, res.click, 'Edit')

    # Checks bio is displayed & that markup isn't escaped
    def test_profile_page_content(self):
        imp = G(User, username='aisha')
        G(UserProfile, user=imp, bio='<i>Nothing to see</i>')
        res = self.app.get(
            reverse('viewuser', args=[imp.pk, 'imp']),
            user='aisha')
        bio = res.html.select('.bio-content')[0]
        self.assertEqual(bio.find('i').get_text(), 'Nothing to see')

    def test_profile_page_bio_edit(self):
        editurl = reverse('updatebio', args=[self.lisa.pk])
        res = self.app.get(editurl, user='lisa')
        form = res.form
        form['bio'] = 'Valid profile data.'
        form.submit()
        res = self.app.get(self.lisaprofile.get_full_url())
        bio = res.html.select('.bio-content')[0]
        self.assertEqual(bio.get_text(), 'Valid profile data.')

    def test_profile_page_slug_edit(self):
        editurl = reverse('updatebio', args=[self.lisa.pk])
        res = self.app.get(editurl, user='lisa')
        form = res.form
        form['slug'] = 'arbitrary-slug'
        form.submit()
        res = self.app.get(f'/user/{self.lisa.pk}/')
        url = res.headers['Location']
        self.assertEqual(url, reverse('viewuser', args=[self.lisa.pk, 'arbitrary-slug']))

    def test_profile_page_redirect(self):
        res = self.app.get(f'/user/{self.lisa.pk}/')
        # check for some kind of redirect
        self.assertEqual(res.status[0], '3')
        newloc = res.headers['Location']
        self.assertEqual(newloc, self.lisaprofile.get_full_url())
