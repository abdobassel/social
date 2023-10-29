# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.urls import reverse_lazy
# from django.views.generic import CreateView, DetailView, ListView
#
# from .forms import PostForms
# from .models import Post
#
#
# class PostListView(ListView):
#     model = Post
#     template_name = "posts/home.html"
#     context_object_name = "posts"
#     ordering = ["-timestamp"]  # Order by timestamp in descending order
#
#
# class DetailPostView(DetailView):
#     model = Post
#     template_name = "posts/post_detail.html"
#     context_object_name = "post"
#
#     def get_object(self, queryset=None):
#         # Use both 'id' and 'slug' for filtering the Post object
#         return Post.objects.get(id=self.kwargs["id"])
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["id"] = self.kwargs["id"]
#         return context
#
#
# class CreatePostView(LoginRequiredMixin, CreateView):
#     model = Post
#     form_class = PostForms
#     template_name = "posts/post_create.html"
#     success_url = reverse_lazy("posts:post-list")
#     ordering = ["-timestamp"]  # Order by timestamp in descending order
#
#     def form_valid(self, form):
#         post = form.save(commit=False)
#         post.user = self.request.user
#         post.save()
#         return super().form_valid(form)
