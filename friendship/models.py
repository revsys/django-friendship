import datetime

from django.db import models
from django.db.models import Q
from django.core.cache import cache
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from friendship.signals import friendship_request_created, \
        friendship_request_rejected, friendship_request_canceled, \
        friendship_request_viewed, friendship_request_accepted, \
        friendship_removed, follower_created, following_created, follower_removed,\
        following_removed


CACHE_TYPES = {
    'friends': 'f-%d',
    'followers': 'fo-%d',
    'following': 'fl-%d',
    'requests': 'fr-%d',
    'unread_requests': 'fru-%d',
    'unread_request_count': 'fruc-%d',
    'read_requests': 'frr-%d',
    'rejected_requests': 'frj-%d',
}

BUST_CACHES = {
    'friends': ['friends'],
    'followers': ['followers'],
    'following': ['following'],
    'requests': [
        'requests',
        'unread_requests',
        'unread_request_count',
        'read_requests',
        'rejected_requests',
        ],
}


def cache_key(type, user_pk):
    """
    Build the cache key for a particular type of cached value
    """
    return CACHE_TYPES[type] % user_pk


def bust_cache(type, user_pk):
    """
    Bust our cache for a given type, can bust multiple caches
    """
    bust_keys = BUST_CACHES[type]
    keys = [CACHE_TYPES[k] % user_pk for k in bust_keys]
    cache.delete_many(keys)


class FriendshipRequest(models.Model):
    """ Model to represent friendship requests """
    from_user = models.ForeignKey(User, related_name='friendship_requests_sent')
    to_user = models.ForeignKey(User, related_name='friendship_requests_received')

    message = models.TextField(_('Message'), blank=True)

    created = models.DateTimeField(default=datetime.datetime.now)
    rejected = models.DateTimeField(blank=True, null=True)
    viewed = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = _('Friendship Request')
        verbose_name_plural = _('Friendship Requests')
        unique_together = ('from_user', 'to_user')

    def __unicode__(self):
        return "User #%d friendship requested #%d" % (self.from_user_id, self.to_user_id)

    def accept(self):
        """ Accept this friendship request """
        relation1 = Friend.objects.create(
                        from_user=self.from_user,
                        to_user=self.to_user
                    )
        relation2 = Friend.objects.create(
                        from_user=self.to_user,
                        to_user=self.from_user
                    )
        friendship_request_accepted.send(
                sender=self,
                from_user=self.from_user,
                to_user=self.to_user
            )

        self.delete()
        return True

    def reject(self):
        """ reject this friendship request """
        self.rejected = datetime.datetime.now()
        friendship_request_rejected.send(sender=self)
        self.save()

    def cancel(self):
        """ cancel this friendship request """
        self.delete()
        friendship_request_canceled.send(sender=self)
        return True

    def mark_viewed(self):
        self.viewed = datetime.datetime.now()
        friendship_request_viewed.send(sender=self)
        self.save()
        return True


class FriendshipManager(models.Manager):
    """ Friendship manager """

    def friends(self, user):
        """ Return a list of all friends """
        key = cache_key('friends', user.pk)
        friends = cache.get(key)

        if not friends:
            qs = Friend.objects.select_related(depth=1).filter(to_user=user).all()
            friends = [u.from_user for u in qs]
            cache.set(key, friends)

        return friends

    def requests(self, user):
        """ Return a list of friendship requests """
        key = cache_key('requests', user.pk)
        requests = cache.get(key)

        if not requests:
            qs = FriendshipRequest.objects.select_related(depth=1).filter(
                    to_user=user).all()
            requests = list(qs)
            cache.set(key, requests)

        return requests

    def unread_requests(self, user):
        """ Return a list of unread friendship requests """
        key = cache_key('unread_requests', user.pk)
        unread_requests = cache.get(key)

        if not unread_requests:
            qs = FriendshipRequest.objects.select_related(depth=1).filter(
                    to_user=user,
                    viewed__isnull=True).all()
            unread_requests = list(qs)
            cache.set(key, unread_requests)

        return unread_requests

    def unread_request_count(self, user):
        """ Return a count of unread friendship requests """
        key = cache_key('unread_request_count', user.pk)
        count = cache.get(key)

        if not count:
            count = FriendshipRequest.objects.select_related(depth=1).filter(
                    to_user=user,
                    viewed__isnull=True).count()
            cache.set(key, count)

        return count

    def read_requests(self, user):
        """ Return a list of read friendship requests """
        key = cache_key('read_requests', user.pk)
        read_requests = cache.get(key)

        if not read_requests:
            qs = FriendshipRequest.objects.select_related(depth=1).filter(
                    to_user=user,
                    viewed__isnull=False).all()
            read_requests = list(qs)
            cache.set(key, read_requests)

        return read_requests

    def rejected_requests(self, user):
        """ Return a list of rejected friendship requests """
        key = cache_key('rejected_requests', user.pk)
        rejected_requests = cache.get(key)

        if not rejected_requests:
            qs = FriendshipRequest.objects.select_related(depth=1).filter(
                    to_user=user,
                    rejected__isnull=False).all()
            rejected_requests = list(qs)
            cache.set(key, rejected_requests)

        return rejected_requests

    def add_friend(self, from_user, to_user):
        """ Create a friendship request """
        request = FriendshipRequest.objects.create(
                    from_user=from_user,
                    to_user=to_user
                )
        bust_cache('requests', to_user.pk)
        friendship_request_created.send(sender=self)

        return request

    def remove_friend(self, to_user, from_user):
        """ Destroy a friendship relationship """
        try:
            qs = Friend.objects.filter(
                        Q(to_user=to_user, from_user=from_user) |
                        Q(to_user=from_user, from_user=to_user)
                    ).distinct().all()
            if qs:
                friendship_removed.send(
                        sender=qs[0],
                        from_user=from_user,
                        to_user=to_user
                    )
                qs.delete()
                bust_cache('friends', to_user.pk)
                bust_cache('friends', from_user.pk)
                return True
            else:
                return False
        except Friend.DoesNotExist:
            return False

    def are_friends(self, user1, user2):
        """ Are these two users friends? """
        friends1 = cache.get(cache_key('friends', user1.pk))
        friends2 = cache.get(cache_key('friends', user2.pk))
        if friends1 and user2 in friends1:
            return True
        elif friends2 and user1 in friends2:
            return True
        else:
            try:
                Friend.objects.get(to_user=user1, from_user=user2)
                return True
            except Friend.DoesNotExist:
                return False


