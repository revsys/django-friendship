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

        # Can optionally save a message when creating friend requests
        some_other_user = User.objects.get(pk=2)
        message_relationship = Friend.objects.add_friend(
            from_user=request.user,
            to_user=some_other_user,
            message='Hi, I would like to be your friend',
        )

        # Attempting to create an already existing friendship will raise
        # `friendship.exceptions.AlreadyExistsError`, a subclass of
        # `django.db.IntegrityError`.
        dupe_relationship = Friend.objects.add_friend(request.user, other_user)
        AlreadyExistsError: u'Friendship already requested'

        # Create request.user follows other_user relationship
        following_created = Following.objects.add_follower(request.user, other_user)

        # Attempting to add an already existing follower will also raise
        # `friendship.exceptions.AlreadyExistsError`,
        dupe_following = Following.objects.add_follower(request.user, other_user)
        AlreadyExistsError: u"User 'alice' already follows 'bob'"

        was_following = Following.objects.remove_follower(request.user, other_user)

        # Create request.user blocks other_user relationship
        block_created = Block.objects.add_block(request.user, other_user)

        # Remove request.user blocks other_user relationship
        block_remove = Block.objects.remove_block(request.user, other_user)



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
settings.FRIENDSHIP_CONTEXT_OBJECT_NAME == 'user'
settings.FRIENDSHIP_CONTEXT_OBJECT_LIST_NAME = 'users'
