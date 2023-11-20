from django.db import models
from os import getenv


# Create your models here.
Limit = int(getenv('Limit', 20))
Offset = int(getenv('Offset', 0))


class Manager(models.Manager):
    def get(self, **kwargs):
        try:
            return super().get(**kwargs)
        except:
            return None


class _(models.Model):

    objects = Manager()

    def Json(self):
        return {'id': self.id}

    def Overview(self):
        return {'id': self.id}

    class Meta:
        abstract = True
        ordering = ("-id", )


class BlogCategory(_):
    Name = models.CharField(max_length=200, unique=True,
                            null=False, blank=False)
    CreatedAt = models.DateTimeField(auto_now_add=True)

    def Json(self):
        data = self.Overview()
        data["blog"] = [_.Overview() for _ in self.blog_set.all()[:Limit]]
        return data

    def Overview(self):
        return {"id": self.id, "name": self.Name, "createdAt": self.CreatedAt}

    def __str__(self) -> str:
        return f"[ {self.id} ] {self.Name}"


class Blog(_):
    Category = models.ForeignKey(
        BlogCategory, null=False, on_delete=models.PROTECT)
    Title = models.CharField(max_length=200, null=False, blank=False)
    OverView = models.TextField(blank=False)
    Description = models.TextField(blank=False)

    Cover = models.ImageField(upload_to="Blog")
    CreatedAt = models.DateTimeField(auto_now_add=True)
    View = models.BigIntegerField(default=0, null=False)
    Comment = models.ManyToManyField("Comment", blank=True)
    Images = models.ManyToManyField("BlogImage", blank=True)

    def __str__(self) -> str:
        return f"{self.Title} ({self.id})"

    def Json(self):
        self.View += 1
        self.save()
        data = self.Overview()
        data.update({
            "overView": self.OverView,
            "description": self.Description,
            "comment": [_.Json() for _ in self.Comment.all()[:Limit]],
            "images": [_.Json() for _ in self.Images.all()]
        })
        return data

    def Overview(self):
        return {
            "id": self.id,
            "cover": self.Cover.url,
            "category": self.Category.Overview(),
            "title": self.Title,
            "createdAt": self.CreatedAt,
            "view": self.View
        }


class BlogImage(_):
    Link = models.ImageField(upload_to="Gallery")

    def Json(self):
        return {"id": self.id, "link": self.Link}

    def __str__(self) -> str:
        return f"{self.Link} ({self.id})"


class Comment(_):
    Text = models.TextField(blank=False)
    CreatedAt = models.DateTimeField(auto_now_add=True)

    def Json(self):
        return self.Overview()

    def Overview(self):
        return {"id": self.id, "content": self.Text, "createdAt": self.CreatedAt}

    def __str__(self) -> str:
        return f"{self.Text[:30]} ({self.id})"


class EmailList(_):
    Email = models.EmailField(max_length=100, unique=True)
    CreatedAt = models.DateTimeField(auto_now_add=True)

    def Json(self):
        return {**super().Json(), "email": self.Email, "created": self.CreatedAt}

    def __str__(self) -> str:
        return f"{self.Email} ({self.id})"


# ================================= =================================

class GroupImage(_):
    Title = models.CharField(max_length=300)
    CreatedAt = models.DateTimeField(auto_now_add=True)

    def Json(self):
        data = self.Overview()
        data.update({"image": [_.Overview() for _ in self.image_set.all()]})
        return data

    def Overview(self):
        return {"id": self.id, "title": self.Title, "createdAt": self.CreatedAt}

    def __str__(self) -> str:
        return f"( {self.id} ) {self.Title}"


class Image(_):
    Group = models.ForeignKey(GroupImage, on_delete=models.CASCADE)

    Link = models.ImageField(upload_to="Gallery")
    Description = models.TextField()

    Facebook = models.URLField()
    Instagram = models.URLField()
    Twitter = models.URLField()
    Youtube = models.URLField()

    def Json(self):
        return self.Overview()

    def Overview(self):
        return {
            "id": self.id, "link": self.Link.url,
            "group_id": self.Group_id, "description": self.Description,
            "facebook": self.Facebook, "instagram": self.Instagram,
            "twitter": self.Twitter, "youtube": self.Youtube
        }

    def __str__(self) -> str:
        return f"[ {self.Group_id} ] [ {self.id} ] { self.Link }"


class Agence(_):
    Name = models.CharField(max_length=1000)
    Address = models.CharField(max_length=1000)
    Phone = models.CharField(max_length=1000)
    Fax = models.CharField(max_length=1000)
    CreatedAt = models.DateTimeField(auto_now_add=True)

    def Json(self):
        return self.Overview()

    def Overview(self):
        return {
            "id": self.id, "name": self.Name,
            "address": self.Address, "phone": self.Phone,
            "fax": self.Fax, "created": self.CreatedAt
        }

    def __str__(self) -> str:
        return f"[ {self.id} ] {self.Name}"


class Product(_):
    Name = models.CharField(max_length=1000, null=False, blank=False)
    Description = models.TextField()
    CreatedAt = models.DateTimeField(auto_now_add=True)

    def Json(self):
        _ = self.Overview()
        _.update({
            "images": [x.Overview() for x in self.productimage_set.all()]
        })
        return _

    def Overview(self):
        return {"id": self.id, "name": self.Name, "description": self.Description, "created": self.CreatedAt}

    def __str__(self) -> str:
        return f"[ {self.id} ] {self.Name}"


class ProductImage(_):
    Image = models.ImageField(
        upload_to="Product Image", null=False, blank=False)
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def Json(self):
        return self.Overview()

    def Overview(self):
        return {"id": self.id, "link": self.Image.url, "product_id": self.Product_id}

    def __str__(self) -> str:
        return f"[ {self.id} ] [ {self.Product_id} ] {self.Image.url}"


class Member(_):
    Name = models.CharField(max_length=1000, blank=True, null=False)
    Profile = models.ImageField(upload_to="Member Profile")
    Post = models.CharField(max_length=200)
    Phone = models.CharField(max_length=20)
    Email = models.EmailField(max_length=150)
    CreatedAt = models.DateTimeField(auto_now_add=True)

    def Json(self):
        return self.Overview()

    def Overview(self):
        return {
            "id": self.id, "name": self.Name, "post": self.Post,
            "profile": self.Profile.url, "phone": self.Phone,
            "email": self.Email, "created": self.CreatedAt
        }

    def __str__(self) -> str:
        return self.Name


class CoverImage(_):
    Image = models.ImageField(upload_to="Cover Image", null=False, blank=False)

    def Json(self):
        return self.Overview()

    def Overview(self):
        return {"id": self.id, "link": self.Image.url}

    def __str__(self) -> str:
        return f"[ {self.id} ] {self.Image.url}"
