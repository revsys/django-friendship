Version 1.8.0
-------------

*Released July 6th, 2018*

- Fix migrations for people migrating from <= 1.5.x.
  If you are migrating from 1.6 or 1.7, please rollback django-friendships
  migrations to 0001 and migrate-fake 0002::

    $ ./manage.py migrate friendship 0001
    $ ./manage.py migrate friendship 0002 --fake

  If you're migrating from ``v1.7.x``, you'll likely have to fake ``0003`` as well::

    $ ./manage.py migrate friendship 0003 --fake

Version 1.7.1
-------------

*Released July 5th, 2018*

- Bugfix, missing migration

Version 1.7.0
-------------

*Released July 2nd, 2018*

- Add support for Django 2.0
- Drop support for Django < 1.11

Version 1.6.0
-------------

*Released May 22nd, 2018*

- Added can_request_send option (narnikgamarnik)
- Added blocking feature (Darren Mckeeman)

Version 1.5.0
-------------

*Released August 21st, 2016*

- Added support for Django 1.10

Version 1.4.0
-------------

*Released July 23rd, 2016*

- Moved template tag to assignment_tag to avoid Django 1.9 error

Version 1.3.3
-------------

*Released July 1st, 2016*

- Support non-integer primary keys in cache keys
- Remove support for Django 1.4

Version 1.3.1
-------------

*Released November 11th, 2015*

- Raise AlreadyFriendError if creating request when users are already friends
- PEP8 cleanups

Version 1.3.0
-------------

*Released July 12th, 2015*

- Updated Django 1.7 and 1.8 compatibility
- Signal related bug fixes
- Python 3 compatibility

Version 1.2.0
-------------

*Released September 22nd, 2014*

- Updated test runner for 1.7 compatibility
- Fixed security issue where we were not checking the owner of a FriendRequest during accept and
  cancelation
- Added optional 'message' kwarg to FriendshipManager.add_friend() so it is easier to set the
  optional message field on FriendshipRequests

Version 1.1.0
-------------

*Released May 6th, 2014*

- Added Django 1.7 compatibility.
- Fixed caching issue with sent_requests.
- Added unrejected_requests() and unrejected_request_count() manager methods.

Version 1.0.0
-------------

- Fixed bug where FriendRequests could be left hanging if both sides requested friendship prior to
  one side accepting.  Caused exception if the user accepted the second request.
- Fixed ordering of friendship_request_rejected signal to not fire until DB is updated.
- Fixed Django 1.6 compatibility issue
- 1.0 release whoo hoo!

Changes prior to version 0.9.0
------------------------------

Lots.  We didn't keep good track of issues prior to 1.0.0.
