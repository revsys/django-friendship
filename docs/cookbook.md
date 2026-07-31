# Cookbook

Task-oriented recipes for common things you'll do with `django-friendship`. Every
example assumes the models are imported:

```python
from friendship.models import Block, Follow, Friend, FriendshipRequest
```

## Send a friend request and handle the outcome

`add_friend` creates a `FriendshipRequest` and returns it. It raises when the
request can't be made, so handle those cases:

```python
from django.core.exceptions import ValidationError

from friendship.exceptions import AlreadyExistsError, AlreadyFriendsError

try:
    request = Friend.objects.add_friend(
        from_user=request.user,
        to_user=other_user,
        message="Hi! I would like to add you",  # optional
    )
except ValidationError:
    ...  # a user cannot friend themselves
except AlreadyFriendsError:
    ...  # they are already friends
except AlreadyExistsError:
    ...  # a pending request already exists (in either direction)
```

To check first instead of catching an exception:

```python
if Friend.objects.request_exists(from_user=request.user, to_user=other_user):
    ...  # a request is already pending
```

## Respond to a friend request

```python
friend_request = FriendshipRequest.objects.get(
    from_user=other_user, to_user=request.user
)

friend_request.accept()   # creates the friendship (fires friendship_request_accepted)
friend_request.reject()   # marks it rejected
friend_request.cancel()   # the sender withdraws it
```

A rejected request no longer blocks the future — the sender may
[`add_friend`](usage.md#managing-friendships) again, and the rejected request is
revived as a fresh, unread one.

## List friends and pending requests

```python
# Everyone request.user is friends with
Friend.objects.friends(user=request.user)

# Requests waiting for request.user to act on
Friend.objects.unread_requests(user=request.user)

# Requests request.user has sent
Friend.objects.sent_requests(user=request.user)
```

## Check whether two users are friends

```python
if Friend.objects.are_friends(user1=request.user, user2=other_user):
    ...
```

## Follow and unfollow

```python
Follow.objects.add_follower(follower=request.user, followee=other_user)
Follow.objects.remove_follower(follower=request.user, followee=other_user)

Follow.objects.followers(user=other_user)   # who follows other_user
Follow.objects.following(user=request.user)  # who request.user follows
```

## Block and unblock

```python
Block.objects.add_block(blocker=request.user, blocked=other_user)
Block.objects.remove_block(blocker=request.user, blocked=other_user)

Block.objects.is_blocked(user1=request.user, user2=other_user)
```

## Notify a user when they receive a friend request

Use the [`friendship_request_created`](signals.md#friendship_request_created)
signal so the notification is sent no matter where `add_friend` is called from:

```python
from django.dispatch import receiver

from friendship.signals import friendship_request_created


@receiver(friendship_request_created)
def email_on_request(sender, **kwargs):
    friend_request = sender  # the new FriendshipRequest
    notify(friend_request.to_user, f"{friend_request.from_user} wants to be friends")
```

See [Signals](signals.md) for every signal and its arguments.

## Cap how many friends a user can have

Set [`FRIENDSHIP_MAX_FRIENDS`](usage.md#settings) and handle the limit when a
request is accepted:

```python
from friendship.exceptions import MaxFriendsExceededError

try:
    friend_request.accept()
except MaxFriendsExceededError:
    ...  # this user's friend list is full
```

## Use a custom user model

Nothing special is required. The bundled views and templates resolve users by
your model's `USERNAME_FIELD` (via `get_username()`), so a model that
authenticates by email works out of the box. See
[Custom user models](usage.md#custom-user-models).
