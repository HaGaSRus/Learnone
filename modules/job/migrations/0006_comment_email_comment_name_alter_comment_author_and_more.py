# Generated by Django 4.2.10 on 2024-04-01 09:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('job', '0005_alter_article_full_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='email',
            field=models.EmailField(blank=True, max_length=255, verbose_name='Email посетителя'),
        ),
        migrations.AddField(
            model_name='comment',
            name='name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Имя посетителя'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments_author', to=settings.AUTH_USER_MODEL, verbose_name='Автор комментария'),
        ),
        migrations.CreateModel(
            name='ViewCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(verbose_name='IP адрес')),
                ('viewed_on', models.DateTimeField(auto_now_add=True, verbose_name='Дата просмотра')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='views', to='job.article')),
            ],
            options={
                'verbose_name': 'Просмотр',
                'verbose_name_plural': 'Просмотры',
                'ordering': ('-viewed_on',),
                'indexes': [models.Index(fields=['-viewed_on'], name='job_viewcou_viewed__e54270_idx')],
            },
        ),
    ]
