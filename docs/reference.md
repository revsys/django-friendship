# API reference

## Managers

The manager methods are the main entry point — `Friend.objects`, `Follow.objects`,
and `Block.objects` are instances of these.

::: friendship.models.FriendshipManager

::: friendship.models.FollowingManager

::: friendship.models.BlockManager

## Models

::: friendship.models.FriendshipRequest

::: friendship.models.Friend

::: friendship.models.Follow

::: friendship.models.Block

## Exceptions

::: friendship.exceptions
    options:
      members:
        - AlreadyExistsError
        - AlreadyFriendsError
        - MaxFriendsExceededError
