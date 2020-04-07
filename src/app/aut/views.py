#-*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response,get_object_or_404, redirect

#para el sistema de login importamos lo siguiente
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


def login_view(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		login(request, user)
		return redirect('/')
	else:
		#context = {'errors':True}
		#return render(request, 'index.html' , context)
		return redirect('/')


@login_required(login_url='/')
def logout_view(request):
	logout(request)
	return redirect('/')
