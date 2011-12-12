from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

from friendship.models import Friend, Follow


def view_friends(request, username, template_name='friendship/friends_list.html'):
    """ View the friends of a user """
    user = get_object_or_404(User, username=username)
    friends = Friend.objects.friends(user)

    return render(request, template_name, {'user': user, 'friends': friends})


@login_required
def add_friend(request, from_username, to_username):
    """ Create a FriendshipRequest """
    pass


@login_required
def accept_friend(request, friendship_request_id):
    """ Accept a friendship request """
    pass


@login_required
def reject_friend(request, friendship_request_id):
    """ Reject a friendship request """
    pass


@login_required
def cancel_friend(request, friendship_request_id):
    """ Cancel a previously created friendship_request_id """
    pass


@login_required
def friendship_request_list(request, username):
    """ View unread and read friendship requests """
    pass


@login_required
def friendship_request_list_rejected(request, user):
    """ View rejected friendship requests """
    pass


@login_required
def friendship_request(request, friendship_request_id):
    """ View a particular friendship request """
    pass


def followers(request, username, template_name='friendship/followers_list.html'):
    """ List this user's followers """
    user = get_object_or_404(User, username=username)
    followers = Follow.objects.followers(user)

    return render(request, template_name, {'user': user, 'followers': followers})


def following(request, username, template_name='friendship/following_list.html'):
    """ List who this user follows """
    user = get_object_or_404(User, username=username)
    following = Follow.objects.following(user)

    return render(request, template_name, {'user': user, 'following': following})


@login_required
def add_follower(request, follower, followee):
    """ Create a following relationship """
    pass


@login_required
def remove_follower(request, follower, followee):
    """ Remove a following relationship """
    pass
