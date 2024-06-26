# Generated by Django 4.2.13 on 2024-06-13 11:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_active', models.BooleanField(default=True)),
                ('sale_id', models.CharField(max_length=50)),
                ('code', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('totalAmount', models.DecimalField(decimal_places=6, default=0, max_digits=50)),
                ('status', models.IntegerField(choices=[(1, 'PENDING'), (2, 'COMPLETED'), (3, 'CANCELED')], default=1)),
                ('recorder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='staffSale', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SaleProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_active', models.BooleanField(default=True)),
                ('quantity', models.DecimalField(decimal_places=6, default=0, max_digits=50)),
                ('unitPrice', models.DecimalField(decimal_places=6, default=0, max_digits=50)),
                ('status', models.IntegerField(choices=[(1, 'SOLD'), (2, 'RETURNED')], default=1)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='productSaleProduct', to='product.product')),
                ('sale', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='saleSaleProduct', to='sale.sale')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SalePayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_active', models.BooleanField(default=True)),
                ('code', models.CharField(blank=True, max_length=50, unique=True)),
                ('amount', models.DecimalField(decimal_places=6, default=0, max_digits=50)),
                ('paymentType', models.IntegerField(choices=[(1, 'CASH'), (2, 'CARD')], default=1)),
                ('sale', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='saleSalePayment', to='sale.sale')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
