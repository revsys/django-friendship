from django import template

from friendship.models import Friend, Follow, FriendshipRequest

register = template.Library()


@register.inclusion_tag('friendship/templatetags/friends.html')
def friends(user):
    """
    Simple tag to grab all friends
    """
    return {'friends': Friend.objects.friends(user)}


@register.inclusion_tag('friendship/templatetags/followers.html')
def followers(user):
    """
    Simple tag to grab all followers
    """
    return {'followers': Follow.objects.followers(user)}


@register.inclusion_tag('friendship/templatetags/following.html')
def following(user):
    """
    Simple tag to grab all users who follow the given user
    """
    return {'following': Follow.objects.following(user)}


@register.inclusion_tag('friendship/templatetags/friend_requests.html')
def friend_requests(user):
    """
    Inclusion tag to display friend requests
    """
    return {'friend_requests': Friend.objects.requests(user)}


@register.inclusion_tag('friendship/templatetags/friend_request_count.html')
def friend_request_count(user):
    """
    Inclusion tag to display the count of unread friend requests
    """
    return {'friend_request_count': Friend.objects.unread_request_count(user)}


@register.inclusion_tag('friendship/templatetags/friend_count.html')
def friend_count(user):
    """
    Inclusion tag to display the total count of friends for the given user
    """
    return {'friend_count': len(Friend.objects.friends(user))}


@register.inclusion_tag('friendship/templatetags/friend_rejected_count.html')
def friend_rejected_count(user):
    """
    Inclusion tag to display the count of rejected friend requests
    """
    return {'friend_rejected_count': len(Friend.objects.rejected_requests(user))}
