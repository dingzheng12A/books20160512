#coding=utf-8
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.db.models.signals import post_save
class NewsAdmin(admin.ModelAdmin):


	class Media:
		js=('/js/tinymce/tinymce.min.js','/js/textareas.js')


class book(models.Model):
	name=models.CharField(max_length=50)
	author=models.CharField(max_length=20)
	price=models.FloatField()
	importdate=models.DateTimeField()
	user=models.CharField(max_length=20)


class logtype(models.Model):
	logtype=models.CharField(max_length=50)
	
class log(models.Model):
	user=models.CharField(max_length=50)
	type=models.ForeignKey(logtype,related_name='book_log')
	date=models.DateTimeField(auto_now_add=True)
	message=models.CharField(max_length=100)

#admin.site.register(NewsAdmin)
# Create your models here.


class newgroup(Group):
	group=models.OneToOneField(Group)
	description=models.TextField(max_length=512)
	updatetime=models.DateTimeField(auto_now=True)

