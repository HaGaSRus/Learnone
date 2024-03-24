from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
from django.urls import reverse
from taggit.managers import TaggableManager
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from modules.services.utils import  image_compress

from mptt.models import MPTTModel, TreeForeignKey

from pytils.translit import slugify


User = get_user_model()


class Article(models.Model):
    """
    Модель постов для сайта
    """

    class ArticleManager(models.Manager):
        """
        Кастомный менеджер для модели статей
        """

        def all(self):
            """
            Список статей (SQL запрос с фильтрацией для страницы списка статей)
            """
            return self.get_queryset().select_related('author', 'category').prefetch_related('ratings').filter(status='published')

        def detail(self):
            """
            Детальная статья (SQL запрос с фильтрацией для страницы со статьёй)
            """
            return self.get_queryset()\
                .select_related('author', 'category')\
                .prefetch_related('comments', 'comments__author', 'comments__author__profile', 'tags', 'ratings')\
                .filter(status='published')

    STATUS_OPTIONS = (
        ('published', 'Опубликовано'),
        ('draft', 'Черновик')
    )

    title = models.CharField(verbose_name='Заголовок', max_length=255)
    slug = models.CharField(verbose_name='URL', max_length=255, blank=True, unique=True)
    short_description = models.TextField(verbose_name='Краткое описание', max_length=500)
    full_description = models.TextField(verbose_name='Полное описание')
    thumbnail = models.ImageField(
        verbose_name='Превью поста',
        blank=True,
        upload_to='images/thumbnails/',
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))]
    )
    status = models.CharField(choices=STATUS_OPTIONS, default='published', verbose_name='Статус поста', max_length=10)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    author = models.ForeignKey(to=User, verbose_name='Автор', on_delete=models.SET_DEFAULT, related_name='author_posts', default=1)
    updater = models.ForeignKey(to=User, verbose_name='Обновил', on_delete=models.SET_NULL, null=True, related_name='updater_posts', blank=True)
    fixed = models.BooleanField(verbose_name='Зафиксировано', default=False)
    category = TreeForeignKey('Category', on_delete=models.PROTECT, related_name='articles', verbose_name='Категория')
    thumbnail = models.ImageField(
        verbose_name='Превью поста',
        blank=True,
        upload_to='images/thumbnails/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))]
    )

    class Meta:
        db_table = 'app_articles'
        ordering = ['-fixed', '-time_create']
        indexes = [models.Index(fields=['-fixed', '-time_create', 'status'])]
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    custom = ArticleManager()

    short_description = CKEditor5Field(max_length=500, verbose_name='Краткое описание', config_name='extends')
    full_description = CKEditor5Field(verbose_name='Полное описание', config_name='extends')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('articles_detail', kwargs={'slug': self.slug})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__thumbnail = self.thumbnail if self.pk else None

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        if not self.slug:
            self.slug = slugify(self)
        super().save(*args, **kwargs)

        if self.__thumbnail != self.thumbnail and self.thumbnail:
            image_compress(self.thumbnail.path, width=500, height=500)

    tags = TaggableManager()

    def get_sum_rating(self):
        return sum([rating.value for rating in self.ratings.all()])


class Category(MPTTModel):
    """
    Модель категорий с вложенностью
    """
    title = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(max_length=255, verbose_name='Url категории', blank=True)
    description = models.TextField(verbose_name='Описание категории', max_length=300)
    parent = TreeForeignKey(
        'self',
        on_delete = models.CASCADE,
        null = True,
        blank = True,
        db_index = True,
        related_name = 'children',
        verbose_name = 'Родительская категория'
    )

    class MPTTMeta:
        """
        Сортировка по вложенности
        """
        order_insertion_by = ('title',)

    class Meta:
        """
        Сортировка, название модели в админ панели, таблица с данными
        """
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'app_categories'

    def __str__(self):
        """
        Возвращение заголовка категории
        """
        return self.title

    def get_absolute_url(self):
        return reverse('articles_by_category', kwargs={'slug': self.slug})


class Comment(MPTTModel):
    """
    Модель древовидных комментариев
    """
    STATUS_OPTIONS = (
        ('published', 'Опубликовано'),
        ('draft', 'Черновик')
    )

    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья', related_name='comments')
    author = models.ForeignKey(User, verbose_name='Автор комментария', on_delete=models.CASCADE, related_name='comments_author')
    content = models.TextField(verbose_name='Текст комментария', max_length=3000)
    time_create = models.DateTimeField(verbose_name='Время добавления', auto_now_add=True)
    time_update = models.DateTimeField(verbose_name='Время обновления', auto_now=True)
    status = models.CharField(choices=STATUS_OPTIONS, default='published', verbose_name='Статус поста', max_length=10)
    parent = TreeForeignKey('self', verbose_name='Родительский комментарий', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    class MTTMeta:
        order_insertion_by = ('-time_create',)

    class Meta:
        db_table = 'app_comments'
        indexes = [models.Index(fields=['-time_create', 'time_update', 'status', 'parent'])]
        ordering = ['-time_create']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.author}:{self.content}'


class Rating(models.Model):
    """
    Модель рейтинга: Лайк - Дизлайк
    """
    article = models.ForeignKey(to=Article, verbose_name='Статья', on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(to=User, verbose_name='Пользователь', on_delete=models.CASCADE, blank=True, null=True)
    value = models.IntegerField(verbose_name='Значение', choices=[(1, 'Нравится'), (-1, 'Не нравится')])
    time_create = models.DateTimeField(verbose_name='Время добавления', auto_now_add=True)
    ip_address = models.GenericIPAddressField(verbose_name='IP Адрес')

    class Meta:
        unique_together = ('article', 'ip_address')
        ordering = ('-time_create', )
        indexes = [models.Index(fields=['-time_create', 'value'])]
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'

    def __str__(self):
        return self.article.title



