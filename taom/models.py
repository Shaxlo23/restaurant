from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.utils.text import slugify
from uuid import uuid4

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError("Email ni bo'sh bo'lishi mumkin emas")
        
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)

        user.save()
        
        return user
    
    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)

        return self.create_user(email,password,**extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    phone = models.CharField(max_length=40,blank=False,null=False)
    image = models.ImageField(upload_to='images/',default='images/default.jpg',blank=True,null=False)
    
    slug = models.SlugField(blank=True,null=False,unique=True)

    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=False)

    objects = CustomUserManager()

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.first_name}-{self.last_name}-{str(uuid4())[:4]}")
        super().save(*args,**kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Restaurant(models.Model):
    name = models.CharField(max_length=100,blank=False,null=False)
    address = models.CharField(max_length=200,blank=False,null=False)
    phone = models.CharField(max_length=20,blank=False,null=False)
    logo = models.ImageField(upload_to='logos/',default='logos/default.jpg',blank=True,null=False)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=False)

    slug = models.SlugField(blank=True,null=False,unique=True)


    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='restaurants',
        null=True,
        blank=True,
    )

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{str(uuid4())[:4]}")
        super().save(*args,**kwargs)


    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100,blank=False,null=False)
    slug = models.SlugField(blank=True,unique=True)

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{str(uuid4())[:4]}")

        super().save(*args,**kwargs)

    def __str__(self):
        return self.name
    

class Dish(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='dishes'
    )

    categories = models.ManyToManyField(
        Category,
        related_name='dishes'
        
    )

    name = models.CharField(max_length=50,blank=False,null=False)
    price = models.PositiveIntegerField(blank=False,null=False)
    image = models.ImageField(upload_to='dishes/',default='dishes/default.jpg',blank=True,null=False)

    is_available = models.BooleanField(default=True,blank=True,null=False)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=False)

    slug = models.SlugField(blank=True,null=False,unique=True)

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{str(uuid4())[:4]}")

        super().save(*args,**kwargs)

    def __str__(self):
        return self.name

