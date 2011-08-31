from django.contrib.auth.models import User
from django.test import TestCase 
from django.test.client import Client 
from django.core.urlresolvers import reverse

from friendship.models import Friend, Follow, FriendshipRequest


class FriendshipModelTests(TestCase):

    def setUp(self):
        """ Setup some initial users """ 
        self.user_bob = User.objects.create_user('bob', 'bob@bob.com', 'bobpass')
        self.user_steve = User.objects.create_user('steve', 'steve@steve.com', 'stevepass') 
        self.user_susan = User.objects.create_user('susan', 'susan@susan.com', 'susanpass')
        self.user_amy = User.objects.create_user('amy', 'amy@amy.amy.com', 'amypass') 

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
        self.assertEqual(len(Friend.objects.unread_requests(self.user_steve)), 1)
        self.assertEqual(len(Friend.objects.rejected_requests(self.user_steve)), 0)

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

        self.assertFalse(Friend.objects.are_friends(self.user_susan, self.user_amy)) 
        self.assertEqual(len(Friend.objects.rejected_requests(self.user_amy)), 1)

        # Susan wants to be friends with Amy, and Amy reads it
        req4 = Friend.objects.add_friend(self.user_susan, self.user_amy) 
        req4.mark_viewed()

        self.assertFalse(Friend.objects.are_friends(self.user_susan, self.user_amy)) 
        self.assertEqual(len(Friend.objects.rejected_requests(self.user_amy)), 1)

        self.assertEqual(len(Friend.objects.read_requests(self.user_amy)), 1)

    def test_following(self):
        # Bob follows Steve 
        req1 = Follow.objects.add_follower(self.user_bob, self.user_steve)
        self.assertEqual(len(Follow.objects.followers(self.user_steve)), 1) 
        self.assertEqual(len(Follow.objects.following(self.user_bob)), 1) 
        self.assertEqual(Follow.objects.followers(self.user_steve), [self.user_bob])
        self.assertEqual(Follow.objects.following(self.user_bob), [self.user_steve])

        self.assertTrue(Follow.objects.follows(self.user_bob, self.user_steve)) 
        self.assertFalse(Follow.objects.follows(self.user_steve, self.user_bob))

        # Remove the relationship 
        self.assertTrue(Follow.objects.remove_follower(self.user_bob, self.user_steve)) 
        self.assertEqual(len(Follow.objects.followers(self.user_steve)), 0) 
        self.assertEqual(len(Follow.objects.following(self.user_bob)), 0) 
        self.assertFalse(Follow.objects.follows(self.user_bob, self.user_steve))

class FriendshipViewTests(TestCase):

    def setUp(self):
        """ Setup some initial users """ 
        self.user_bob = User.objects.create_user('bob', 'bob@bob.com', 'bobpass')
        self.user_steve = User.objects.create_user('steve', 'steve@steve.com', 'stevepass') 
        self.user_susan = User.objects.create_user('susan', 'susan@susan.com', 'susanpass')
        self.user_amy = User.objects.create_user('amy', 'amy@amy.amy.com', 'amypass') 

    def _is_200(self, url):
        client = Client()
        response = client.get(url)
        self.assertEqual(response.status_code, 200) 

    def test_simple_200s(self):
        """ Test that certain views return a 200 status code """
        self._is_200(reverse('friendship_view_friends', kwargs={'username': 'bob'}))
        self._is_200(reverse('friendship_followers', kwargs={'username': 'bob'}))
        self._is_200(reverse('friendship_following', kwargs={'username': 'bob'}))

