# Generated by Django 3.2.5 on 2021-11-11 00:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0007_auto_20211108_2327'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actiondetail', models.TextField()),
                ('contactlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.contactlist')),
            ],
        ),
    ]
