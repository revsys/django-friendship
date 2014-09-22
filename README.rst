django-friendship
=================

.. image:: https://secure.travis-ci.org/revsys/django-friendship.png
    :alt: Build Status
    :target: http://travis-ci.org/revsys/django-friendship

Usage
=====

Add ``friendship`` to ``INSTALLED_APPS`` and run ``syncdb``.

To use ``django-friendship`` in your views::

    from django.contrib.auth.models import User
    from friendship.models import Friend, Follow

    def my_view(request):
        # List of this user's friends
        all_friends = Friend.objects.friends(request.user)

        # List all unread friendship requests
        requests = Friend.objects.unread_requests(user=request.user)

        # List all rejected friendship requests
        rejects = Friend.objects.rejected_requests(user=request.user)

        # Count of all rejected friendship requests
        reject_count = Friend.objects.rejected_request_count(user=request.user)

        # List all unrejected friendship requests
        unrejects = Friend.objects.unrejected_requests(user=request.user)

        # Count of all unrejected friendship requests
        unreject_count = Friend.objects.unrejected_request_count(user=request.user)

        # List all sent friendship requests
        sent = Friend.objects.sent_requests(user=request.user)

        # List of this user's followers
        all_followers = Following.objects.followers(request.user)

        # List of who this user is following
        following = Following.objects.following(request.user)

        ### Managing friendship relationships

        # Create a friendship request
        other_user = User.objects.get(pk=1)
        new_relationship = Friend.objects.add_friend(request.user, other_user)

        # Can optionally save a message when creating friend requests
        message_relationship = Friend.objects.add_friend(
            from_user=request.user,
            to_user=some_other_user,
            message='Hi, I would like to be your friend',
        )

        # And immediately accept it, normally you would give this option to the user
        new_relationship.accept()

        # Now the users are friends
        Friend.objects.are_friends(request.user, other_user) == True

        # Remove the friendship
        Friend.objects.remove_friend(other_user, request.user)

        # Create request.user follows other_user relationship
        following_created = Following.objects.add_follower(request.user, other_user)

To use ``django-friendship`` in your templates::

   {% load friendshiptags %}

   {% friends request.user %}
   {% followers request.user %}
   {% following request.user %}
   {% friend_requests request.user %}

Signals
=======

``django-friendship`` emits the following signals:

* friendship_request_created
* friendship_request_rejected
* friendship_request_canceled
* friendship_request_accepted
* friendship_removed
* follower_created
* following_created
* follower_removed
* following_removed

Compatibility
=============

This package requires Django 1.4 and above since v0.9.0. It is currently tested by Travis-CI against 1.4.12, 1.5.7, 1.6.4, and 1.7b1.

The last release supporting Django 1.3 is v0.8.3.
