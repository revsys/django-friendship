# Signals

`django-friendship` emits [Django signals](https://docs.djangoproject.com/en/stable/topics/signals/)
(from `friendship.signals`) after various social actions, so you can react to
them — send a notification, write an audit log, invalidate a cache — without
patching the app.

!!! note

    Signals are only emitted when you go through the manager helper methods
    (`add_friend`, `add_follower`, `add_block`, `accept`, …). Creating or deleting
    `FriendshipRequest`, `Follow`, or `Block` rows directly does **not** fire them.

## Connecting a receiver

Import the signal and connect a receiver with `@receiver`. Read the values you
care about from the keyword arguments, and always accept `**kwargs` so your
receiver keeps working if more arguments are added:

```python
from django.dispatch import receiver

from friendship.models import Follow
from friendship.signals import follower_created


@receiver(follower_created, sender=Follow)
def notify_on_follow(sender, follower, **kwargs):
    # `follower` is the user who just started following someone.
    ...
```

## What `sender` is, and why it matters

`sender` lets you scope a receiver with `@receiver(signal, sender=...)`. In
`django-friendship` it is not the same kind of object for every signal:

| Signals | `sender` |
| --- | --- |
| Follow/block **`*_created`** (`follower_created`, `followee_created`, `following_created`, `block_created`) | the **model class** (`Follow` or `Block`) |
| Follow/block **`*_removed`** (`follower_removed`, `followee_removed`, `following_removed`, `block_removed`) | the **removed instance** (`Follow` / `Block`) |
| Friendship-request signals and `friendship_removed` | the relevant **instance** (`FriendshipRequest`, or the removed `Friend`) |

So `@receiver(follower_created, sender=Follow)` works, but connecting to
`follower_removed` with `sender=Follow` would **not** match — the removed
signals send an instance, so connect to them without a `sender` and filter
inside the receiver if you need to.

## Two behaviors worth knowing

!!! warning "`add_follower` emits three _different_ signals"

    A single `Follow.objects.add_follower(...)` call sends `follower_created`,
    `followee_created`, and `following_created` — once each — carrying the
    follower, the followee, and the new `Follow` row respectively. Connect to the
    one that matches what you need.

!!! warning "`block_created` and `block_removed` fire _three times_ per call"

    A single `Block.objects.add_block(...)` sends `block_created` three times:
    once with `blocker=`, once with `blocked=`, and once with `blocking=` (the
    `Block` row). Each fire carries only **one** of those keys, so a receiver on
    `block_created` runs three times per block. Guard for the key you want:

    ```python
    from friendship.models import Block
    from friendship.signals import block_created


    @receiver(block_created, sender=Block)
    def on_block(sender, **kwargs):
        if "blocking" in kwargs:  # the Block row; fires once per add_block
            block = kwargs["blocking"]
            ...
    ```

## Friendship request signals

### `friendship_request_created`

Sent when `Friend.objects.add_friend(...)` successfully creates a request.

- `sender` — the newly created `FriendshipRequest`.

### `friendship_request_accepted`

Sent when `FriendshipRequest.accept()` creates the two `Friend` rows.

- `sender` — the accepted `FriendshipRequest`.
- `from_user` — the user who sent the request.
- `to_user` — the user who accepted it.

### `friendship_request_rejected`

Sent from `FriendshipRequest.reject()`.

- `sender` — the rejected `FriendshipRequest`.

### `friendship_request_canceled`

Sent after `FriendshipRequest.cancel()` deletes the request.

- `sender` — the `FriendshipRequest` that was canceled by its sender.

### `friendship_request_viewed`

Sent after `FriendshipRequest.mark_viewed()` marks the request as viewed.

- `sender` — the viewed `FriendshipRequest`.

### `friendship_removed`

Sent from `Friend.objects.remove_friend(...)`.

- `sender` — the removed `Friend` instance.
- `from_user` — one side of the friendship.
- `to_user` — the other side.

## Follow signals

Sent by `Follow.objects.add_follower(...)` (created) and
`Follow.objects.remove_follower(...)` (removed). The `*_created` signals send
`Follow` (the class) as `sender`; the `*_removed` signals send the removed row.

### `follower_created`

- `sender` — the `Follow` class.
- `follower` — the user who is now following someone.

### `followee_created`

- `sender` — the `Follow` class.
- `followee` — the user who is now being followed.

### `following_created`

- `sender` — the `Follow` class.
- `following` — the newly created `Follow` row.

### `follower_removed`

- `sender` — the removed `Follow` row.
- `follower` — the user who was following.

### `followee_removed`

- `sender` — the removed `Follow` row.
- `followee` — the user who was being followed.

### `following_removed`

- `sender` — the removed `Follow` row.
- `following` — the removed `Follow` row.

## Block signals

Both fire **three times** per call (see [above](#two-behaviors-worth-knowing)),
once each with `blocker`, `blocked`, and `blocking`.

### `block_created`

Sent by `Block.objects.add_block(...)`.

- `sender` — the `Block` class.
- one of `blocker` (the user doing the blocking), `blocked` (the user being
  blocked), or `blocking` (the new `Block` row).

### `block_removed`

Sent by `Block.objects.remove_block(...)`.

- `sender` — the removed `Block` row.
- one of `blocker`, `blocked`, or `blocking` (the removed `Block` row).