class Friend(models.Model):
    """ Model to represent Friendships """
    to_user = models.ForeignKey(User, related_name='friends')
    from_user = models.ForeignKey(User, related_name='_unused_friend_relation')
    created = models.DateTimeField(default=datetime.datetime.now)

    objects = FriendshipManager()

    class Meta:
        verbose_name = _('Friend')
        verbose_name_plural = _('Friends')
        unique_together = ('from_user', 'to_user')

    def __unicode__(self):
        return "User #%d is friends with #%d" % (self.to_user_id, self.from_user_id)


class FollowingManager(models.Manager):
    """ Following manager """

    def followers(self, user):
        """ Return a list of all followers """
        key = cache_key('followers', user.pk)
        followers = cache.get(key)

        if not followers:
            qs = Follow.objects.filter(followee=user).all()
            followers = [u.follower for u in qs]
            cache.set(key, followers)

        return followers

    def following(self, user):
        """ Return a list of all users the given user follows """
        key = cache_key('following', user.pk)
        following = cache.get(key)

        if not following:
            qs = Follow.objects.filter(follower=user).all()
            following = [u.followee for u in qs]
            cache.set(key, following)

        return following

    def add_follower(self, follower, followee):
        """ Create 'follower' follows 'followee' relationship """
        relation = Follow.objects.create(follower=follower, followee=followee)

        follower_created.send(sender=self, follower=follower)
        following_created.send(sender=self, follow=followee)

        bust_cache('followers', followee.pk)
        bust_cache('following', follower.pk)

        return relation

    def remove_follower(self, follower, followee):
        """ Remove 'follower' follows 'followee' relationship """
        try:
            rel = Follow.objects.get(follower=follower, followee=followee)
            follower_removed.send(sender=rel, follower=rel.follower)
            following_removed.send(sender=rel, following=rel.followee)
            rel.delete()
            bust_cache('followers', followee.pk)
            bust_cache('following', follower.pk)
            return True
        except Follow.DoesNotExist:
            return False

    def follows(self, follower, followee):
        """ Does follower follow followee? Smartly uses caches if exists """
        followers = cache.get(cache_key('following', follower.pk))
        following = cache.get(cache_key('followers', followee.pk))

        if followers and followee in followers:
            return True
        elif following and follower in following:
            return True
        else:
            try:
                Follow.objects.get(follower=follower, followee=followee)
                return True
            except Follow.DoesNotExist:
                return False


class Follow(models.Model):
    """ Model to represent Following relationships """
    follower = models.ForeignKey(User, related_name='following')
    followee = models.ForeignKey(User, related_name='followers')
    created = models.DateTimeField(default=datetime.datetime.now)

    objects = FollowingManager()

    class Meta:
        verbose_name = _('Following Relationship')
        verbose_name_plural = _('Following Relationships')
        unique_together = ('follower', 'followee')

    def __unicode__(self):
        return "User #%d follows #%d" % (self.follower_id, self.followee_id)
