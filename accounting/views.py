from django.shortcuts import render

from django.http import HttpResponse


def accounting(request):
	return HttpResponse('<h1>Hello World!</h1> <br> <p> by Accounting</p>')