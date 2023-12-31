# Generated by Django 4.2.2 on 2023-07-12 09:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_skills_options'),
        ('projects', '0007_alter_projects_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.profile'),
        ),
    ]
