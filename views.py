#coding=utf-8
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from haha.books.models import newgroup
from django.contrib.auth import authenticate
from django.contrib import auth
from haha.forms import RegForm,PassForm,FlatPageForm,AddBook,AddUser
from DjangoVerifyCode import Code
from haha.books.models import book
from django.utils.encoding import smart_str
import MySQLdb
import json
import time
import sys
import xlwt
import xlrd
import re
import json
from xlrd import xldate_as_tuple
from haha.forms import uploadform
reload(sys)
sys.setdefaultencoding('utf-8')

def code(request):
	code=Code(request)
	return code.display()

def login(request):
	if request.method=='POST' and "captcha" not in request.REQUEST:
		username=request.POST['username']
		password=request.POST['password']
		user=authenticate(username=username,password=password)
		if user is not None and user.is_active:
			auth.login(request,user)
			request.session['username']=username
			return HttpResponseRedirect('/accounts/profile/')
		else:
			errors="have error"
			return render_to_response('registration/login.html',{'errors':errors})
	if request.method=='POST' and request.POST['captcha']:
		_code=request.POST.get('captcha')
		code=Code(request)
		if code.check(_code):
			username=request.POST['username']
                	password=request.POST['password']
			user=authenticate(username=username,password=password)
			if user is not None and user.is_active:
                        	auth.login(request,user)
                        	request.session['username']=username
                      	  	return HttpResponseRedirect('/accounts/profile/')
			else:
				errors="have error"
				return render_to_response("registration/login.html",{'errors':errors})
		else:
			capterr="验证码错误!"
			return render_to_response("registration/login.html",{'capterr':capterr,"code":code},context_instance=RequestContext(request))
	return render_to_response('registration/login.html')

def logout(request):
	auth.logout(request)
	return render_to_response('registration/logged_out.html')

