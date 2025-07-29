from django.urls import reverse
from .models import Comment, Post, User
from django.db.models import Count
from django.shortcuts import get_object_or_404

POSTS_PER_PAGE = 10


class PostsEditMixin:
    model = Post
    template_name = 'blog/create.html'


class CommentEditMixin:
    model = Comment
    pk_url_kwarg = 'pk'
    template_name = 'blog/comment.html'

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.kwargs['post_id']])


class ProfileMixin:

    paginate_by = POSTS_PER_PAGE
    context_object_name = 'posts'
    template_name = 'blog/profile.html'

    def get_profile_user(self):

        return get_object_or_404(User, username=self.kwargs['username'])

    def get_posts_queryset(self, user):
        return user.posts.select_related(
            'category',
            'location'
        ).annotate(comment_count=Count('comment')).order_by('-pub_date')
