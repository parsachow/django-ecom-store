# Generated by Django 4.2.6 on 2024-10-24 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_remove_order_shipping'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipping',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.order'),
        ),
    ]
