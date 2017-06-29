from django.shortcuts import render

# Create your views here.
def dashboard(request, username=None):
	context={'username':username}
	return render(request,'dashboard/dash.html',context)