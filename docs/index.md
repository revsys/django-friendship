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

## Where to next

- [Usage](usage.md): the manager API, settings, and template tags
- [Signals](signals.md): the signals the app emits
- [API reference](reference.md): the managers, models, and exceptions

## llms.txt

This documentation is available in the [llms.txt](https://llmstxt.org/) format, a
Markdown convention suited to LLMs and AI coding assistants.

Two files are published:

- [`llms.txt`](https://django-friendship.readthedocs.io/en/latest/llms.txt): a
  short description of the project plus links to each section of the
  documentation. The structure is described [here](https://llmstxt.org/#format).
- [`llms-full.txt`](https://django-friendship.readthedocs.io/en/latest/llms-full.txt):
  the same index with the content of every page included inline, including the
  generated API reference.

Every page is also published as Markdown alongside its HTML, so you can link an
assistant at a single section rather than the whole corpus. Append `.md` to the
page name:

```text
https://django-friendship.readthedocs.io/en/latest/usage.md
https://django-friendship.readthedocs.io/en/latest/signals.md
https://django-friendship.readthedocs.io/en/latest/reference.md
```

These files are not picked up automatically by IDEs or coding agents today, but
most will use them if you supply a link or paste the text.
