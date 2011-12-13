from django.conf.urls.defaults import url, patterns
from friendship.views import view_friends, add_friend, accept_friend, \
        reject_friend, cancel_friend, friendship_request_list, \
        friendship_request_list_rejected, friendship_request, followers,\
        following, add_follower, remove_follower, all_users

urlpatterns = patterns('',
    url(
        regex=r'^users/$',
        view=all_users,
        name='friendship_view_users',
    ),
    url(
        regex=r'^friends/(?P<username>[\w-]+)/$',
        view=view_friends,
        name='friendship_view_friends',
    ),
    url(
        regex=r'^friend/add/(?P<from_username>[\w-]+)/(?P<to_username>[\w-]+)/$',
        view=add_friend,
        name='friendship_add_friend',
    ),
    url(
        regex=r'^friend/accept/(?P<friendship_request_id>\d+)/$',
        view=accept_friend,
        name='friendship_accept',
    ),
    url(
        regex=r'^friend/reject/(?P<friendship_request_id>\d+)/$',
        view=reject_friend,
        name='friendship_reject',
    ),
    url(
        regex=r'^friend/cancel/(?P<friendship_request_id>\d+)/$',
        view=cancel_friend,
        name='friendship_cancel',
    ),
    url(
        regex=r'^friend/requests/(?P<username>[\w-]+)/$',
        view=friendship_request_list,
        name='friendship_requests',
    ),
    url(
        regex=r'^friend/requests/(?P<username>[\w-]+)/rejected/$',
        view=friendship_request_list_rejected,
        name='friendship_requests_rejected',
    ),
    url(
        regex=r'^friend/request/(?P<friendship_request_id>\d+)/$',
        view=friendship_request,
        name='friendship_request_detail',
    ),
    url(
        regex=r'^followers/(?P<username>[\w-]+)/$',
        view=followers,
        name='friendship_followers',
    ),
    url(
        regex=r'^following/(?P<username>[\w-]+)/$',
        view=following,
        name='friendship_following',
    ),
    url(
        regex=r'^follower/add/(?P<from_username>[\w-]+)/(?P<to_username>[\w-]+)/$',
        view=add_follower,
        name='friendship_add_follower',
    ),
    url(
        regex=r'^follower/remove/(?P<from_username>[\w-]+)/(?P<to_username>[\w-]+)/$',
        view=remove_follower,
        name='friendship_remove_follower',
    ),
)
