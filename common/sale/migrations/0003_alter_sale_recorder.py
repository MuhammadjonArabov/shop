# Generated by Django 4.2.13 on 2024-07-02 08:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sale', '0002_alter_sale_recorder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='recorder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='staffSale', to=settings.AUTH_USER_MODEL),
        ),
    ]