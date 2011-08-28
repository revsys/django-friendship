import datetime
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User 
from django.utils.translation import ugettext_lazy as _

from friendship.signals import friendship_request_created, friendship_request_rejected, friendship_request_canceled, friendship_request_viewed, friendship_request_accepted, friendship_removed, new_follower, new_following, remove_follower, remove_following 

class FriendshipRequest(models.Model):
    """ Model to represent friendship requests """ 
    from_user = models.ForeignKey(User, related_name='friendship_requests_sent')
    to_user = models.ForeignKey(User, related_name='friendship_requests_received')
    is_rejected = models.BooleanField(_('Rejected'), 
            help_text="Receiving user rejected the request", default=False)

    has_viewed = models.BooleanField(_('Viewed'), 
            help_text="Receiving user has viewed the request", default=False)

    message = models.TextField(_('Message'), blank=True) 

    created = models.DateTimeField(default=datetime.datetime.now)
    rejected = models.DateTimeField(blank=True, null=True)
    viewed = models.DateTimeField(blank=True, null=True)


    class Meta:
        verbose_name = _('Friendship Request')
        verbose_name_plural = _('Friendship Requests')

    def save(self, *args, **kwargs):
        if self.is_rejected and not self.rejected:
            self.rejected = datetime.datetime.now()

        if self.has_viewed and not self.viewed: 
            self.viewed = datetime.datetime.now()

        super(FriendshipRequest, self).save(*args, **kwargs)

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
        """ rejcet this friendship request """ 
        self.is_rejected = True 
        friendship_request_rejected.send(sender=self)
        self.save()

    def cancel(self):
        """ cancel this friendship request """ 
        self.delete()
        friendship_request_canceled.send(sender=self)
        return True 

    def mark_viewed(self):
        self.has_viewed = True 
        friendship_request_viewed.send(sender=self)
        self.save() 
        return True 

class FriendshipManager(models.Manager):
    """ Friendship manager """ 

    def friends(self, user):
        """ Return a list of all friends """
        qs = Friend.objects.select_related(depth=1).filter(to_user=user).all()
        return [u.from_user for u in qs]

    def requests(self, user):
        """ Return a list of friendship requests """
        qs = FriendshipRequest.objects.select_related(depth=1).filter(
                to_user=user).all()
        return list(qs) 

    def unread_requests(self, user):
        """ Return a list of unread friendship requests """ 
        qs = FriendshipRequest.objects.select_related(depth=1).filter(
                to_user=user,
                has_viewed=False).all()
        return list(qs) 

    def read_requests(self, user):
        """ Return a list of read friendship requests """ 
        qs = FriendshipRequest.objects.select_related(depth=1).filter(
                to_user=user,
                has_viewed=True).all()
        return list(qs) 

    def rejected_requests(self, user):
        """ Return a list of rejected friendship requests """ 
        qs = FriendshipRequest.objects.select_related(depth=1).filter(
                to_user=user,
                is_rejected=True).all()
        return list(qs) 

    def add_friend(self, from_user, to_user):
        """ Create a friendship request """ 
        request = FriendshipRequest.objects.create(
                    from_user=from_user, 
                    to_user=to_user
                )
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
                return True
            else:
                return False 
        except Friend.DoesNotExist:
            return False 

    def are_friends(self, user1, user2):
        """ Are these two users friends? """ 
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

    def __unicode__(self):
        return "User #%d is friends with #%d" % (self.to_user_id, self.from_user_id)

class FollowingManager(models.Manager):
    """ Following manager """ 

    def followers(self, user):
        """ Return a list of all followers """ 
        qs = Follow.objects.filter(followee=user).all()
        return [u.follower for u in qs]

    def following(self, user): 
        """ Return a list of all users the given user follows """ 
        qs = Follow.objects.filter(follower=user).all()
        return [u.followee for u in qs]

    def add_follower(self, follower, followee):
        """ Create 'follower' follows 'followee' relationship """ 
        relation = Follow.objects.create(follower=follower, followee=followee)
        return relation 

    def remove_follower(self, follower, followee):
        """ Remove 'follower' follows 'followee' relationship """ 
        try:
            rel = Follow.objects.get(follower=follower, followee=followee)
            remove_follower.send(sender=rel, follower=rel.follower)
            remove_following.send(sender=rel, following=rel.followee)
            rel.delete()
            return True
        except Follow.DoesNotExist:
            return False 

    def follows(self, follower, followee):
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

    def __unicode__(self):
        return "User #%d follows #%d" % (self.follwer_id, self.followee_id)

    def save(self, *args, **kwargs):
        super(Follow, self).save(*args, **kwargs)
        new_follower.send(sender=self, follower=self.follower)
        new_following.send(sender=self, follow=self.followee)

