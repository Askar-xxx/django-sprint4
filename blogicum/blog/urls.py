from django.urls import path, include, reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='index'),
    path('posts/<int:post_id>/', views.PostDisplayView.as_view(),
         name='post_detail'),
    path('posts/create/', views.NewPostView.as_view(), name='create_post'),
    path('posts/<int:post_id>/edit/', views.PostEditView.as_view(),
         name='edit_post'),
    path('posts/<int:post_id>/delete/', views.PostRemovalView.as_view(),
         name='delete_post'),
    path('posts/<int:post_id>/comment/', views.AddCommentView.as_view(),
         name='add_comment'),
    path('posts/<int:post_id>/comments/<int:pk>/edit/',
         views.EditCommentView.as_view(),
         name='edit_comment'),
    path('posts/<int:post_id>/comments/<int:pk>/delete/',
         views.RemoveCommentView.as_view(),
         name='delete_comment'),
    path('profile/edit/', views.ProfileUpdateView.as_view(),
         name='edit_profile'),
    path('profile/<str:username>/', views.UserPostsView.as_view(),
         name='profile'),
    path('category/<slug:category_slug>/',
         views.CategoryPostsView.as_view(),
         name='category_posts'),
    path('auth/registration/',
         CreateView.as_view(
             template_name='registration/registration_form.html',
             form_class=UserCreationForm,
             success_url=reverse_lazy('blog:index'),
         ),
         name='registration'),
    path('auth/', include('django.contrib.auth.urls')),
]
