# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration

try:
    from django.contrib.auth import get_user_model
except ImportError: # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()

user_orm_label = '%s.%s' % (User._meta.app_label, User._meta.object_name)
user_model_label = '%s.%s' % (User._meta.app_label, User._meta.module_name)


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'FriendshipRequest'
        db.create_table('friendship_friendshiprequest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='friendship_requests_sent', to=orm[user_orm_label])),
            ('to_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='friendship_requests_received', to=orm[user_orm_label])),
            ('message', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('rejected', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('viewed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('friendship', ['FriendshipRequest'])

        # Adding unique constraint on 'FriendshipRequest', fields ['from_user', 'to_user']
        db.create_unique('friendship_friendshiprequest', ['from_user_id', 'to_user_id'])

        # Adding model 'Friend'
        db.create_table('friendship_friend', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('to_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='friends', to=orm[user_orm_label])),
            ('from_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_unused_friend_relation', to=orm[user_orm_label])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('friendship', ['Friend'])

        # Adding unique constraint on 'Friend', fields ['from_user', 'to_user']
        db.create_unique('friendship_friend', ['from_user_id', 'to_user_id'])

        # Adding model 'Follow'
        db.create_table('friendship_follow', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('follower', self.gf('django.db.models.fields.related.ForeignKey')(related_name='following', to=orm[user_orm_label])),
            ('followee', self.gf('django.db.models.fields.related.ForeignKey')(related_name='followers', to=orm[user_orm_label])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('friendship', ['Follow'])

        # Adding unique constraint on 'Follow', fields ['follower', 'followee']
        db.create_unique('friendship_follow', ['follower_id', 'followee_id'])

    def backwards(self, orm):
        
        # Removing unique constraint on 'Follow', fields ['follower', 'followee']
        db.delete_unique('friendship_follow', ['follower_id', 'followee_id'])

        # Removing unique constraint on 'Friend', fields ['from_user', 'to_user']
        db.delete_unique('friendship_friend', ['from_user_id', 'to_user_id'])

        # Removing unique constraint on 'FriendshipRequest', fields ['from_user', 'to_user']
        db.delete_unique('friendship_friendshiprequest', ['from_user_id', 'to_user_id'])

        # Deleting model 'FriendshipRequest'
        db.delete_table('friendship_friendshiprequest')

        # Deleting model 'Friend'
        db.delete_table('friendship_friend')

        # Deleting model 'Follow'
        db.delete_table('friendship_follow')

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        user_model_label: {
            'Meta': {'object_name': User.__name__, 'db_table': "'%s'" % User._meta.db_table},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'friendship.follow': {
            'Meta': {'unique_together': "(('follower', 'followee'),)", 'object_name': 'Follow'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'followee': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'followers'", 'to': "orm['%s']" % user_orm_label}),
            'follower': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'following'", 'to': "orm['%s']" % user_orm_label}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'friendship.friend': {
            'Meta': {'unique_together': "(('from_user', 'to_user'),)", 'object_name': 'Friend'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'from_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_unused_friend_relation'", 'to': "orm['%s']" % user_orm_label}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'to_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'friends'", 'to': "orm['%s']" % user_orm_label})
        },
        'friendship.friendshiprequest': {
            'Meta': {'unique_together': "(('from_user', 'to_user'),)", 'object_name': 'FriendshipRequest'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'from_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'friendship_requests_sent'", 'to': "orm['%s']" % user_orm_label}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'rejected': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'to_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'friendship_requests_received'", 'to': "orm['%s']" % user_orm_label}),
            'viewed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['friendship']