@login_required(login_url='/accounts/')
def profile(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/accounts/")
	if 'active' in request.POST and 'username' in request.POST:
		active=request.POST.get('active')
		username=request.POST.get('username')
		users=User.objects.get(username=username)
		if active=="1":
			users.is_active=1
		else:
			users.is_active=0
		users.save()
		return HttpResponse("success")
	if 'name' in request.POST and 'page' in request.POST and 'rows' in request.POST:
		page=request.POST.get('page')
		rows=request.POST.get('rows')
		curr_page=(int(page)-1)*int(rows)
		conn=MySQLdb.connect(host='localhost',user='root',passwd='redhat',port=3306,db='haha',charset="utf8")
		cursor=conn.cursor()
		name=request.POST.get('name')
		sql="select username,email,is_active,last_login from auth_user where username like '%"+str(name)+"%' limit "+str(curr_page)+","+str(rows)+";"
		sql2="select username,email,is_active,last_login from auth_user where username like '%"+str(name)+"%';"
		count=cursor.execute(sql2)
		cursor.execute(sql)
		if count%int(rows)==0:
			pages=count/int(rows)
		else:
			pages=count/int(rows)+1
		curr_page=int(page)
		results=[]
		infors=cursor.fetchall()
		for infor in infors:
			if infor[2]==1:
				status="启用"
			else:
				status="禁用"
			results.append({'name':infor[0],'email':infor[1],'status':status,'last_login':infor[3]})
		return render_to_response('registration/user.html',{'results':results,'pages':pages},context_instance=RequestContext(request))
	if 'page' in request.POST and 'rows' in request.POST:
		page=request.POST.get('page')
		rows=request.POST.get('rows')
		curr_page=(int(page)-1)*int(rows)
		sql="select username,email,is_active,last_login from auth_user limit "+str(curr_page)+","+str(rows)+";"
		sql2="select username,email,is_active,last_login from auth_user;"
		conn=MySQLdb.connect(host='localhost',user='root',passwd='redhat',port=3306,db='haha',charset="utf8")
		cursor=conn.cursor()
		count=cursor.execute(sql2)
		cursor.execute(sql)
		if count%int(rows)==0:
			pages=count/int(rows)
		else:
			pages=count/int(rows)+1
		curr_page=int(page)
		results=[]
		infors=cursor.fetchall()
		for infor in infors:
			if infor[2]==1:
				status="启用"
			else:
				status="禁用"
			results.append({'name':infor[0],'email':infor[1],'status':status,'last_login':infor[3]})
		return render_to_response('registration/user.html',{'results':results,"pages":pages},context_instance=RequestContext(request))
	return render_to_response('registration/user.html',context_instance=RequestContext(request))

def reg(request):
	if request.method=='POST':
		form=RegForm(request.POST)
		if form.is_valid():
			username=form.cleaned_data['Username']
			email=form.cleaned_data['email']
			password=form.cleaned_data['Password']
			user=User.objects.create(username=username,email=email)
			user.set_password(password)
			user.save()
			return HttpResponse("用户注册成功！请<a href='/accounts/'>登录</a>")
		
	else:
		form=RegForm()
	return render_to_response('registration/reg.html',{'form':form})


@login_required(login_url="/accounts/")
def password(request):
	username=request.GET['username']
	if request.method=='POST':
		form=PassForm(request.POST)
		if form.is_valid():
			password=form.cleaned_data['orignPass']
			newpass=form.cleaned_data.get('NewPass')
			user=authenticate(username=username,password=password)
			if user is None:
				error="用户密码不正确!"
				code="/code"
				return render_to_response('registration/pass.html',{'form':form,'error':error,'code':code})
			else:
				user.set_password(newpass)
				user.save()	
				message='更改密码成功!请重新登录!'
				return render_to_response('registration/pass.html',{'form':form,'message':message})
	else:
		form=PassForm()
	return render_to_response('registration/pass.html',{'form':form})		



@login_required
def addbook(request):
	if request.method=='POST':
		form=AddBook(request.POST)
		if form.is_valid():
			bookname=form.cleaned_data['bookname']
			author=form.cleaned_data['author']
			price=form.cleaned_data['price']
			importdate=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
			user=request.user
			Book=book.objects.create(name=bookname,author=author,price=price,importdate=importdate,user=user)
			Book.save()
			message="增加图书成功！"
			return render_to_response("registration/addbook.html",{'form':form,'message':message})
	else:
		form=AddBook()
	return render_to_response('registration/addbook.html',{'form':form})




@login_required
def booklist(request):
	if request.method=='POST':
		bookname=request.POST.get('bookname')
		author=request.POST.get('author')
		if len(bookname)>0:
			return render_to_response('registration/booklist.html',{'bookname':bookname})
		if len(author)>0:
			return render_to_response('registration/booklist.html',{'author':author})
	return render_to_response('registration/booklist.html')


@login_required
def test(request):
	page=request.GET.get('page')
	int_page=int(page)
	pages=int_page*3
	if 'bookname' in request.GET:
		bookname=request.GET.get('bookname')
		conn=MySQLdb.connect(host='localhost',user='root',passwd='redhat',port=3306,db='haha')
		cursor=conn.cursor()
		if 'order' in request.GET:
			order=request.GET.get('order')
			if int(order)==1:
				sql="select name,author,price,importdate from books_book where name like '%"+str(bookname)+"%' order by price  limit "+str(pages)+",3;"
			else:
				sql="select name,author,price,importdate from books_book where name like '%"+str(bookname)+"%' order by price desc limit "+str(pages)+",3;"
		else:
			sql="select name,author,price,importdate from books_book where name like '%"+str(bookname)+"%' limit "+str(pages)+",3;"
		sql1="select name,author,price,importdate from books_book where name like '%"+str(bookname)+"%';"
		cursor.execute("set names utf8;")
		cursor.execute(sql)
		infors=cursor.fetchall()
		ress=[]
		for infor in infors:
			ress.append({'bookname':infor[0],'author':infor[1],'price':infor[2],'importdate':infor[3]})
		count=cursor.execute(sql1)
		if count%3==0:
			number_pages=count/3
		else:
			number_pages=count/3+1
		end_pages=number_pages-1
		if int_page==0:
			has_priv=False
		else:
			has_priv=True
		if int_page==end_pages:
			has_next=False
		else:
			has_next=True	
		next_page=int_page+1
		priv_page=int_page-1
		cursor.close()
		conn.close()
		if 'order' in request.GET:
			return render_to_response('registration/test.html',{'ress':ress,'has_next':has_next,'has_priv':has_priv,'end_pages':end_pages,'next_page':next_page,'priv_page':priv_page,'bookname':bookname,'order':request.GET.get('order')})
		return render_to_response('registration/test.html',{'ress':ress,'has_next':has_next,'has_priv':has_priv,'end_pages':end_pages,'next_page':next_page,'priv_page':priv_page,'bookname':bookname})
	if 'author' in request.GET:
		author=request.GET.get('author')
		conn=MySQLdb.connect(host='localhost',user='root',passwd='redhat',port=3306,db='haha')
		cursor=conn.cursor()
		if 'order' in request.GET:
			order=request.GET.get('order')
			if int(order)==1:
				sql="select name,author,price,importdate from books_book where author like '%"+str(author)+"%' order by price limit "+str(pages)+",3;"
			else:
				sql="select name,author,price,importdate from books_book where author like '%"+str(author)+"%' order by price desc limit "+str(pages)+",3;"
		else:
			sql="select name,author,price,importdate from books_book where author like '%"+str(author)+"%' limit "+str(pages)+",3;"
		sql1="select name,author,price,importdate from books_book where author like '%"+str(author)+"%';"
		cursor.execute("set names utf8;")
		cursor.execute(sql)
		infors=cursor.fetchall()
		ress=[]
		for infor in infors:
			ress.append({'bookname':infor[0],'author':infor[1],'price':infor[2],'importdate':infor[3]})
		count=cursor.execute(sql1)
		if count%3==0:
			number_pages=count/3
		else:
			number_pages=count/3+1
		end_pages=number_pages-1
		if int_page==0:
			has_priv=False
		else:
			has_priv=True
		if int_page==end_pages:
			has_next=False
		else:
			has_next=True	
		next_page=int_page+1
		priv_page=int_page-1
		cursor.close()
		conn.close()
		if 'order' in request.GET:
			return render_to_response('registration/test.html',{'ress':ress,'has_next':has_next,'has_priv':has_priv,'end_pages':end_pages,'next_page':next_page,'priv_page':priv_page,'author':author,'order':order})
		return render_to_response('registration/test.html',{'ress':ress,'has_next':has_next,'has_priv':has_priv,'end_pages':end_pages,'next_page':next_page,'priv_page':priv_page,'author':author})
	return render_to_response('registration/test.html',{'ress':ress,'bookname':bookname})



@login_required
def modifybook(request):
	if request.method=='POST':
		bookname=request.POST.get('bookname')
		author=request.POST.get('author')
		return render_to_response('registration/modifybook.html',{'bookname':bookname,'author':author})
	return render_to_response('registration/modifybook.html')	



@login_required
def modify(request):
	page=request.GET.get('page')
	int_page=int(page)
	pages=int_page*3
	if 'bookname' in request.GET and 'author' in request.GET: 
		bookname=request.GET.get('bookname')
		author=request.GET.get('author')
		conn=MySQLdb.connect(host='localhost',user='root',passwd='redhat',port=3306,db='haha')
		cursor=conn.cursor()
		if 'order' in request.GET:
			order=request.GET.get('order')
			if int(order)==1:
				sql="select id,name,author,price,importdate from books_book where name like '%"+str(bookname)+"%' and author like '%"+str(author)+"%' order by price  limit "+str(pages)+",3;"
			else:
				sql="select id,name,author,price,importdate from books_book where name like '%"+str(bookname)+"%' and author like '%"+str(author)+"%' order by price desc limit "+str(pages)+",3;"
		else:
			sql="select id,name,author,price,importdate from books_book where name like '%"+str(bookname)+"%' and author like '%"+str(author)+"%' limit "+str(pages)+",3;"
		sql1="select id,name,author,price,importdate from books_book where name like '%"+str(bookname)+"%' and author like '%"+str(author)+"%';"
		cursor.execute("set names utf8;")
		cursor.execute(sql)
		infors=cursor.fetchall()
		ress=[]
		for infor in infors:
			ress.append({'id':infor[0],'bookname':infor[1],'author':infor[2],'price':infor[3],'importdate':infor[4]})
		count=cursor.execute(sql1)
		if count%3==0:
			number_pages=count/3
		else:
			number_pages=count/3+1
		end_pages=number_pages-1
		if int_page==0:
			has_priv=False
		else:
			has_priv=True
		if int_page==end_pages:
			has_next=False
		else:
			has_next=True	
		next_page=int_page+1
		priv_page=int_page-1
		cursor.close()
		conn.close()
		if 'order' in request.GET:
			return render_to_response('registration/modify.html',{'ress':ress,'has_next':has_next,'has_priv':has_priv,'end_pages':end_pages,'next_page':next_page,'priv_page':priv_page,'bookname':bookname,'author':author,'order':request.GET.get('order')})
		return render_to_response('registration/modify.html',{'ress':ress,'has_next':has_next,'has_priv':has_priv,'end_pages':end_pages,'next_page':next_page,'priv_page':priv_page,'bookname':bookname,'author':author})
	else:
		if 'author' in request.GET:
			author=request.GET.get('author')
			conn=MySQLdb.connect(host='localhost',user='root',passwd='redhat',port=3306,db='haha')
			cursor=conn.cursor()
			if 'order' in request.GET:
				order=request.GET.get('order')
				if int(order)==1:
					sql="select id,name,author,price,importdate from books_book where author like '%"+str(author)+"%' order by price limit "+str(pages)+",3;"
				else:
					sql="select id,name,author,price,importdate from books_book where author like '%"+str(author)+"%' order by price desc limit "+str(pages)+",3;"
			else:
				sql="select id,name,author,price,importdate from books_book where author like '%"+str(author)+"%' limit "+str(pages)+",3;"
			sql1="select id,name,author,price,importdate from books_book where author like '%"+str(author)+"%';"
			cursor.execute("set names utf8;")
			cursor.execute(sql)
			infors=cursor.fetchall()
			ress=[]
			for infor in infors:
				ress.append({'id':infor[0],'bookname':infor[1],'author':infor[2],'price':infor[3],'importdate':infor[4]})
			count=cursor.execute(sql1)
			if count%3==0:
				number_pages=count/3
			else:
				number_pages=count/3+1
			end_pages=number_pages-1
			if int_page==0:
				has_priv=False
			else:
				has_priv=True
			if int_page==end_pages:
				has_next=False
			else:
				has_next=True	
			next_page=int_page+1
			priv_page=int_page-1
			cursor.close()
			conn.close()
			if 'order' in request.GET:
				return render_to_response('registration/modify.html',{'ress':ress,'has_next':has_next,'has_priv':has_priv,'end_pages':end_pages,'next_page':next_page,'priv_page':priv_page,'author':author,'order':order})
			return render_to_response('registration/modify.html',{'ress':ress,'has_next':has_next,'has_priv':has_priv,'end_pages':end_pages,'next_page':next_page,'priv_page':priv_page,'author':author})
		else:
			if 'bookname' in request.GET:
				bookname=request.GET.get('bookname')
				conn=MySQLdb.connect(host='localhost',user='root',passwd='redhat',port=3306,db='haha')
				cursor=conn.cursor()
				if 'order' in request.GET:
					order=request.GET.get('order')
					if int(order)==1:
						sql="select id,name,author,price,importdate from books_book where name like '%"+str(bookname)+"%' order by price limit "+str(pages)+",3;"
					else:
						sql="select id,name,author,price,importdate from books_book where name like '%"+str(bookname)+"%' order by price desc limit "+str(pages)+",3;"
				else:
					sql="select id,name,author,price,importdate from books_book where name like '%"+str(bookname)+"%' limit "+str(pages)+",3;"
				sql1="select id,name,author,price,importdate from books_book where name like '%"+str(bookname)+"%';"
				cursor.execute("set names utf8;")
				cursor.execute(sql)
				infors=cursor.fetchall()
				ress=[]
				for infor in infors:
					ress.append({'id':infor[0],'bookname':infor[1],'author':infor[2],'price':infor[3],'importdate':infor[4]})
				count=cursor.execute(sql1)
				if count%3==0:
					number_pages=count/3
				else:
					number_pages=count/3+1
				end_pages=number_pages-1
				if int_page==0:
					has_priv=False
				else:
					has_priv=True
				if int_page==end_pages:
					has_next=False
				else:
					has_next=True	
				next_page=int_page+1
				priv_page=int_page-1
				cursor.close()
				conn.close()
				if 'order' in request.GET:
					return render_to_response('registration/modify.html',{'ress':ress,'has_next':has_next,'has_priv':has_priv,'end_pages':end_pages,'next_page':next_page,'priv_page':priv_page,'bookname':bookname,'order':order})
				return render_to_response('registration/modify.html',{'ress':ress,'has_next':has_next,'has_priv':has_priv,'end_pages':end_pages,'next_page':next_page,'priv_page':priv_page,'bookname':bookname})
		return render_to_response('registration/modify.html',{'ress':ress,'bookname':bookname})






@login_required
def update(request):
	reload(sys)
	sys.setdefaultencoding('utf-8')
	if request.method=='POST':
		id=request.POST.get('id').strip()
		bookname=request.POST.get('bookname')
		author=request.POST.get('author')
		price=request.POST.get('price')
		conn=MySQLdb.connect(host='localhost',user='root',passwd='redhat',port=3306,db='haha',charset='utf8')
		sql="update books_book set name='%s',author='%s',price=%f where id=%d" %(bookname,author,float(price),int(id))
		cursor=conn.cursor()
		cursor.execute("set names utf8")
		cursor.execute(sql)
		conn.commit()
		cursor.close()
		conn.close()
	return HttpResponse("")	


@login_required
def deletebook(request):
	if request.method=='POST':
		bookname=request.POST.get('bookname')
		author=request.POST.get('author')
		return render_to_response('registration/deletebook.html',{'bookname':bookname,'author':author})
	return render_to_response('registration/deletebook.html')	

@login_required
def delete(request):
	page=request.GET.get('page')
	int_page=int(page)
	pages=int_page*3
	if 'bookname' in request.GET and 'author' in request.GET: 
		bookname=request.GET.get('bookname')
		author=request.GET.get('author')
		conn=MySQLdb.connect(host='localhost',user='root',passwd='redhat',port=3306,db='haha')
		cursor=conn.cursor()
		if 'order' in request.GET:
			order=request.GET.get('order')
			if int(order)==1:
				sql="select id,name,author,price,importdate from books_book where name like '%"+str(bookname)+"%' and author like '%"+str(author)+"%' order by price  limit "+str(pages)+",3;"
		else:
			sql="select id,name,author,price,importdate from books_book where name like '%"+str(bookname)+"%' and author like '%"+str(author)+"%' limit "+str(pages)+",3;"
		sql1="select id,name,author,price,importdate from books_book where name like '%"+str(bookname)+"%' and author like '%"+str(author)+"%';"
		cursor.execute("set names utf8;")
		cursor.execute(sql)
		infors=cursor.fetchall()
		ress=[]
		for infor in infors:
			ress.append({'id':infor[0],'bookname':infor[1],'author':infor[2],'price':infor[3],'importdate':infor[4]})
		count=cursor.execute(sql1)
		if count%3==0:
			number_pages=count/3
		else:
			number_pages=count/3+1
		end_pages=number_pages-1
		if int_page==0:
			has_priv=False
		else:
			has_priv=True
		if int_page==end_pages:
			has_next=False
		else:
			has_next=True	
		next_page=int_page+1
		priv_page=int_page-1
		cursor.close()
		conn.close()
		if 'order' in request.GET:
			return render_to_response('registration/delete.html',{'ress':ress,'has_next':has_next,'has_priv':has_priv,'end_pages':end_pages,'next_page':next_page,'priv_page':priv_page,'bookname':bookname,'author':author,'order':request.GET.get('order')})
		return render_to_response('registration/delete.html',{'ress':ress,'has_next':has_next,'has_priv':has_priv,'end_pages':end_pages,'next_page':next_page,'priv_page':priv_page,'bookname':bookname,'author':author})
	else:
		if 'author' in request.GET:
			author=request.GET.get('author')
			conn=MySQLdb.connect(host='localhost',user='root',passwd='redhat',port=3306,db='haha')
			cursor=conn.cursor()
			if 'order' in request.GET:
				order=request.GET.get('order')
				if int(order)==1:
					sql="select id,name,author,price,importdate from books_book where author like '%"+str(author)+"%' order by price limit "+str(pages)+",3;"
				else:
					sql="select id,name,author,price,importdate from books_book where author like '%"+str(author)+"%' order by price desc limit "+str(pages)+",3;"
			else:
				sql="select id,name,author,price,importdate from books_book where author like '%"+str(author)+"%' limit "+str(pages)+",3;"
			sql1="select id,name,author,price,importdate from books_book where author like '%"+str(author)+"%';"
			cursor.execute("set names utf8;")
			cursor.execute(sql)
			infors=cursor.fetchall()
			ress=[]
			for infor in infors:
				ress.append({'id':infor[0],'bookname':infor[1],'author':infor[2],'price':infor[3],'importdate':infor[4]})
			count=cursor.execute(sql1)
			if count%3==0:
				number_pages=count/3
			else:
				number_pages=count/3+1
			end_pages=number_pages-1
			if int_page==0:
				has_priv=False
			else:
				has_priv=True
			if int_page==end_pages:
				has_next=False
			else:
				has_next=True	
			next_page=int_page+1
			priv_page=int_page-1
			cursor.close()
			conn.close()
			if 'order' in request.GET:
				return render_to_response('registration/delete.html',{'ress':ress,'has_next':has_next,'has_priv':has_priv,'end_pages':end_pages,'next_page':next_page,'priv_page':priv_page,'author':author,'order':order})
			return render_to_response('registration/delete.html',{'ress':ress,'has_next':has_next,'has_priv':has_priv,'end_pages':end_pages,'next_page':next_page,'priv_page':priv_page,'author':author})
		else:
			if 'bookname' in request.GET:
				bookname=request.GET.get('bookname')
				conn=MySQLdb.connect(host='localhost',user='root',passwd='redhat',port=3306,db='haha')
				cursor=conn.cursor()
				if 'order' in request.GET:
					order=request.GET.get('order')
					if int(order)==1:
						sql="select id,name,author,price,importdate from books_book where name like '%"+str(bookname)+"%' order by price limit "+str(pages)+",3;"
					else:
						sql="select id,name,author,price,importdate from books_book where name like '%"+str(bookname)+"%' order by price desc limit "+str(pages)+",3;"
				else:
					sql="select id,name,author,price,importdate from books_book where name like '%"+str(bookname)+"%' limit "+str(pages)+",3;"
				sql1="select id,name,author,price,importdate from books_book where name like '%"+str(bookname)+"%';"
				cursor.execute("set names utf8;")
				cursor.execute(sql)
				infors=cursor.fetchall()
				ress=[]
				for infor in infors:
					ress.append({'id':infor[0],'bookname':infor[1],'author':infor[2],'price':infor[3],'importdate':infor[4]})
				count=cursor.execute(sql1)
				if count%3==0:
					number_pages=count/3
				else:
					number_pages=count/3+1
				end_pages=number_pages-1
				if int_page==0:
					has_priv=False
				else:
					has_priv=True
				if int_page==end_pages:
					has_next=False
				else:
					has_next=True	
				next_page=int_page+1
				priv_page=int_page-1
				cursor.close()
				conn.close()
				if 'order' in request.GET:
					return render_to_response('registration/delete.html',{'ress':ress,'has_next':has_next,'has_priv':has_priv,'end_pages':end_pages,'next_page':next_page,'priv_page':priv_page,'bookname':bookname,'order':order})
				return render_to_response('registration/delete.html',{'ress':ress,'has_next':has_next,'has_priv':has_priv,'end_pages':end_pages,'next_page':next_page,'priv_page':priv_page,'bookname':bookname})
		return render_to_response('registration/delete.html',{'ress':ress,'bookname':bookname})

@login_required
def dels(request):
	reload(sys)
	sys.setdefaultencoding('utf-8')
	if request.method=='POST' and 'id' in request.POST:
		id=request.POST.get('id').strip()
		conn=MySQLdb.connect(host='localhost',user='root',passwd='redhat',port=3306,db='haha',charset='utf8')
		sql="delete from books_book where id=%d" %(int(id))
		cursor=conn.cursor()
		cursor.execute("set names utf8")
		cursor.execute(sql)
		conn.commit()
		cursor.close()
		conn.close()
	if request.method=='POST' and 'ids' in request.POST:
		ids=request.POST.get('ids').strip()
		for id in ids.split(','):
			if len(id)>0:
				conn=MySQLdb.connect(host='localhost',user='root',passwd='redhat',port=3306,db='haha',charset='utf8')
				cursor=conn.cursor()
				sql="delete from books_book where id=%d" %(int(id))
				cursor.execute(sql)
				conn.commit()
		cursor.close()
		conn.close()
	return HttpResponse("")	



@login_required
def excel(request):
	wb=xlwt.Workbook()
	ws=wb.add_sheet('Sheetname',cell_overwrite_ok=True)	
	style_k=xlwt.easyxf('font: bold on,colour_index green,height 360;align: wrap off;borders:left 1,right 1,top 1,bottom 1;pattern: pattern alt_bars, fore_colour gray25, back_colour gray25') 
	fnt=xlwt.Font()
	fnt.name='Arial'
	fnt.colour_index=4
	fnt.bold=True
	
	pattern=xlwt.Pattern()
	pattern.pattern=xlwt.Pattern.SOLID_PATTERN
	pattern.pattern_back_color=0x3A
	pattern.pattern_fore_colour=0x3A
	
	borders=xlwt.Borders()
	borders.left=1
	borders.right=1
	borders.top=1
	borders.bottom=1
	borders.bottom_colour=0x3A

	style=xlwt.XFStyle()
	style.font=fnt
	style.borders=borders
	style.pattern=pattern

	for i in range(2,8):
		ws.col(i).width-0xd00+2000
	
	ws.write(0,0,'Firstname',style)
	ws.write(0,0,'Firstname')
	ws.write_merge(0,1,0,1,'Firstname',style)

	style.num_format_str='YYYY-MM-DD'
	n="HYPERLINK"
	attach_report=xlwt.Formula(n+'("http://www.baidu.com";"frame.pdf")')
	fname='testfile.xls'
	agent=request.META.get('HTTP_USER_AGENT')
	if agent and re.search('MSIE',agent):
		response=HttpResponse(mimetype="application/vnd.ms-excel")
		response['Content-Disposition']='attachment;filename=%s' % urlquote(fname)
	else:
		response=HttpResponse(mimetype="application/ms-excel")
		response['Content-Disposition']='attachment;filename=%s' % smart_str(fname)
	wb.save(response)
	return response

@login_required
def export(request):
	reload(sys)
	sys.setdefaultencoding('utf-8')
	times=time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime(time.time()))
	conn=MySQLdb.connect(host="localhost",user="root",passwd="redhat",port=3306,db='haha',charset="utf8")
	cursor=conn.cursor()
	if request.method=='GET':
		if 'bookname' in request.GET:
			bookname=request.GET.get('bookname')
			sql="select name,author,price,importdate from books_book where name like '%"+str(bookname)+"%';"	
		if 'author' in request.GET:
			author=request.GET.get('author')
			sql="select name,author,price,importdate from books_book where author like '%"+str(author)+"%';"	
	cursor.execute(sql)
	wb=xlwt.Workbook()
	ws=wb.add_sheet(u'图书',cell_overwrite_ok=True)	
	style_k=xlwt.easyxf('font: bold on,colour_index green,height 360;align: wrap off;borders:left 1,right 1,top 1,bottom 1;pattern: pattern alt_bars, fore_colour gray25, back_colour gray25') 
	fnt=xlwt.Font()
	fnt.name='Arial'
	fnt.colour_index=4
	fnt.bold=True
	
	alignment=xlwt.Alignment()
	alignment.horz=xlwt.Alignment.HORZ_CENTER
	alignment.vert=xlwt.Alignment.VERT_CENTER
	
	
	borders=xlwt.Borders()
	borders.left=1
	borders.right=1
	borders.top=1
	borders.bottom=1

	style=xlwt.XFStyle()
	style.font=fnt
	style.borders=borders
	style.alignment=alignment
	style1=xlwt.XFStyle()
	style1.font=fnt
	style1.borders=borders
	style1.alignment=alignment
	

	for i in range(2,8):
		ws.col(i).width-0xd00+2000
	
	ws.write(0,0,u'图书名称',style)
	ws.write(0,0,u'图书名称')
	ws.write_merge(0,1,0,1,u'图书名称',style)

	ws.write(0,2,u'作者',style)
	ws.write(0,2,u'作者')
	ws.write_merge(0,1,2,3,u'作者',style)

	ws.write(0,3,u'价格(￥)',style)
	ws.write(0,3,u'价格(￥)')
	ws.write_merge(0,1,4,5,u'价格(￥)',style)

	ws.write(0,6,u'入库日期',style)
	ws.write(0,6,u'入库日期')
	ws.write_merge(0,1,6,7,u'入库日期',style)

	style.num_format_str='YYYY-MM-DD h:mm'
	n="HYPERLINK"
	infors=cursor.fetchall()
	i=2
	for infor in infors:
		ws.write(i,0,infor[0],style)
		ws.write(i,0,infor[0])
		ws.write_merge(i,i,0,1,infor[0],style)

		ws.write(i,2,infor[1],style)
		ws.write(i,2,infor[1])
		ws.write_merge(i,i,2,3,infor[1],style)

		ws.write(i,4,infor[2],style1)
		ws.write(i,4,infor[2])
		ws.write_merge(i,i,4,5,infor[2],style1)

		ws.write(i,6,infor[3],style)
		ws.write(i,6,infor[3])
		ws.write_merge(i,i,6,7,infor[3],style)
		i=i+1
		

	fname='export%s.xls' % times
	agent=request.META.get('HTTP_USER_AGENT')
	if agent and re.search('MSIE',agent):
		response=HttpResponse(mimetype="application/vnd.ms-excel")
		response['Content-Disposition']='attachment;filename=%s' % urlquote(fname)
	else:
		response=HttpResponse(mimetype="application/ms-excel")
		response['Content-Disposition']='attachment;filename=%s' % smart_str(fname)
	wb.save(response)
	return response






