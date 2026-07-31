# Signals

`django-friendship` emits a number of signals (from `friendship.signals`) after
various social actions.

!!! note

    These signals are only emitted when using the manager helper methods. They
    are **not** emitted if `FriendshipRequest`, `Follow`, or `Block` objects are
    created manually.

## Friendship request signals

### `friendship_request_created`

Sent whenever `FriendshipManager.add_friend` successfully creates a request.

- `sender` — the `FriendshipRequest` instance that was just created.

### `friendship_request_canceled`

Sent after `FriendshipRequest.cancel` deletes the request.

- `sender` — the `FriendshipRequest` that was canceled by its requester.

### `friendship_request_viewed`

Sent after `FriendshipRequest.mark_viewed` marks the request as viewed.

- `sender` — the `FriendshipRequest` that was viewed.

### `friendship_request_accepted`

Sent after `FriendshipRequest.accept` creates the two `Friend` objects.

- `sender` — the `FriendshipRequest` that was accepted.
- `from_user` — the request's `from_user`.
- `to_user` — the request's `to_user`.

### `friendship_request_rejected`

Sent from `FriendshipRequest.reject`.

- `sender` — the rejected `FriendshipRequest`.

### `friendship_removed`

Sent from `FriendshipManager.remove_friend`.

- `sender` — the removed `Friend` instance.
- `from_user`
- `to_user`

## Follow and block signals

!!! note

    The `*_created` follow/block signals send the **model class** as `sender`
    (`Follow` or `Block`), so you can connect a receiver with `sender=Follow` /
    `sender=Block`. The `*_removed` signals send the removed instance.

```python
from django.dispatch import receiver

from friendship.models import Follow
from friendship.signals import follower_created


@receiver(follower_created, sender=Follow)
def on_follow(sender, follower, **kwargs):
    ...
```

### `follower_created`

Sent by `FollowingManager.add_follower`.

- `sender` — the `Follow` model class.
- `follower` — the user who is now following someone.

### `followee_created`

Sent by `FollowingManager.add_follower`.

- `sender` — the `Follow` model class.
- `followee` — the user who is now being followed.

### `following_created`

Sent by `FollowingManager.add_follower`.

- `sender` — the `Follow` model class.
- `following` — the newly created `Follow` instance.

### `follower_removed`

Sent by `FollowingManager.remove_follower`.

- `sender` — the removed `Follow` instance.
- `follower` — the user who was following.

### `followee_removed`

Sent by `FollowingManager.remove_follower`.

- `sender` — the removed `Follow` instance.
- `followee` — the user who was being followed.

### `following_removed`

Sent by `FollowingManager.remove_follower`.

- `sender` — the removed `Follow` instance.
- `following` — the removed `Follow` instance.

### `block_created`

Sent by `BlockManager.add_block`, once each with `blocker`, `blocked`, and
`blocking`.

- `sender` — the `Block` model class.

### `block_removed`

Sent by `BlockManager.remove_block`, once each with `blocker`, `blocked`, and
`blocking`.

- `sender` — the removed `Block` instance.
