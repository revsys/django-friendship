import os
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.core.urlresolvers import reverse
from django.test import TestCase

from friendship.exceptions import AlreadyExistsError, AlreadyFriendsError
from friendship.models import Friend, Follow, FriendshipRequest


TEST_TEMPLATES = os.path.join(os.path.dirname(__file__), 'templates')


class login(object):
    def __init__(self, testcase, user, password):
        self.testcase = testcase
        success = testcase.client.login(username=user, password=password)
        self.testcase.assertTrue(
            success,
            "login with username=%r, password=%r failed" % (user, password)
        )

    def __enter__(self):
        pass

    def __exit__(self, *args):
        self.testcase.client.logout()


class BaseTestCase(TestCase):

    def setUp(self):
        """
        Setup some initial users

        """
        self.user_pw = 'test'
        self.user_bob = self.create_user('bob', 'bob@bob.com', self.user_pw)
        self.user_steve = self.create_user('steve', 'steve@steve.com', self.user_pw)
        self.user_susan = self.create_user('susan', 'susan@susan.com', self.user_pw)
        self.user_amy = self.create_user('amy', 'amy@amy.amy.com', self.user_pw)
        cache.clear()

    def tearDown(self):
        cache.clear()
        self.client.logout()

    def login(self, user, password):
        return login(self, user, password)

    def create_user(self, username, password, email_address):
        user = User.objects.create_user(username, password, email_address)
        return user

    def assertResponse200(self, response):
        self.assertEqual(response.status_code, 200)

    def assertResponse302(self, response):
        self.assertEqual(response.status_code, 302)

    def assertResponse403(self, response):
        self.assertEqual(response.status_code, 403)

    def assertResponse404(self, response):
        self.assertEqual(response.status_code, 404)


