from django.urls import path
from .views import NewsList, PostDetail, Search, PostCreate, ArticleList, PostUpdate, FullList, PostDelete, UserUpdate, \
    make_me_author, unsubscribe, subscribe
from .filters import PostFilter

urlpatterns = [
    path("", FullList.as_view(), name='full_list'),
    path("accounts/profile/", UserUpdate.as_view(), name='user_update'),
    path("news/", NewsList.as_view(), name='news'),
    path("articles/", ArticleList.as_view(), name='articles'),
    path('news/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('articles/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', Search.as_view(), name='post_filter'),
    path('news/create/', PostCreate.as_view(), name='post_create'),
    path('articles/create/', PostCreate.as_view(), name='post_create'),
    path('news/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('articles/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path("accounts/profile/upgrade/", make_me_author, name='upgrade'),
    path("news/subscribe/", subscribe, name='subscribe'),
    path("news/unsubscribe/", unsubscribe, name='unsubscribe'),
]
