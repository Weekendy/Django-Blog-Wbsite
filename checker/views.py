from django.shortcuts import render, redirect
from blogs.models import BlogPostMedia
from .forms import *
from django.http import Http404
from blog import settings
import os

def image_active(request, media_objects, ab_url):
    if not request.user.is_staff:
        raise Http404

    media = media_objects.filter(activate=False).order_by('date_added').first()
    if request.method != "POST":
        form = ActiveForm()
    else:
        form = ActiveForm(data=request.POST)
        if form.is_valid():
            if form.cleaned_data['activate']:
                media.activate = True
                media.save()
            else:
                os.remove(os.path.join(settings.MEDIA_ROOT, str(media.image)))
                media.delete()
            return redirect(ab_url)
            
    context = {'media': media, 'form': form}
    return render(request, 'checker/image_active.html', context)

def blogpost_photo(request):
    return image_active(request, BlogPostMedia.objects, 'checker:blogpost_photo')