class FriendshipModelTests(BaseTestCase):

    def test_friendship_request(self):
        ### Bob wants to be friends with Steve
        req1 = Friend.objects.add_friend(self.user_bob, self.user_steve)

        # Ensure neither have friends already
        self.assertEqual(Friend.objects.friends(self.user_bob), [])
        self.assertEqual(Friend.objects.friends(self.user_steve), [])

        # Ensure FriendshipRequest is created
        self.assertEqual(FriendshipRequest.objects.filter(from_user=self.user_bob).count(), 1)
        self.assertEqual(FriendshipRequest.objects.filter(to_user=self.user_steve).count(), 1)
        self.assertEqual(Friend.objects.unread_request_count(self.user_steve), 1)

        # Ensure the proper sides have requests or not
        self.assertEqual(len(Friend.objects.requests(self.user_bob)), 0)
        self.assertEqual(len(Friend.objects.requests(self.user_steve)), 1)
        self.assertEqual(len(Friend.objects.sent_requests(self.user_bob)), 1)
        self.assertEqual(len(Friend.objects.sent_requests(self.user_steve)), 0)

        self.assertEqual(len(Friend.objects.unread_requests(self.user_steve)), 1)
        self.assertEqual(Friend.objects.unread_request_count(self.user_steve), 1)

        self.assertEqual(len(Friend.objects.rejected_requests(self.user_steve)), 0)

        self.assertEqual(len(Friend.objects.unrejected_requests(self.user_steve)), 1)
        self.assertEqual(Friend.objects.unrejected_request_count(self.user_steve), 1)

        # Ensure they aren't friends at this point
        self.assertFalse(Friend.objects.are_friends(self.user_bob, self.user_steve))

        # Accept the request
        req1.accept()

        # Ensure neither have pending requests
        self.assertEqual(FriendshipRequest.objects.filter(from_user=self.user_bob).count(), 0)
        self.assertEqual(FriendshipRequest.objects.filter(to_user=self.user_steve).count(), 0)

        # Ensure both are in each other's friend lists
        self.assertEqual(Friend.objects.friends(self.user_bob), [self.user_steve])
        self.assertEqual(Friend.objects.friends(self.user_steve), [self.user_bob])
        self.assertTrue(Friend.objects.are_friends(self.user_bob, self.user_steve))

        # Make sure we can remove friendship
        self.assertTrue(Friend.objects.remove_friend(self.user_bob, self.user_steve))
        self.assertFalse(Friend.objects.are_friends(self.user_bob, self.user_steve))
        self.assertFalse(Friend.objects.remove_friend(self.user_bob, self.user_steve))

        # Susan wants to be friends with Amy, but cancels it
        req2 = Friend.objects.add_friend(self.user_susan, self.user_amy)
        self.assertEqual(Friend.objects.friends(self.user_susan), [])
        self.assertEqual(Friend.objects.friends(self.user_amy), [])
        req2.cancel()
        self.assertEqual(Friend.objects.requests(self.user_susan), [])
        self.assertEqual(Friend.objects.requests(self.user_amy), [])

        # Susan wants to be friends with Amy, but Amy rejects it
        req3 = Friend.objects.add_friend(self.user_susan, self.user_amy)
        self.assertEqual(Friend.objects.friends(self.user_susan), [])
        self.assertEqual(Friend.objects.friends(self.user_amy), [])
        req3.reject()

        # Duplicated requests raise a more specific subclass of IntegrityError.
        with self.assertRaises(AlreadyExistsError):
            Friend.objects.add_friend(self.user_susan, self.user_amy)

        self.assertFalse(Friend.objects.are_friends(self.user_susan, self.user_amy))
        self.assertEqual(len(Friend.objects.rejected_requests(self.user_amy)), 1)
        self.assertEqual(len(Friend.objects.rejected_requests(self.user_amy)), 1)

        # let's try that again..
        req3.delete()

        # Susan wants to be friends with Amy, and Amy reads it
        req4 = Friend.objects.add_friend(self.user_susan, self.user_amy)
        req4.mark_viewed()

        self.assertFalse(Friend.objects.are_friends(self.user_susan, self.user_amy))
        self.assertEqual(len(Friend.objects.read_requests(self.user_amy)), 1)

        # Ensure we can't be friends with ourselves
        with self.assertRaises(ValidationError):
            Friend.objects.add_friend(self.user_bob, self.user_bob)

        # Ensure we can't do it manually either
        with self.assertRaises(ValidationError):
            Friend.objects.create(to_user=self.user_bob, from_user=self.user_bob)

    def test_already_friends_with_request(self):
        # Make Bob and Steve friends
        req = Friend.objects.add_friend(self.user_bob, self.user_steve)
        req.accept()

        with self.assertRaises(AlreadyFriendsError):
            req2 = Friend.objects.add_friend(self.user_bob, self.user_steve)

    def test_multiple_friendship_requests(self):
        """ Ensure multiple friendship requests are handled properly """
        ### Bob wants to be friends with Steve
        req1 = Friend.objects.add_friend(self.user_bob, self.user_steve)

        # Ensure neither have friends already
        self.assertEqual(Friend.objects.friends(self.user_bob), [])
        self.assertEqual(Friend.objects.friends(self.user_steve), [])

        # Ensure FriendshipRequest is created
        self.assertEqual(FriendshipRequest.objects.filter(from_user=self.user_bob).count(), 1)
        self.assertEqual(FriendshipRequest.objects.filter(to_user=self.user_steve).count(), 1)
        self.assertEqual(Friend.objects.unread_request_count(self.user_steve), 1)

        # Steve also wants to be friends with Bob before Bob replies
        req2 = Friend.objects.add_friend(self.user_steve, self.user_bob)

        # Ensure they aren't friends at this point
        self.assertFalse(Friend.objects.are_friends(self.user_bob, self.user_steve))

        # Accept the request
        req1.accept()

        # Ensure neither have pending requests
        self.assertEqual(FriendshipRequest.objects.filter(from_user=self.user_bob).count(), 0)
        self.assertEqual(FriendshipRequest.objects.filter(to_user=self.user_steve).count(), 0)
        self.assertEqual(FriendshipRequest.objects.filter(from_user=self.user_steve).count(), 0)
        self.assertEqual(FriendshipRequest.objects.filter(to_user=self.user_bob).count(), 0)

    def test_multiple_calls_add_friend(self):
        """ Ensure multiple calls with same friends, but different message works as expected """
        req1 = Friend.objects.add_friend(self.user_bob, self.user_steve, message='Testing')

        with self.assertRaises(AlreadyExistsError):
            req2 = Friend.objects.add_friend(self.user_bob, self.user_steve, message='Foo Bar')

    def test_following(self):
        # Bob follows Steve
        req1 = Follow.objects.add_follower(self.user_bob, self.user_steve)
        self.assertEqual(len(Follow.objects.followers(self.user_steve)), 1)
        self.assertEqual(len(Follow.objects.following(self.user_bob)), 1)
        self.assertEqual(Follow.objects.followers(self.user_steve), [self.user_bob])
        self.assertEqual(Follow.objects.following(self.user_bob), [self.user_steve])

        self.assertTrue(Follow.objects.follows(self.user_bob, self.user_steve))
        self.assertFalse(Follow.objects.follows(self.user_steve, self.user_bob))

        # Duplicated requests raise a more specific subclass of IntegrityError.
        with self.assertRaises(IntegrityError):
            Follow.objects.add_follower(self.user_bob, self.user_steve)
        with self.assertRaises(AlreadyExistsError):
            Follow.objects.add_follower(self.user_bob, self.user_steve)

        # Remove the relationship
        self.assertTrue(Follow.objects.remove_follower(self.user_bob, self.user_steve))
        self.assertEqual(len(Follow.objects.followers(self.user_steve)), 0)
        self.assertEqual(len(Follow.objects.following(self.user_bob)), 0)
        self.assertFalse(Follow.objects.follows(self.user_bob, self.user_steve))

        # Ensure we canot follow ourselves
        with self.assertRaises(ValidationError):
            Follow.objects.add_follower(self.user_bob, self.user_bob)

        with self.assertRaises(ValidationError):
            Follow.objects.create(follower=self.user_bob, followee=self.user_bob)