@login_required
def upload(f):
	filename=f.name
	destination=open("upload/%s" % filename,'wb+')
	for chunk in f.chunks():
		destination.write(chunk)
	destination.close()


@login_required
def open_excel(file):
	try:
		data=xlrd.open_workbook(file)
		return data
	except Exception,e:
		print str(e)


@login_required
def batchs(request):
	files=open('/home/haha/haha/upload/readme.txt',"rb")
	chars=files.readlines()
	help_content=" ".join(chars)
	if request.method=='POST':
			form=uploadform(request.POST,request.FILES)
			if form.is_valid():
				times=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
				user=request.user.id
				f=request.FILES['files']
				if f.name.split('.')[1]=='txt':
					message=''
					upload(f)
					openf=open('upload/%s' % f.name,'rb')
					chars=openf.readlines()
					for char in chars:
						results=[]
						bookname=char.split(',')[0].strip()
						author=char.split(',')[1].strip()
						price=char.split(',')[2].split('\n')[0].strip()
						try:
							Book=book.objects.get(name=bookname)
						except book.DoesNotExist:
							if len(bookname)>0 and len(author)>0 and len(price)>0:
								Book=book.objects.create(name=bookname,author=author,price=price,importdate=times,user=user)
								Book.save()
							else:
								message="数据格式不正确!"
						else:
							message="图书:%s已经录入过!" % bookname
					openf.close()
						
				else:
					if f.name.split('.')[1]=='xls':
						message="excel file upload"
						upload(f)
						data=open_excel('upload/%s' % f.name)
						table=data.sheet_by_index(0)
						nrows=table.nrows
						ncols=table.ncols
						title=table.row_values(0)
						for rownum in range(2,nrows):
							record=[]
							row=table.row_values(rownum)
							for i in range(ncols):
								record.append(row[i])
							try:
								Book=book.objects.get(name=record[0])
							except book.DoesNotExist:
								Book=book.objects.create(name=record[0],author=record[2],price=record[4],importdate=times,user=user)
								Book.save()
							else:
								message="图书:%s 已经录入过！" % record[0]
					else:
						message='not supper this file'
				if message=='':
					message='图书录入成功!'
				return render_to_response('registration/batch.html',{'form':form,'message':message})
	else:
		form=uploadform()
	return render_to_response('registration/batch.html',{'form':form,'help_content':help_content})






