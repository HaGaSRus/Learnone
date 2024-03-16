from django.urls import path

from .views import ArticleListView, ArticleDetailView, ArticleByCategoryListView, articles_list, ArticleCreateView

urlpatterns = [
    path('', ArticleListView.as_view(), name='home'),
    path('articles/', articles_list, name='articles_by_page'),
    path('articles/create/', ArticleCreateView.as_view(), name='articles_create'),
    path('articles/<str:slug>/', ArticleDetailView.as_view(), name='articles_detail'),
    path('category/<str:slug>/', ArticleByCategoryListView.as_view(), name="articles_by_category"),
]

