=======
Signals
=======

``django-friendship`` emits a number of signals after various social actions

.. admonition:: Note

    These signals are only emitted when using the noted helper functions. These will not be emitted if Request or Follow objects are created manually.


* **friendship_request_created**
    Sent whenever FriendshipManager.add_friend successfully created a friendship request.

    Arguments sent:

    ``sender``
        The FriendshipRequest instance that has just been created

* **friendship_request_canceled**
    Sent after FriendshipRequest.cancel deletes the ``sender`` FriendshipRequest object.

    ``sender``
        The Friendship instance that was just canceled by it's requester.

* **friendship_request_viewed**
    Sent after FriendshipRequest.mark_viewed marks ``sender`` as viewed.

    ``sender``
        The FriendshipRequest objected viewed.

* **friendship_request_accepted**
    Sent after FriendshipRequest.accept is called to mark the request as accepted, creating two Friend objects.

    ``sender``
        The FriendshipRequest object accepted.

    ``from_user``
        The FriendshipRequest.from_user User object

    ``to_user``
        The FriendshipRequest.to_user User object

* **friendship_request_rejected**

    ``sender``
        The rejected FriendshipRequest. Sent from FriendshipRequest.reject.

* **friendship_removed**

    ``sender``

    ``from_user``

    ``to_user``

.. admonition:: Note

    The follow and block ``*_created`` signals send the **model class** as
    ``sender`` (``Follow`` or ``Block``), so you can connect a receiver with
    ``sender=Follow`` / ``sender=Block``. The ``*_removed`` signals send the
    removed instance.

* **follower_created**
    Sent by FollowingManager.add_follower.

    ``sender``
        The ``Follow`` model class.

    ``follower``
        The user who is now following someone.

* **followee_created**
    Sent by FollowingManager.add_follower.

    ``sender``
        The ``Follow`` model class.

    ``followee``
        The user who is now being followed.

* **following_created**
    Sent by FollowingManager.add_follower.

    ``sender``
        The ``Follow`` model class.

    ``following``
        The newly created ``Follow`` instance.

* **follower_removed**
    Sent by FollowingManager.remove_follower.

    ``sender``
        The removed ``Follow`` instance.

    ``follower``
        The user who was following.

* **followee_removed**
    Sent by FollowingManager.remove_follower.

    ``sender``
        The removed ``Follow`` instance.

    ``followee``
        The user who was being followed.

* **following_removed**
    Sent by FollowingManager.remove_follower.

    ``sender``
        The removed ``Follow`` instance.

    ``following``
        The removed ``Follow`` instance.

* **block_created**
    Sent by BlockManager.add_block, once each with ``blocker``, ``blocked``, and ``blocking``.

    ``sender``
        The ``Block`` model class.

* **block_removed**
    Sent by BlockManager.remove_block, once each with ``blocker``, ``blocked``, and ``blocking``.

    ``sender``
        The removed ``Block`` instance.