@login_required
def wocao(request):
	conn=MySQLdb.connect(host='localhost',user='root',passwd='redhat',port=3306,db='haha',charset='utf8')
	cursor=conn.cursor()
	if request.method=='POST':
		name=request.POST.get('name')
		sql="insert into message(message)values(%s)"
		cursor.execute(sql,name)
	conn.commit()
	cursor.close()
	conn.close()
		
	return HttpResponse("...............................")




@login_required
def ttt(request):
	if request.method=='POST':
		a=request.POST.get('a')
		b=request.POST.get('b')
		return HttpResponse(int(a)+int(b))
	return HttpResponse("...............")


@login_required
def auths(request):
	if request.method=='POST':
		username=request.user.username
		password=request.POST.get('passwd')
		newpass=request.POST.get('newpass')
		user=authenticate(username=username,password=password)
		if user is not None:
			users=User.objects.get(username=username)
			users.set_password(newpass)
			users.save()
			return HttpResponse(1)
		else:
			return HttpResponse(0)
	return HttpResponse("........................")
		



@login_required
def dropuser(request):
	if request.method=='POST':
		username=request.POST.get('user')
		if username=="admin":
			return HttpResponse("failed")
		user=User.objects.get(username=username)
		user.delete()
		return HttpResponse("success")
	return HttpResponse("................")




