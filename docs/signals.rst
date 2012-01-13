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

* **friendship_request_canceled`**
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

* **follower_created**

    ``sender``

    ``follower``

* **following_created**

    ``sender``

    ``followee``

* **follower_removed**

    ``sender``

    ``follower``

* **following_removed**

    ``sender``

    ``following``
