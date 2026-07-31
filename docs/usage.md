# Usage

`django-friendship` gives you a manager API for creating and managing
friendships, follows, and blocks. Import the models at the top of your
`views.py`:

```python
from django.contrib.auth.models import User
from friendship.models import Block, Friend, Follow
```

## Getting data about friendships

```python
# List of this user's friends
Friend.objects.friends(request.user)

# Number of friends this user has
Friend.objects.friend_count(request.user)

# Requests, filtered by status
Friend.objects.unread_requests(user=request.user)
Friend.objects.unrejected_requests(user=request.user)
Friend.objects.rejected_requests(user=request.user)
Friend.objects.sent_requests(user=request.user)

# Are two users friends?
Friend.objects.are_friends(request.user, other_user)

# Does a request already exist between two users (either direction)?
Friend.objects.request_exists(request.user, other_user)
```

## Managing friendships

```python
other_user = User.objects.get(pk=1)

# Create a friendship request (message is optional)
Friend.objects.add_friend(
    request.user,
    other_user,
    message="Hi! I would like to add you",
)

# Attempting to create an existing friendship raises
# friendship.exceptions.AlreadyExistsError (a subclass of django.db.IntegrityError).

# Remove a friendship
Friend.objects.remove_friend(request.user, other_user)
```

Accept or reject a request on the `FriendshipRequest` object:

```python
from friendship.models import FriendshipRequest

friend_request = FriendshipRequest.objects.get(
    from_user=other_user, to_user=request.user
)
friend_request.accept()
# or friend_request.reject()
```

A rejected request does not block future requests — the sender may request again
later, and the rejected request is revived as a fresh, unread request.

### Limiting the number of friends

By default a user may have unlimited friends. Set `FRIENDSHIP_MAX_FRIENDS` to
cap it. The limit is checked when a request is accepted; if either user is
already at the limit, `accept()` raises `MaxFriendsExceededError` and no
friendship is created (the request is left intact so it can be accepted later):

```python
from friendship.exceptions import MaxFriendsExceededError

try:
    friend_request.accept()
except MaxFriendsExceededError:
    ...  # tell the user their friend list is full
```

## Follows

```python
# Create / remove a follow
Follow.objects.add_follower(request.user, other_user)
Follow.objects.remove_follower(request.user, other_user)

# Read follows
Follow.objects.followers(request.user)
Follow.objects.following(request.user)
```

## Blocks

```python
# Create / remove a block
Block.objects.add_block(request.user, other_user)
Block.objects.remove_block(request.user, other_user)

# Read blocks
Block.objects.blocked(request.user)
Block.objects.blocking(request.user)
Block.objects.is_blocked(request.user, other_user)
```

## Template tags

```django
{% load friendshiptags %}

{% friends request.user %}
{% followers request.user %}
{% following request.user %}
{% blockers request.user %}
{% blocking request.user %}
{% friend_requests request.user %}
{% friend_request_count request.user %}
{% friend_count request.user %}
{% friend_rejected_count request.user %}
```

## Custom user models

`django-friendship` works with a custom `AUTH_USER_MODEL`. The bundled views and
templates resolve users by the model's `USERNAME_FIELD` (via `get_username()`),
so a model that authenticates by email works out of the box. For the default
user model `USERNAME_FIELD` is `"username"`, so nothing changes.

## Settings

```python
# Context variable names used by the bundled views
FRIENDSHIP_CONTEXT_OBJECT_NAME = "user"
FRIENDSHIP_CONTEXT_OBJECT_LIST_NAME = "users"

# How friendship-request querysets fetch related rows
# ("select_related", "prefetch_related", "none")
FRIENDSHIP_MANAGER_FRIENDSHIP_REQUEST_SELECT_RELATED_STRATEGY = "select_related"

# Optional cap on friends per user. Unset (the default) means unlimited.
FRIENDSHIP_MAX_FRIENDS = 800
```