@login_required
def adduser(request):
	if request.method=='POST':
		username=request.POST.get('username')
		email=request.POST.get('email')
		password=request.POST.get('password')
		users=User.objects.filter(username=username)
		if len(users)>0:
			return HttpResponse(1)
		users=User.objects.filter(email=email)
		if len(users):
			return HttpResponse(2)	

		users=User.objects.create(username=username,email=email)
		users.set_password(password)
		users.save()
		return HttpResponse(4)
	return HttpResponse(".......................")




@login_required
def edituser(request):
	if request.method=='POST':
		if 'username' in  request.POST and 'email' in request.POST:
		 	username=request.POST.get('username')	
			email=request.POST.get('email')
			users=User.objects.exclude(username=username)
			user=users.filter(email=email)
			if len(user)>0:
				return HttpResponse(2)                          #该邮箱已经被使用
			else:
				users=User.objects.get(username=username)
				users.email=email
				users.save()
				return HttpResponse(1)				#更新邮箱地址成功
		if 'username' in request.POST and 'password' in request.POST:
			username=request.POST.get('username')
			password=request.POST.get('password')
			users=User.objects.get(username=username)
			users.set_password(password)
			users.save()
			return HttpResponse(3)					#更新密码成功
	return HttpResponse("........................")

@login_required
def statusquery(request):
	if 'name' in request.POST:
		name=request.POST.get('name')
	sql="select username,email,is_active,last_login from auth_user"
        conn=MySQLdb.connect(host='localhost',user='root',passwd='redhat',port=3306,db='haha',charset="utf8")
        cursor=conn.cursor()
        cursor.execute(sql)
        results=[]
        infors=cursor.fetchall()
        for infor in infors:
                if infor[2]==1:
                        status="启用"
                else:
                        status="禁用"
                results.append({'name':infor[0],'email':infor[1],'status':status,'last_login':infor[3]})	
	return HttpResponse(results)

