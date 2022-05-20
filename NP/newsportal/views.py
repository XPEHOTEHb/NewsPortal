from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm


class FullList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'posts'
    queryset = Post.objects.all().order_by('-rating')
    paginate_by = 1


class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'posts'
    queryset = Post.objects.filter(category = 'NW')
    paginate_by = 1


class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'post'

class ArticleList(ListView):
    model = Post
    template_name = 'articles.html'
    context_object_name = 'posts'
    queryset = Post.objects.filter(category = 'AR')
    paginate_by = 1


"""class ArticleDetail(DetailView):
    model = Post
    template_name = 'article.html'
    context_object_name = 'post'"""


class Search(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-id')

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        app_url = self.request.path
        if 'news' in app_url:
            post.category = "NW"
        else:
            post.category = "AR"
        return super().form_valid(form)

class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('full_list')

