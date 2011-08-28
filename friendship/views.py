from django.db import models 
from django.contrib.auth.decorators import login_required 

from friendship.models import Friend, Follow, FriendshipRequest

def view_friends(request, username):
    """ View the friends of a user """ 
    pass 

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

def followers(request, user):
    """ List this user's followers """ 
    pass 

def following(request, user):
    """ List who this user follows """ 
    pass 

@login_required 
def add_follower(request, follower, followee):
    """ Create a following relationship """ 
    pass 

@login_required 
def remove_follower(request, follower, followee):
    """ Remove a following relationship """ 
    pass 