@login_required
def query():
	conn=MySQLdb.connect(host='localhost',user='root',passwd='redhat',port=3306,db='haha',charset='utf8')
	cursor=conn.cursor()
	sql="select name,description,updatetime from auth_group a inner join books_newgroup b on a.id=b.group_id;"
	cursor.execute(sql)
	infors=cursor.fetchall()
	results=[]
	for infor in infors:
		result={}
		result["name"]=infor[0]
		group=Group.objects.get(name=infor[0])
		userlist=group.user_set.all()
		users=''
		for user in userlist:
                    users=users+user.username+","
		result["description"]=infor[1]
		result["updatetime"]=str(infor[2])
		result['userlist']=users
		results.append(json.dumps(result))
	return results
		

@login_required
def addrole(request):
	if 'rolename' in request.POST and 'roledesc' in request.POST and 'action' in request.POST:
		times=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		rolename=request.POST.get('rolename')
		action=request.POST.get('action')
		roledesc=request.POST.get('roledesc')
		if action=='1':
			group=Group.objects.filter(name=rolename)
			if len(group)>0:
				return HttpResponse(4)                                                    #角色已经存在，然后4
			groups=newgroup.objects.create(name=rolename,description=roledesc,updatetime=times)
			groups.save()
			data=query()
			return HttpResponse(json.dumps(data))

		if action=='2':
			newrole=request.POST.get('newrolename')
			if len(newrole)>0:
				group=Group.objects.filter(name=newrole)
				if len(group)>0:
					return HttpResponse(4)
				else:
					groups=newgroup.objects.get(name=rolename)
					groups.name=newrole
					groups.description=roledesc
					groups.save()
			else:
				groups=newgroup.objects.get(name=rolename)
				groups.description=roledesc
				groups.save()
			data=query()
			return HttpResponse(json.dumps(data))
	if 'rolename' in request.POST and 'action' in request.POST:
		rolename=request.POST.get('rolename')
		action=request.POST.get('action')
		if action=='3':
			groups=newgroup.objects.get(name=rolename)
			groups.delete()
			data=query()
			return HttpResponse(json.dumps(data))
					
	data=query()
	return HttpResponse(json.dumps(data))

	
