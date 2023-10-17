from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView

from .forms import UserProfileForm
from .models import Profile


class ProfileAuthorizationMixin:
    def dispatch(self, request, *args, **kwargs):
        profile = self.get_object()

        if profile.user != request.user:
            return redirect("home")  # Redirect unauthorized users

        return super().dispatch(request, *args, **kwargs)


class ProfileListView(ListView):
    # queryset = Profile.objects.all()
    model = Profile
    template_name = "profiles/profile_list.html"
    context_object_name = "profiles"

    # def get_queryset(self):
    #     return self.model.objects.filter(user=self.request.user)


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "profiles/profile_detail.html"
    context_object_name = "profile"
    pk_url_kwarg = "pk"  # Define the URL keyword argument to use for pk


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UserProfileForm
    template_name = "profiles/profile_update.html"
    success_url = reverse_lazy("profile-list")

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("profiles:profile-detail", kwargs={"pk": self.object.pk})
