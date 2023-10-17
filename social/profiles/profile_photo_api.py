import os


def get_filename_extension(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def profile_photo_path(instance, filename, **kwargs):
    new_filename = instance.id
    # final_filename = instance.user.username
    name, ext = get_filename_extension(filename)
    final_filename = f"{instance.user.username}_{ext}"
    return f"{new_filename}/{final_filename}"
