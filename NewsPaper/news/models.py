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

    def __str__(self):
        return f'{self.authorUser.username}'


class Category(models.Model):
    categoryName = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f'{self.categoryName}'


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

    def __str__(self):
        return f'{self.title}, рейт {self.rate}, дата {self.creationDate.strftime("%m/%d/%Y, %H:%M:%S")}'

    def get_absolute_url(self):
        return f'/news/{self.id}'


class PostCategory(models.Model):
    posts = models.ForeignKey(Post, on_delete=models.CASCADE)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.posts.title}, категория: {self.categories.categoryName}'


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

    def __str__(self):
        return f'Пост: {self.commentPost.title}, пользователь: {self.commentUser.username}: {self.text[:20]}, ' \
               f'рейт: {self.rate}, дата: {self.creationDate.strftime("%m/%d/%Y, %H:%M:%S")}'
