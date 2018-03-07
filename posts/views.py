from urllib.parse import quote_plus

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
# Create your views here.
from comments.models import Comment
from comments.forms import CommentForm
from . models import Post
from . forms import PostForm


def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    if not request.user.is_authenticated():
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    #else:
    #    messages.error(request, "Not Successfully Created")
    return render(request, "post_form.html", {"form": form})

def post_list(request):
    queryset_list = Post.objects.all().filter(draft=False).order_by("-timestamp")

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(title__icontains=query)

    paginator = Paginator(queryset_list, 3)
    page = request.GET.get("page")
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    return render (request, "post_list.html", {"object_list":queryset, "title":"List"})

def post_detail(request, slug=None):
    instance     = get_object_or_404(Post, slug=slug)
    share_string = quote_plus(instance.content)
    comments     = Comment.objects.filter(post=instance, parent=None)
    comment_form = CommentForm(request.POST or None)#, initial={"user":request.user, "post":instance})

    if comment_form.is_valid():
        print(comment_form.cleaned_data)
        comment_instance = comment_form.save(commit=False)
        comment_instance.user = request.user
        comment_instance.post = instance
        try:
            comment_instance.parent_id = int(request.POST.get("parent_id"))
        except:
            comment_instance.parent_id = None
        comment_instance.save()
        return HttpResponseRedirect(comment_instance.post.get_absolute_url())

    return render (request, 
                   "post_detail.html", 
                   {"instance":instance, "title":instance.title, "share_string": share_string, 
                    "comments":comments, "comment_form":comment_form})

def post_update(request, slug=None):
    # 获取实例
    instance = get_object_or_404(Post, slug=slug)
    # 将实例渲染到表单上
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()  # 更新实例对象
        messages.success(request, "更新已保存1")
        #messages.success(request, "更新已保存2")
        #messages.success(request, "更新已保存3")
        return HttpResponseRedirect(instance.get_absolute_url())

    return render (request, 
                   "post_form.html", 
                   {"instance":instance, "title":instance.title, "form":form})

def post_delete(request, slug=None):
    # 直接获取实例对象并将其删除
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "成功删除")
    return redirect("posts:list")