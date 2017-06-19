from django.shortcuts import render
from .models import TreeItemBase, TreeBase
from django.contrib.auth.decorators import login_required

@login_required(login_url="login/")
def home(request):
    if(request.method == "POST"):
        treeItem = TreeItemBase()
        treeItem.parent = TreeItemBase.objects.get(id=request.POST.get("parent", ""))
        treItem.tree = TreeBase.objects.get(id=request.POST.get("tree", ""))
        treeItem.title = request.POST.get("group name", "")
        treeItem.url("/")
        treeItem.save()
        return redirect('home')
    elif(request.method == "GET"):
        return render(request,"home.html")
