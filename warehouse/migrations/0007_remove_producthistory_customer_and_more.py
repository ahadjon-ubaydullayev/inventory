# Generated by Django 5.0.3 on 2024-07-26 18:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("warehouse", "0006_remove_producthistory_customer_id_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="producthistory",
            name="customer",
        ),
        migrations.RemoveField(
            model_name="producthistory",
            name="product",
        ),
        migrations.AddField(
            model_name="producthistory",
            name="customer_id",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="producthistory",
            name="product_id",
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="producthistory",
            name="transaction_type",
            field=models.CharField(max_length=10),
        ),
    ]
