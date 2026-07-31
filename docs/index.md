# django-friendship

Create and manage follows, blocks, and bi-directional friendships between
users. `django-friendship` features:

- Friendship request objects that can be accepted, rejected, canceled, or marked
  as viewed.
- Helpers to list all friend requests sent or received by a user, filtered by
  status.
- A per-user blocklist.
- Template tags for friendships, blocks, and follows.
- Integration with a custom `AUTH_USER_MODEL`.
- Validation to prevent common mistakes.
- Faster responses through caching.

## Installation

1. `pip install django-friendship`
2. Add `"friendship"` to `INSTALLED_APPS` and run `python manage.py migrate`.
3. Optionally wire up the bundled views by including the URLconf:

```python
urlpatterns = [
    # other paths
    path("friendship/", include("friendship.urls")),
]
```

See [Usage](usage.md) for the manager API and template tags, and
[Signals](signals.md) for the signals the app emits.
