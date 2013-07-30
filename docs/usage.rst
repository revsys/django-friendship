=====
Usage
=====


Installation
============

* Install friend using your favorite package manager (which is pip)::

    pip install django-friendship

* Add ``friendship`` to ``INSTALLED_APPS``
* run ``syncdb``::

    manage.py syncdb

Examples
========

To use ``django-friendship`` in your views::

    from django.contrib.auth.models import User
    from friendship.models import Friend, Following

    def my_view(request):
        # List of this user's friends
        all_friends = Friend.objects.friends(request.user)

        # List all unread friendship requests
        requests = Friend.objects.unread_requests(user=request.user)

        # List all rejected friendship requests
        rejects = Friend.objects.rejected_requests(user=request.user)

        # List of this user's followers
        all_followers = Following.objects.followers(request.user)

        # List of who this user is following
        following = Following.objects.following(request.user)

        ### Managing friendship relationships
        other_user = User.objects.get(pk=1)
        new_relationship = Friend.objects.add_friend(request.user, other_user)
        Friend.objects.are_friends(request.user, other_user) == True
        Friend.objects.remove_friend(other_user, request.user)

        # Create request.user follows other_user relationship
        following_created = Following.objects.add_follower(request.user, other_user)
        was_following = Following.objects.remove_follower(request.user, other_user)


To use ``django-friendship`` in your templates::

   {% load friendshiptags %}

   {% friends request.user %}
   {% followers request.user %}
   {% following request.user %}
   {% friend_requests request.user %}
   {% friend_request_count request.user %}


Settings
========
settings.DEFAULT_CACHE_VALUE == 86400 seconds (24 hours)

