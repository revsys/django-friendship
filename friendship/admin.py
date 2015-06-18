from __future__ import absolute_import

from django.contrib import admin

from .models import Follow, Friend, FriendshipRequest


class FollowAdmin(admin.ModelAdmin):
    model = Follow
    fields = ('follower', 'followee','created')


class FriendAdmin(admin.ModelAdmin):
    model = Friend
    fields = ('to_user', 'from_user','created')


class FriendshipRequestAdmin(admin.ModelAdmin):
    model = FriendshipRequest
    fields = ('from_user', 'to_user','message','created','rejected','viewed')


admin.site.register(Follow, FollowAdmin)
admin.site.register(Friend, FriendAdmin)
admin.site.register(FriendshipRequest, FriendshipRequestAdmin)
