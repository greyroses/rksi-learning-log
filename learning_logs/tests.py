from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Entry, Topic


class LearningLogModelTests(TestCase):
    def test_topic_and_entry_keep_owner_relation_and_readable_text(self):
        owner = get_user_model().objects.create_user('learner', password='test-password')
        topic = Topic.objects.create(owner=owner, text='Шахматы')
        entry = Entry.objects.create(topic=topic, text='Изучил дебют ферзевого гамбита.')

        self.assertEqual(str(topic), 'Шахматы')
        self.assertEqual(entry.topic, topic)
        self.assertIn('Изучил дебют', str(entry))


class LearningLogAccessTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user('learner', password='test-password')
        self.other_user = get_user_model().objects.create_user('other', password='test-password')
        self.topic = Topic.objects.create(owner=self.user, text='Моя тема')
        self.other_topic = Topic.objects.create(owner=self.other_user, text='Чужая тема')
        self.entry = Entry.objects.create(topic=self.topic, text='Моя запись')
        self.other_entry = Entry.objects.create(topic=self.other_topic, text='Чужая запись')

    def test_topics_require_login_and_hide_other_users_data(self):
        anonymous = self.client.get(reverse('learning_logs:topics'))
        self.assertRedirects(anonymous, f"{reverse('users:login')}?next={reverse('learning_logs:topics')}")

        self.client.force_login(self.user)
        response = self.client.get(reverse('learning_logs:topics'))
        self.assertContains(response, self.topic.text)
        self.assertNotContains(response, self.other_topic.text)

    def test_new_topic_assigns_current_user_despite_forged_owner(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('learning_logs:new_topic'),
            {'text': 'Новая тема', 'owner': self.other_user.pk},
        )

        new_topic = Topic.objects.get(text='Новая тема')
        self.assertRedirects(response, reverse('learning_logs:topics'))
        self.assertEqual(new_topic.owner, self.user)

    def test_foreign_topic_cannot_be_viewed_or_receive_entry(self):
        self.client.force_login(self.user)
        detail = self.client.get(reverse('learning_logs:topic', args=[self.other_topic.pk]))
        create = self.client.post(reverse('learning_logs:new_entry', args=[self.other_topic.pk]), {'text': 'Взлом'})

        self.assertEqual(detail.status_code, 404)
        self.assertEqual(create.status_code, 404)
        self.assertFalse(Entry.objects.filter(text='Взлом').exists())

    def test_entry_edit_is_limited_to_topic_owner(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('learning_logs:edit_entry', args=[self.entry.pk]),
            {'text': 'Исправленная моя запись', 'topic': self.other_topic.pk},
        )
        self.entry.refresh_from_db()
        foreign = self.client.get(reverse('learning_logs:edit_entry', args=[self.other_entry.pk]))

        self.assertRedirects(response, reverse('learning_logs:topic', args=[self.topic.pk]))
        self.assertEqual(self.entry.text, 'Исправленная моя запись')
        self.assertEqual(self.entry.topic, self.topic)
        self.assertEqual(foreign.status_code, 404)