class FriendshipViewTests(BaseTestCase):

    def setUp(self):
        super(FriendshipViewTests, self).setUp()
        self.friendship_request = Friend.objects.add_friend(self.user_steve, self.user_bob)

    def test_friendship_view_users(self):
        url = reverse('friendship_view_users')

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse200(response)

        with self.settings(FRIENDSHIP_CONTEXT_OBJECT_LIST_NAME='object_list', TEMPLATE_DIRS=(TEST_TEMPLATES,)):
            response = self.client.get(url)
            self.assertResponse200(response)
            self.assertTrue('object_list' in response.context)

    def test_friendship_view_friends(self):
        url = reverse('friendship_view_friends', kwargs={'username': self.user_bob.username})

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse200(response)
        self.assertTrue('user' in response.context)

        with self.settings(FRIENDSHIP_CONTEXT_OBJECT_NAME='object', TEMPLATE_DIRS=(TEST_TEMPLATES,)):
            response = self.client.get(url)
            self.assertResponse200(response)
            self.assertTrue('object' in response.context)

    def test_friendship_add_friend(self):
        url = reverse('friendship_add_friend', kwargs={'to_username': self.user_amy.username})

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse302(response)

        with self.login(self.user_bob.username, self.user_pw):
            # if we don't POST the view should return the
            # friendship_add_friend view
            response = self.client.get(url)
            self.assertResponse200(response)

            # on POST accept the friendship request and redirect to the
            # friendship_request_list view
            response = self.client.post(url)
            self.assertResponse302(response)
            redirect_url = reverse('friendship_request_list')
            self.assertTrue(redirect_url in response['Location'])

    def test_friendship_add_friend_dupe(self):
        url = reverse('friendship_add_friend', kwargs={'to_username': self.user_amy.username})

        with self.login(self.user_bob.username, self.user_pw):
            # if we don't POST the view should return the
            # friendship_add_friend view

            # on POST accept the friendship request and redirect to the
            # friendship_request_list view
            response = self.client.post(url)
            self.assertResponse302(response)
            redirect_url = reverse('friendship_request_list')
            self.assertTrue(redirect_url in response['Location'])

            response = self.client.post(url)
            self.assertResponse200(response)
            self.assertTrue('errors' in response.context)
            self.assertEqual(response.context['errors'], ['Friendship already requested'])

    def test_friendship_requests(self):
        url = reverse('friendship_request_list')

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse302(response)

        with self.login(self.user_bob.username, self.user_pw):
            response = self.client.get(url)
            self.assertResponse200(response)

    def test_friendship_requests_rejected(self):
        url = reverse('friendship_requests_rejected')

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse302(response)

        with self.login(self.user_bob.username, self.user_pw):
            response = self.client.get(url)
            self.assertResponse200(response)

    def test_friendship_accept(self):
        url = reverse('friendship_accept', kwargs={'friendship_request_id': self.friendship_request.pk})

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse302(response)

        with self.login(self.user_bob.username, self.user_pw):
            # if we don't POST the view should return the
            # friendship_requests_detail view
            response = self.client.get(url)
            self.assertResponse302(response)
            redirect_url = reverse('friendship_requests_detail', kwargs={'friendship_request_id': self.friendship_request.pk})
            self.assertTrue(redirect_url in response['Location'])

            # on POST accept the friendship request and redirect to the
            # friendship_view_friends view
            response = self.client.post(url)
            self.assertResponse302(response)
            redirect_url = reverse('friendship_view_friends', kwargs={'username': self.user_bob.username})
            self.assertTrue(redirect_url in response['Location'])

        with self.login(self.user_steve.username, self.user_pw):
            # on POST try to accept the friendship request
            # but I am logged in as Steve, so I cannot accept
            # a request sent to Bob
            response = self.client.post(url)
            self.assertResponse404(response)

    def test_friendship_reject(self):
        url = reverse('friendship_reject', kwargs={'friendship_request_id': self.friendship_request.pk})

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse302(response)

        with self.login(self.user_bob.username, self.user_pw):
            # if we don't POST the view should return the
            # friendship_requests_detail view
            response = self.client.get(url)
            self.assertResponse302(response)
            redirect_url = reverse('friendship_requests_detail', kwargs={'friendship_request_id': self.friendship_request.pk})
            self.assertTrue(redirect_url in response['Location'])

            # on POST reject the friendship request and redirect to the
            # friendship_requests view
            response = self.client.post(url)
            self.assertResponse302(response)
            redirect_url = reverse('friendship_request_list')
            self.assertTrue(redirect_url in response['Location'])

        with self.login(self.user_steve.username, self.user_pw):
            # on POST try to reject the friendship request
            # but I am logged in as Steve, so I cannot reject
            # a request sent to Bob
            response = self.client.post(url)
            self.assertResponse404(response)

    def test_friendship_cancel(self):
        url = reverse('friendship_cancel', kwargs={'friendship_request_id': self.friendship_request.pk})

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse302(response)

        with self.login(self.user_bob.username, self.user_pw):
            # if we don't POST the view should return the
            # friendship_requests_detail view
            response = self.client.get(url)
            self.assertResponse302(response)
            redirect_url = reverse('friendship_requests_detail', kwargs={'friendship_request_id': self.friendship_request.pk})
            self.assertTrue(redirect_url in response['Location'])

            # on POST try to cancel the friendship request
            # but I am logged in as Bob, so I cannot cancel
            # a request made by Steve
            response = self.client.post(url)
            self.assertResponse404(response)

        with self.login(self.user_steve.username, self.user_pw):
            # on POST cancel the friendship request and redirect to the
            # friendship_requests view
            response = self.client.post(url)
            self.assertResponse302(response)
            redirect_url = reverse('friendship_request_list')
            self.assertTrue(redirect_url in response['Location'])

    def test_friendship_requests_detail(self):
        url = reverse('friendship_requests_detail', kwargs={'friendship_request_id': self.friendship_request.pk})

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse302(response)

        with self.login(self.user_bob.username, self.user_pw):
            response = self.client.get(url)
            self.assertResponse200(response)

    def test_friendship_followers(self):
        url = reverse('friendship_followers', kwargs={'username': 'bob'})

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse200(response)

        with self.settings(FRIENDSHIP_CONTEXT_OBJECT_NAME='object', TEMPLATE_DIRS=(TEST_TEMPLATES,)):
            response = self.client.get(url)
            self.assertResponse200(response)
            self.assertTrue('object' in response.context)

    def test_friendship_following(self):
        url = reverse('friendship_following', kwargs={'username': 'bob'})

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse200(response)

        with self.settings(FRIENDSHIP_CONTEXT_OBJECT_NAME='object', TEMPLATE_DIRS=(TEST_TEMPLATES,)):
            response = self.client.get(url)
            self.assertResponse200(response)
            self.assertTrue('object' in response.context)

    def test_follower_add(self):
        url = reverse('follower_add', kwargs={'followee_username': self.user_amy.username})

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse302(response)

        with self.login(self.user_bob.username, self.user_pw):
            response = self.client.get(url)
            self.assertResponse200(response)

            # on POST accept the friendship request and redirect to the
            # friendship_following view
            response = self.client.post(url)
            self.assertResponse302(response)
            redirect_url = reverse('friendship_following', kwargs={'username': self.user_bob.username})
            self.assertTrue(redirect_url in response['Location'])

            response = self.client.post(url)
            self.assertResponse200(response)
            self.assertTrue('errors' in response.context)
            self.assertEqual(response.context['errors'], ["User 'bob' already follows 'amy'"])

    def test_follower_remove(self):
        # create a follow relationship so we can test removing a follower
        follow = Follow.objects.add_follower(self.user_bob, self.user_amy)

        url = reverse('follower_remove', kwargs={'followee_username': self.user_amy.username})

        # test that the view requires authentication to access it
        response = self.client.get(url)
        self.assertResponse302(response)

        with self.login(self.user_bob.username, self.user_pw):
            response = self.client.get(url)
            self.assertResponse200(response)

            response = self.client.post(url)
            self.assertResponse302(response)
            redirect_url = reverse('friendship_following', kwargs={'username': self.user_bob.username})
            self.assertTrue(redirect_url in response['Location'])
