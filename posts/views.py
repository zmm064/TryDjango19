from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
# Create your views here.
from . models import Post
from . forms import PostForm


def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    #else:
    #    messages.error(request, "Not Successfully Created")
    return render(request, "post_form.html", {"form": form})

def post_list(request):
    queryset_list = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(queryset_list, 5)
    page = request.GET.get("page")
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    return render (request, "post_list.html", {"object_list":queryset, "title":"List"})

def post_detail(request, id=None):
    instance = get_object_or_404(Post, id=id)
    return render (request, "post_detail.html", {"instance":instance, "title":instance.title})

def post_update(request, id=None):
    # 获取实例
    instance = get_object_or_404(Post, id=id)
    # 将实例渲染到表单上
    form = PostForm(request.POST or None, instance=instance)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()  # 更新实例对象
        messages.success(request, "更新已保存1")
        messages.success(request, "更新已保存2")
        messages.success(request, "更新已保存3")
        return HttpResponseRedirect(instance.get_absolute_url())

    return render (request, 
                   "post_form.html", 
                   {"instance":instance, "title":instance.title, "form":form})

def post_delete(request, id=None):
    # 直接获取实例对象并将其删除
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, "成功删除")
    return redirect("posts:list")