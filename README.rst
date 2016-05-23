Django-Friendship
=================

.. image:: https://secure.travis-ci.org/revsys/django-friendship.png
    :alt: Build Status
    :target: http://travis-ci.org/revsys/django-friendship

This application enables you to create and manage follows and bi-d
This application enables you to create and manage follows and bi-directional friendships between users. It features:

* Friendship request objects that can be accepted, rejected, canceled, or marked as viewed.
* Hooks to easily list all friend requests sent or received by a given user, filtered by the status of the request.
* Tags to include information about friendships and follows in your templates.
* Integration with ``AUTH_USER_MODEL``.
* Validation to prevent common mistakes.
* Faster server response time through caching

Requirements
============

**Django 1.4** since v0.9.0 (latest release supporting **Django 1.3** is v0.8.3)

Installation
============

1. ``pip install django-friendship``
2. add ``"friendship"`` to ``INSTALLED_APPS`` and run ``python manage.py migrate``.
3. Use the friendship manager in your own views, or wire up the URLconf to include the builtin views: ::

    urlpatterns = [
        ...
        url(r'^friendship/', include('friendship.urls'))
        ...
    ]

Usage
=====

``django-friendship`` provides a free API that gives you several ways to create and manage friendship requests or follows in your views. Add the following at the top of your ``views.py``::

    from django.contrib.auth.models import User
    from friendship.models import Friend, Follow

Getting Data about Friendships
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* List all of a user's friends: ``Friend.objects.friends(request.user)``
* List all unread friendship requests: ``Friend.objects.unread_requests(user=request.user)``
* List all unrejected friendship requests: ``Friend.objects.unrejected_requests(user=request.user)``
* Count of all unrejected friendship requests: ``Friend.objects.unrejected_request_count(user=request.user)``
* List all rejected friendship requests: ``Friend.objects.rejected_requests(user=request.user)``
* Count of all rejected friendship requests: ``Friend.objects.rejected_request_count(user=request.user)``
* List of all sent friendship requests: ``Friend.objects.sent_requests(user=request.user)``
* Test if two users are friends: ``Friend.objects.are_friends(request.user, other_user) == True``

Getting Data about Follows
~~~~~~~~~~~~~~~~~~~~~~~~~~
* List of a user's followers: ``Follow.objects.followers(request.user)``
* List of who a user is following: ``Follow.objects.following(request.user)``

Managing Friendships and Follows
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Create a friendship request: ::

    other_user = User.objects.get(pk=1)
    Friend.objects.add_friend(
        request.user,                               # The sender
        other_user,                                 # The recipient
        message='Hi! I would like to add you')      # This message is optional

* Let the user who received the request respond: ::

    from friendship.models import FriendshipRequest

    friend_request = FriendshipRequest.objects.get(pk=1)
    friend_request.accept()
    # or friend_request.reject()

* To remove the friendship relationship between ``request.user`` and ``other_user``, do the following: ::

    Friend.objects.remove_friend(request.user, other_user)

* Make request.user a follower of other_user: ::

    Follow.objects.add_follower(request.user, other_user)

Templates
=========

You can use ``django-friendship`` tags in your templates. First enter: ::

    {% load friendshiptags %}

Then use any of the following: ::

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


Contributing
============

Development `takes place on GitHub`__. Bug reports, patches, and fixes are always welcome!

__ https://github.com/revsys/django-friendship
