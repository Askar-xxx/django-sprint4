from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, Http404
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.contrib.auth.views import PasswordChangeView
from django.core.exceptions import PermissionDenied
from .forms import (
    CommentCreateForm,
    PostForm,
    EditUserFormTester,
)
from .models import Category, Comment, Post, User
from .mixins import CommentEditMixin, PostsEditMixin, ProfileMixin
from .utils import filter_published_posts

POSTS_PER_PAGE = 10


class ProfileView(ProfileMixin, ListView):

    def get_queryset(self):
        self.profile_user = self.get_profile_user()
        queryset = self.get_posts_queryset(self.profile_user)

        if self.request.user != self.profile_user:
            queryset = filter_published_posts(queryset)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'profile': self.profile_user,
            'is_owner': self.request.user == self.profile_user
        })
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EditUserFormTester
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class ProfilePasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'registration/password_change_form.html'

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class PostDisplayView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        if not post.is_published and self.request.user != post.author:
            raise Http404
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form': CommentCreateForm(),
            'comments': self.object.comments.select_related('author')
        })
        return context


class PostRemovalView(PostsEditMixin, LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')
    pk_url_kwarg = 'post_id'

    def check_permissions(self, request, *args, **kwargs):
        obj = get_object_or_404(Post, pk=self.kwargs[self.pk_url_kwarg])
        if request.user != obj.author:
            raise PermissionDenied
        return True

    def dispatch(self, request, *args, **kwargs):
        self.check_permissions(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)


class PostEditView(PostsEditMixin, LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    pk_url_kwarg = 'post_id'

    def check_permissions(self, request, *args, **kwargs):
        obj = get_object_or_404(Post, pk=self.kwargs[self.pk_url_kwarg])
        if request.user != obj.author:
            return False
        return True

    def dispatch(self, request, *args, **kwargs):
        if not self.check_permissions(request, *args, **kwargs):
            return redirect('blog:post_detail', post_id=self.kwargs[
                self.pk_url_kwarg])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.object.pk})


class NewPostView(PostsEditMixin, LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.user = request.user

    def form_valid(self, form):
        form.instance.author = self.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile', args=[self.user.username])


class AddCommentView(CommentEditMixin, LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentCreateForm

    def prepare_comment(self, form):
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.author = self.request.user
        return form

    def form_valid(self, form):
        form = self.prepare_comment(form)
        return super().form_valid(form)


class RemoveCommentView(CommentEditMixin, LoginRequiredMixin, DeleteView):
    model = Comment
    pk_url_kwarg = 'pk'

    def check_permissions(self, request, *args, **kwargs):
        obj = get_object_or_404(Comment, pk=self.kwargs['pk'])
        if request.user != obj.author:
            raise PermissionDenied
        return True

    def dispatch(self, request, *args, **kwargs):
        try:
            self.check_permissions(request, *args, **kwargs)
        except PermissionDenied:
            return redirect('blog:post_detail', post_id=self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)


class EditCommentView(CommentEditMixin, LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentCreateForm
    pk_url_kwarg = 'pk'

    def check_permissions(self, request, *args, **kwargs):
        obj = get_object_or_404(Comment, pk=self.kwargs['pk'])
        if request.user != obj.author:
            raise PermissionDenied
        return True

    def dispatch(self, request, *args, **kwargs):
        try:
            self.check_permissions(request, *args, **kwargs)
        except PermissionDenied:
            return redirect('blog:post_detail', post_id=self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)


class UserPostsView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    paginate_by = POSTS_PER_PAGE

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        posts = user.posts.all()
        if self.request.user != user:
            posts = filter_published_posts(posts)
        return posts

    def prepare_context(self, context):
        context['profile'] = get_object_or_404(
            User, username=self.kwargs['username']
        )
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not isinstance(context, dict):
            context = {}

        profile_user = get_object_or_404(
            User, username=self.kwargs['username'])
        context['profile'] = profile_user
        return context


class HomePageView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = POSTS_PER_PAGE
    queryset = filter_published_posts(Post.objects.all())


class CategoryPostsView(ListView):
    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'post_list'
    paginate_by = POSTS_PER_PAGE

    def get_queryset(self):
        category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return filter_published_posts(
            Post.objects.filter(category=category)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return context
