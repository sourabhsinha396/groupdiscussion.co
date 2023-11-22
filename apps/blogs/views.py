from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Blog
from .forms import BlogModelForm


def blog_list(request):
    blogs = Blog.objects.filter(is_active=True)
    context = {
        'blogs': blogs,
    }
    return render(request, 'blogs/blog_list.html', context)


def blog_detail(request, slug):
    blog = Blog.objects.get(slug=slug)
    context = {
        'blog': blog,
    }
    return render(request, 'blogs/blog_detail.html', context)


@login_required
def submit_a_blog(request):
    if request.method == "POST":
        form = BlogModelForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('blogs:blog_list')
        else:
            messages.error(request, form.errors)
            context = {'form': form}
            return render(request, 'blogs/submit_a_blog.html', context)
    form = BlogModelForm()
    context = {'form': form}
    return render(request, 'blogs/submit_a_blog.html', context)
            
