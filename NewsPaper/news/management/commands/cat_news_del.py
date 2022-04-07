from django.core.management.base import BaseCommand, CommandError
from NewsPaper.news.models import Post, Category


class Command(BaseCommand):
    help = "Команда, удаляющая посты указанной категории"

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы правда хотиту удалить все статьи в категории {options["category"]}? yes/no')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR("Отменено"))

        try:
            category = Category.objects.get(categoryName=options["category"])
            Post.objects.filter(postCategory=category)
            self.stdout.write(self.style.SUCCESS(f"Все новости категории {category.categoryName} успешно удалены!"))
        except Post.DoesNotExist:
            raise CommandError(f'Категории {options["category"]} не существует!')
            # self.stdout.write(self.style.ERROR(f'Категории {options["category"]} не существует!'))