@login_required
def grouplist(request):
	group=Group.objects.all()
	results=[]
	for i in group:
		result={}
		result['id']=i.id
		result['name']=i.name
		results.append(json.dumps(result))
	return HttpResponse(json.dumps(results))


@login_required
def usergroup(request):
	if request.method=='POST':
		username=request.POST.get('username')
		user=User.objects.get(username=username)
		group=user.groups.get_query_set()
		results=[]
		for i in group:
			result={}
			result['id']=i.id
			results.append(json.dumps(result))
		return HttpResponse(json.dumps(results))
	return HttpResponse("....................")



@login_required
def groupmod(request):
	if request.method=='POST':
		grouplist=request.POST.get('grouplist')
		removelist=request.POST.get('removelist')
		username=request.POST.get('username')
		user=User.objects.get(username=username)
		if len(grouplist):
			for i in grouplist.split('*'):
				if len(i):
					group=Group.objects.get(id=i)
					user.groups.add(group)
		if len(removelist):
			for i in removelist.split('*'):
				if len(i):
					group=Group.objects.get(id=i)
					user.groups.remove(group)
			
		return HttpResponse("success")
	return HttpResponse("...................")


@login_required
def permlist(request):
	results=[]
	content=ContentType.objects.get_for_model(book)
	permissions=Permission.objects.filter(content_type=content)
	for permission in permissions:
		result={}
		result['name']=permission.name
		result['codename']=permission.codename
		result['content']=u'book'
		results.append(json.dumps(result))
	return HttpResponse(json.dumps(results))


