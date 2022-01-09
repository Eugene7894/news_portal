from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    authorRate = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRate=Sum('rate'))
        pRat = 0
        pRat += postRat.get('postRate')

        commentRat = self.authorUser.comment_set.aggregate(commentRate=Sum('rate'))
        cRat = 0
        cRat += commentRat.get('commentRate')

        self.authorRate = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    categoryName = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NW'
    ARTICLES = 'AR'
    CATEGORY_CHOICE = [
        (NEWS, 'Новости'),
        (ARTICLES, 'Статьи')
    ]
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICE, default=ARTICLES)
    creationDate = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rate = models.SmallIntegerField(default=0)

    def like(self):
        self.rate += 1
        self.save()

    def dislike(self):
        self.rate -= 1
        self.save()

    def preview(self):
        return f'{self.text[:123]} ...'


class PostCategory(models.Model):
    posts = models.ForeignKey(Post, on_delete=models.CASCADE)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    creationDate = models.DateTimeField(auto_now_add=True)
    rate = models.SmallIntegerField(default=0)

    def like(self):
        self.rate += 1
        self.save()

    def dislike(self):
        self.rate -= 1
        self.save()

