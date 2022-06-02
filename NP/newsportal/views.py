from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Subscribe, Category
from .filters import PostFilter
from .forms import PostForm, UserForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


@login_required
def make_me_author(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if 'authors' not in request.user.groups.filter(name='authors'):
        author_group.user_set.add(user)
        return redirect('/')


@login_required
def unsubscribe(request):
    sub = Subscribe.objects.get(subUser=request.user)
    sub.is_subscribe = False
    sub.save()
    return redirect('/')


@login_required
def subscribe(request):
    sub = Subscribe.objects.get(subUser=request.user)
    sub.is_subscribe = True
    sub.save()
    print("Subscribe", sub.subUser, sub.is_subscribe)
    sub.category.add(Category.objects.get(id=1))
    print(sub.category)
    return redirect('/')


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
    queryset = Post.objects.filter(category='NW')
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subscribe_status'] = Subscribe.objects.get(subUser=self.request.user).is_subscribe
        print(
            f'{Subscribe.objects.get(subUser=self.request.user).subUser}, {Subscribe.objects.get(subUser=self.request.user).is_subscribe}')
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subscribe_status'] = Subscribe.objects.get(subUser=self.request.user).is_subscribe
        print(f'{Subscribe.objects.get(subUser=self.request.user).subUser}, '
              f'{Subscribe.objects.get(subUser=self.request.user).category}, '
              f'{Subscribe.objects.get(subUser=self.request.user).is_subscribe}, '
              f'{Category.objects.get(pk=1).name}'
              )
        return context


class ArticleList(ListView):
    model = Post
    template_name = 'articles.html'
    context_object_name = 'posts'
    queryset = Post.objects.filter(category='AR')
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


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('newsportal.add_post',)
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


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('newsportal.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('newsportal.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('full_list')


class UserUpdate(LoginRequiredMixin, UpdateView):
    form_class = UserForm
    template_name = 'user_edit.html'
    success_url = reverse_lazy('user_update')

    def get_object(self, **kwargs):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'authors' not in self.request.user.groups.filter(name='authors'):
            context['is_not_author'] = True
        context['is_not_author'] = False
        # context['is_not_author'] = not self.request.user.groups.filter(name='authors').exist()
        context['subscribe_status'] = not Subscribe.is_subscribe
        return context
