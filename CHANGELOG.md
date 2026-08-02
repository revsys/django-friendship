# Changelog

## Unreleased

_Not released yet_

## Version 1.11.1

_Released August 1st, 2026_

- Test against Python 3.15, including the free-threaded build (3.15t). It is
  still in beta, so the trove classifier is published but support is not
  promised until the final release.

## Version 1.11.0

_Released July 31st, 2026_

- Fix `Follow` and `Block` `*_created` signals to send the model class as
  `sender` so receivers connected with `sender=Follow` / `sender=Block`
  fire (#89)
- Use the `str` URL converter for usernames so usernames containing `.`,
  `@`, `+` or unicode reverse correctly instead of raising
  `NoReverseMatch` (#109)
- Add `FriendshipManager.request_exists(from_user, to_user)` to check for a
  pending friendship request in either direction without duplicating the
  queries (#198)
- Allow a friendship request to be sent again after it was rejected, instead of
  raising `AlreadyExistsError` forever. The previously rejected request is
  revived as a fresh, unread request; use the block feature to stop unwanted
  requests. **Behavior change:** a single rejection no longer permanently blocks
  future requests (#193)
- Add an optional `FRIENDSHIP_MAX_FRIENDS` setting that caps the number of
  friends per user, enforced when a request is accepted (raises
  `MaxFriendsExceededError`). Unset by default, so friendships remain unlimited.
  Adds a `FriendshipManager.friend_count(user)` helper (#82)
- The bundled views and templates now resolve users by the user model's
  `USERNAME_FIELD` (via `get_username()`) instead of a hardcoded `username`, so
  they work with custom user models that use a different `USERNAME_FIELD` (e.g.
  email). No change for the default user model (#57)
- Migrate the documentation from Sphinx to zensical (Markdown) and generate
  `llms.txt` / `llms-full.txt` (#214)

## Version 1.10.0

_Released July 30th, 2026_

- Add support for Django 4.2, 5.0, 5.1, 5.2, 6.0, and 6.1
- Add support for Python 3.10 through 3.14, including free-threaded 3.14
- Move packaging to `pyproject.toml` with the hatchling build backend and
  modernize tooling (nox test matrix, ruff/prek pre-commit, split CI workflows)
- Add ability to use `prefetch_related` rather than `select_related` for
  memory/cache size reduction
- Fix signal sending issue on cancel after object is deleted

## Version 1.9.6

_Released March 13th, 2022_

- ORM performance improvements

## Version 1.9.5

_Released March 13th, 2022_

- Officially support Django 4.0 in trove classifiers

## Version 1.9.4

_Released October 5th, 2021_

- Fix bumpversion related release issue

## Version 1.9.3

_Released October 4th, 2021_

- Fix PyPI deploy process to use main instead of master (actually release what should have been in 1.9.2)
- Fix Django deprecation warnings

## Version 1.9.2

_Released August 25th 2021_

- Broken release, mostly a duplicate of 1.9.1 due to branch renaming issue

## Version 1.9.1

_Released April 9th, 2020_

- Add missing migration.

## Version 1.9.0

_Released April 7th, 2020_

- Drop support for Python 2
- Add support for Django 3.0

## Version 1.8.2

_Released November 27th, 2019_

- Fixed bug with viewing rejected friend requests
- Added friends QuerySet to view context
- Reduce fields queried when not necessary
- Update Travis to check Python 3.8

## Version 1.8.1

_Released May 24th, 2019_

- Fixed bug in `friendship_request_list` view
- Refactored `can_request_send` to be more clear
- Ran Black over the codebase

## Version 1.8.0

_Released July 6th, 2018_

- Fix migrations for people migrating from <= 1.5.x.
  If you are migrating from 1.6 or 1.7, please rollback django-friendships
  migrations to 0001 and migrate-fake 0002:

  ```
  $ ./manage.py migrate friendship 0001
  $ ./manage.py migrate friendship 0002 --fake
  ```

  If you're migrating from `v1.7.x`, you'll likely have to fake `0003` as well:

  ```
  $ ./manage.py migrate friendship 0003 --fake
  ```

## Version 1.7.1

_Released July 5th, 2018_

- Bugfix, missing migration

## Version 1.7.0

_Released July 2nd, 2018_

- Add support for Django 2.0
- Drop support for Django < 1.11

## Version 1.6.0

_Released May 22nd, 2018_

- Added can_request_send option (narnikgamarnik)
- Added blocking feature (Darren Mckeeman)

## Version 1.5.0

_Released August 21st, 2016_

- Added support for Django 1.10

## Version 1.4.0

_Released July 23rd, 2016_

- Moved template tag to assignment_tag to avoid Django 1.9 error

## Version 1.3.3

_Released July 1st, 2016_

- Support non-integer primary keys in cache keys
- Remove support for Django 1.4

## Version 1.3.1

_Released November 11th, 2015_

- Raise AlreadyFriendError if creating request when users are already friends
- PEP8 cleanups

## Version 1.3.0

_Released July 12th, 2015_

- Updated Django 1.7 and 1.8 compatibility
- Signal related bug fixes
- Python 3 compatibility

## Version 1.2.0

_Released September 22nd, 2014_

- Updated test runner for 1.7 compatibility
- Fixed security issue where we were not checking the owner of a FriendRequest during accept and
  cancelation
- Added optional 'message' kwarg to FriendshipManager.add_friend() so it is easier to set the
  optional message field on FriendshipRequests

## Version 1.1.0

_Released May 6th, 2014_

- Added Django 1.7 compatibility.
- Fixed caching issue with sent_requests.
- Added unrejected_requests() and unrejected_request_count() manager methods.

## Version 1.0.0

_Released November 13th, 2013_

- Fixed bug where FriendRequests could be left hanging if both sides requested friendship prior to
  one side accepting.  Caused exception if the user accepted the second request.
- Fixed ordering of friendship_request_rejected signal to not fire until DB is updated.
- Fixed Django 1.6 compatibility issue
- 1.0 release whoo hoo!

## Changes prior to version 0.9.0

Lots.  We didn't keep good track of issues prior to 1.0.0.
