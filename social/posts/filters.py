import django_filters

from .models import Post


class PostFilter(django_filters.FilterSet):
    content = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Post
        fields = {
            "user": ["exact"],
            "hashtags__name": ["icontains"],
        }
