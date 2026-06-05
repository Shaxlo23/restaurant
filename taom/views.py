from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import Restaurant,Dish
from django.http import HttpResponseForbidden

User = get_user_model()

# Create your views here.

def home_view(request):
    return render(request, 'home.html')


def users_list(request):
    users = User.objects.all()
    return render(request, 'users_list.html', {'users': users})

def user_detail(request, slug):
    user = get_object_or_404(User, slug=slug)
    return render(request, 'user_detail.html', {'user': user})

def user_create(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        image = request.FILES.get('image')


        User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            image=image
        )

        return redirect('/')
    return render(request, 'user_create.html')


def user_update(request, slug):
    user = get_object_or_404(User, slug=slug)

    if request.method == 'POST':
        user.first_name= request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.image = request.FILES.get('image')

        if user.image:
            user.image = user.image

        user.save()

        return redirect(f'/user/{user.slug}')
    return render(request, 'user_update.html', {'user': user})

def user_delete(request, slug):
    user = get_object_or_404(User,slug=slug)
    if request.method=='POST':
        user.delete()

        return redirect('/')
    return render(request,'user_delete.html',{'user': user})





def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurant_list.html', {'restaurants': restaurants})

def restaurant_detail(request,slug):
    restaurant = get_object_or_404(Restaurant,slug=slug)

    return render(request, 'restaurant_detail.html', {'restaurant': restaurant})

def restaurant_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        logo = request.FILES.get('logo')

        Restaurant.objects.create(
            name=name,
            address=address,
            phone=phone,
            logo=logo,
            owner=request.user
        )

        return redirect('/restaurant/')
    
    return render(request, 'restaurant_create.html')

def restaurant_update(request,slug):
    restaurant = get_object_or_404(Restaurant,slug=slug)

    
    if restaurant.owner != request.user:
        return HttpResponseForbidden("Siz bu restaurantni edit qilishingiz mumkinmas!")

    if request.method == 'POST':
        restaurant.name = request.POST.get('name')
        restaurant.address = request.POST.get('address')
        restaurant.phone = request.POST.get('phone')
        restaurant.logo = request.FILES.get('logo')

        if restaurant.logo:
            restaurant.logo = restaurant.logo

        restaurant.save()

        return redirect(f'/restaurant/{restaurant.slug}/')
    
    return render(request, 'restaurant_update.html', {'restaurant': restaurant})


def restaurant_delete(request,slug):
    
    restaurant = get_object_or_404(Restaurant,slug=slug)

    if restaurant.owner != request.user:
        return HttpResponseForbidden("Siz bu restaurantni o'chirishingiz mumkinmas!")

    if request.method == 'POST':
        restaurant.delete()

        return redirect('/restaurant/')
    
    return render(request, 'restaurant_delete.html', {'restaurant': restaurant})

@login_required
def dish_create(request, slug):
    restaurant = get_object_or_404(Restaurant, slug=slug)

    if restaurant.owner != request.user:
        return HttpResponseForbidden("Siz bu restaurantga taom qo'shishingiz mumkinmas!")

    if request.method == 'POST':
        name = request.POST.get('name')

        price = request.POST.get('price')

        image = request.FILES.get('image')

        Dish.objects.create(
            restaurant = restaurant,
            name = name,
            price = price,
            image = image
        )

        return redirect(f'/restaurant_detail/{restaurant.slug}/')
    
    return render(request, 'dish_create.html', {'restaurant': restaurant})

@login_required
def dish_update(request,slug):
    dish = get_object_or_404(Dish,slug=slug)

    if dish.restaurant.owner != request.user:
        return HttpResponseForbidden("Siz bu taomni edit qilishingiz mumkinmas!")
    if request.method == 'POST':
        name = request.POST.get('name')

        price = request.POST.get('price')

        image = request.FILES.get('image')


        dish.save()

        return redirect(f'/restaurant_detail/{dish.restaurant.slug}/')
    
    return render(request,'dish_update.html',{'dish':dish})

@login_required
def dish_delete(request,slug):
    dish=get_object_or_404(Dish,slug=slug)

    if dish.restaurant.owner != request.user:
        return HttpResponseForbidden("Siz bu taomni o'chirishingiz mumkinmas!")

    if request.method=='POST':
        dish.delete()

        return redirect(f'/restaurant_detail/{dish.restaurant.slug}/')
    
    return render(request,'dish_delete.html',{'dish': dish})