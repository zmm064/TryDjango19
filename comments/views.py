from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages

from .models import Comment
from .forms import CommentForm

# Create your views here.

def comment_delete(request, id):
    comment = get_object_or_404(Comment, id=id)
    if request.method == "POST":
        parent_url = comment.post.get_absolute_url()
        comment.delete()
        messages.success(request, "This has been deleted")
        return HttpResponseRedirect(parent_url)

    return render(request, "confirm_delete.html", {"object":comment})

def comment_thread(request, id):
    comment = get_object_or_404(Comment, id=id)
    comment_form = CommentForm(request.POST or None)

    if comment_form.is_valid():
        print(comment_form.cleaned_data)
        comment_instance = comment_form.save(commit=False)
        comment_instance.user = request.user
        comment_instance.post = comment.post
        try:
            comment_instance.parent_id = int(request.POST.get("parent_id"))
        except:
            comment_instance.parent_id = None
        comment_instance.save()
        return HttpResponseRedirect(comment_instance.post.get_absolute_url())

    return render(request, 'comment_thread.html', {"comment":comment, "comment_form":comment_form})