@login_required
def addperm(request):
	permname=request.POST.get('permname')
	content=request.POST.get('content')
	permission=Permission.objects.filter(name=permname)
	if len(permission)>0:
		return HttpResponse("4")                     #返回权限名称已经存在的错误码 
	permission=Permission.objects.filter(codename=content)
	if len(permission)>0:
		return HttpResponse("5")                     #返回权限内容已经存在的错误码 
	contentype=ContentType.objects.get_for_model(book)
	permission=Permission.objects.create(codename=content,name=permname,content_type=contentype)
	permission.save()
	data=permlist(request)
	return HttpResponse(data)


@login_required
def assignrole(request):
	rolename=request.POST.get('rolename')
	perm=request.POST.get('perm')
	removelist=request.POST.get('removelist')
	group=Group.objects.get(name=rolename)
	if len(perm)>0:
		for i in perm.split('*'):
			if len(i):
				permission=Permission.objects.get(codename=i)
				group.permissions.add(permission)
	if len(removelist)>0:
		for i in removelist.split('*'):
			if len(i):
				permission=Permission.objects.get(codename=i)
				group.permissions.remove(permission)
	return HttpResponse("success")


@login_required
def getassign(request):                                  #获取权限列表
	rolename=request.POST.get('rolename')
	group=Group.objects.get(name=rolename)
	permissionlist=group.permissions.get_query_set()
	results=[]
	for permission in permissionlist:
		result={}
		result['name']=permission.name
		result['codename']=permission.codename
		results.append(json.dumps(result))
	return HttpResponse(json.dumps(results))
			
