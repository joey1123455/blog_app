from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from django.core.mail import send_mail
from django.views.decorators.http import require_POST

from .models import *
from . forms import *

# Create your views here.
def post_list(request):
    post_list = Post.published.all()
    print(post_list)
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page')

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog\post\list.html', {'posts': posts})


class PostLists(ListView):
    #Alternative list view using class inheritance
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog\post\list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post, 
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    comments = post.comments.filter(active=True)
    form = CommentForm()
    context = {'form': form, 'post': post, 'comments': comments}
    return render(request, 'blog\post\detail.html', context)


def post_share(request, post_id):
    #Retrieve post by id
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED,
        )
    sent = False

    form = EmailPostForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f'{cd["name"]} recommends you read {post.title}'
            message = f'Read {post.title} at {post_url}\n\n {cd["comments"]}'

            send_mail(subject, message, 'folayanjoey@gmail.com', [cd['to']])
            sent = True
        else:
            form = EmailPostForm()

    return render(request, 'blog\post\share.html', {'post': post, 
                                                    'form': form, 
                                                    'sent': sent}
                                                    )


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    context = {'form': form, 'post': post, 'comment': comment}
    return render(request, 'blog\post\comment.html', context)