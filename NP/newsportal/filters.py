from django_filters import FilterSet, ModelChoiceFilter, DateFilter
from .models import Post, Author
import django.forms.widgets


class PostFilter(FilterSet):
    time_is = DateFilter(
        label="Date creation",
        lookup_expr='gt',
        widget = django.forms.DateInput(attrs={'type': 'date',}),
    )

    author = ModelChoiceFilter(
        field_name='author',
        queryset=Author.objects.all(),
        empty_label='Any',
        label = "Author",
    )


    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'category' : ['exact']
            # 'dateCreation': ['gt'],
        }
