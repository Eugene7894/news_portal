from django.contrib import admin
from .models import Author, Category, Post, Comment, PostCategory
from modeltranslation.admin import TranslationAdmin


def nullfy_author_rate(modeladmin, request, queryset):  # request — объект хранящий информацию о запросе и queryset —
    # - грубо говоря, набор объектов, которые мы выделили галочками.
    queryset.update(authorRate=0)


nullfy_author_rate.short_description = 'Обнулить рейтинг авторов' # описание для более понятного представления в админ-
# -панели задаётся, как будто это объект


# создаём новый класс для представления авторов в админке
class AuthorAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями модели, которые вы хотите видеть в таблице
    list_display = ('authorUser', 'authorRate')
    # list_display = [field.name for field in
    #                 Author._meta.get_fields()]  # генерируем список имён всех полей для более красивого отображения
    list_filter = ('authorUser__username', 'authorRate')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('authorUser__username', 'authorRate')  # тут всё очень похоже на фильтры из запросов в базу
    actions = [nullfy_author_rate]  # добавляем действия в список


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('categoryName', 'get_subscribers')
    list_filter = ('categoryName', 'subscribers__username')
    search_fields = ('categoryName', 'subscribers__username')


class CategoryTranslationAdmin(TranslationAdmin):
    model = Category


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'get_categories',
                    'categoryType', 'creationDate', 'rate')
    list_filter = ('author__authorUser__username', 'postCategory__categoryName', 'categoryType', 'creationDate')
    search_fields = ('author__authorUser__username', 'postCategory__categoryName', 'title')


class PostTranslationAdmin(TranslationAdmin):
    model = Post


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in
                    PostCategory._meta.get_fields()]
    # list_display = ('posts', 'categories')
    list_filter = ('posts', 'categories')
    search_fields = ('posts', 'categories')


class CommentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in
                    Comment._meta.get_fields()]
    list_filter = ('commentUser', 'creationDate', 'commentPost__title')
    search_fields = ('commentUser__username', 'commentPost__title')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
