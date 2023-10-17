import shortuuid
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.text import slugify
from django.utils.timesince import timesince

from .models import Post


def post_list(request):
    posts = Post.objects.all()
    context = {"posts": posts}
    return render(request, "posts/post_list.html", context=context)


def post_create(request):
    """
    It extracts and processes data from the request, including post-content, visibility settings, and an optional
    image The view generates a unique identifier for the post, creates a new Post object with the provided data,
    and stores it in the database If both the content and image are provided-the view responds with a structured
    JSON response-containing comprehensive details about the newly created post, such as content, image URL,
    In case either the content or image is missing, the view returns a JSON error response For non-POST
    requests, the view responds with a JSON acknowledgment that data has been received.
    """
    if request.method == "POST":
        content = request.POST.get("post-content")
        visibility = request.POST.get("post-visibility")
        image = request.FILES.get("post-image")
        uuid_key = shortuuid.uuid()
        unique_id = uuid_key[:5]
        if content or image:
            post = Post(
                content=content,
                visibility=visibility,
                image=image,
                slug=slugify(content) + "-" + str(unique_id.lower()),
            )
            post.save()
            return JsonResponse(
                {
                    "post": {
                        "content": post.content,
                        "image": image.url,
                        "username": post.user.username,
                        "profile_photo": post.user.profile.profile_photo.url,
                        "timestamp": timesince(post.timestamp),
                        "id": post.id,
                    }
                }
            )
        else:
            return JsonResponse({"error": f"{image} or {content} does not exist!"})

    return JsonResponse({"data": "sent"})

    # context = {""}
    # return render(request, "posts/post_create.html", context=context)
