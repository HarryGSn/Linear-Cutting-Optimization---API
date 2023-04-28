# Generated by Django 4.1.7 on 2023-04-28 21:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Optimization',
            fields=[
                ('id', models.AutoField(help_text='ID -> PK, Auto Increment', primary_key=True, serialize=False)),
                ('kerf', models.FloatField(default=0)),
                ('deduct_left', models.FloatField(default=0)),
                ('deduct_right', models.FloatField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Optimization',
                'verbose_name_plural': 'Optimizations',
                'db_table': 'optimizations',
            },
        ),
        migrations.CreateModel(
            name='OptimizationBar',
            fields=[
                ('id', models.AutoField(help_text='ID -> PK, Auto Increment', primary_key=True, serialize=False)),
                ('optimization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='optimizations.optimization')),
            ],
            options={
                'verbose_name': 'OptimizationBar',
                'verbose_name_plural': 'OptimizationBars',
                'db_table': 'optimization_bars',
            },
        ),
        migrations.CreateModel(
            name='OptimizationPart',
            fields=[
                ('id', models.AutoField(help_text='ID -> PK, Auto Increment', primary_key=True, serialize=False)),
                ('length', models.FloatField()),
                ('quantity', models.IntegerField(default=1)),
                ('optimization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='optimizations.optimization')),
            ],
            options={
                'verbose_name': 'OptimizationPart',
                'verbose_name_plural': 'OptimizationParts',
                'db_table': 'optimization_parts',
            },
        ),
        migrations.CreateModel(
            name='OptimizationBarPart',
            fields=[
                ('id', models.AutoField(help_text='ID -> PK, Auto Increment', primary_key=True, serialize=False)),
                ('length', models.FloatField()),
                ('optimization_bar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='optimizations.optimizationbar')),
            ],
            options={
                'verbose_name': 'OptimizationBarPart',
                'verbose_name_plural': 'OptimizationBarParts',
                'db_table': 'optimization_bar_parts',
            },
        ),
    ]
