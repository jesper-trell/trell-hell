from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import generic

from .forms import *
from .models import Photo


class IndexView(generic.ListView):
    template_name = 'photos/index.html'
    context_object_name = 'photos_list'

    def get_queryset(self):
        return Photo.objects.order_by('-pub_date')[:]


class ProfileView(generic.ListView):
    template_name = 'photos/profile.html'
    context_object_name = 'photos_list'

    def get_queryset(self):
        return Photo.objects.order_by('-pub_date')[:]


def photo(request, photo_hashid):
    photo = Photo.objects.get(hashid=photo_hashid)

    context = {
        'photo': photo,
        }
    
    return render(request, 'photos/photo.html', context)

def upload(request): 
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST': 
        form = UploadForm(request.POST, request.FILES) 
  
        if form.is_valid(): 
            form = form.save(commit=False)
            form.pub_date = timezone.now()
            form.user = request.user
            form.save()

            photo = Photo.objects.get(hashid=form.hashid)

            context = {
                'photo': photo,
            }
    
            return render(request, 'photos/photo.html', context)
    else: 
        form = UploadForm() 
    return render(request, 'photos/upload.html', {'form' : form}) 


def register(request):
    if request.method == "GET":
        return render(
            request, "photos/register.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("index"))

# def edit(request, product_id):
#     product = ProductModel.objects.get(id=product_id)

#     if(request.method == "POST"):
#         form = ProductForm(request.POST, instance=product)

#         if(form.is_valid):
#             form.save()
#             return redirect("/")

#     else:
#         form = ProductForm()

#     template_name = "products/edit.html"
#     context = {
#         "ProductForm":ProductForm,
#         "ProductModel":ProductModel.objects.get(id=product_id),
# }