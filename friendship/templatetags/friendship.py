from django import template
from django.core.cache import cache
from django.contrib.auth.models import User

from friendship.models import FriendshipRequest, Friend, Follow

register = template.Library()

@register.inclusion_tag('friendship/templatetags/friends.html')
def friends(context, user):
    """
    Simple tag to grab all friends 
    """
    context['friends'] = Friend.objects.friends(user)
    return context 

@register.inclusion_tag('friendship/templatetags/followers.html')
def followers(context, user):
    """
    Simple tag to grab all followers
    """
    context['followers'] = Follow.objects.followers(user)
    return context 

@register.inclusion_tag('friendship/templatetags/following.html')
def following(context, user):
    """
    Simple tag to grab all users who follow the given user
    """
    context['following'] = Follow.objects.following(user)
    return context 

@register.inclusion_tag('friendship/templatetags/friend_requests.html')
def friend_requests(context, user):
    """
    Inclusion tag to display friend requests 
    """
    context['friend_requests'] = Friend.objects.requests(user)
    return context 

@register.inclusion_tag('friendship/templatetags/friend_request_count.html')
def friend_request_count(context, user):
    """
    Inclusion tag to display the count of unread friend requests
    """
    context['friend_request_count'] = Friend.objects.unread_request_count(user)
    return context

