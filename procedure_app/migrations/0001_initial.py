# Generated by Django 4.0.3 on 2022-04-05 08:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Procedure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('procedure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='section', to='procedure_app.procedure')),
            ],
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=50)),
                ('options', models.CharField(max_length=100)),
                ('is_table', models.CharField(max_length=100)),
                ('validations', models.CharField(max_length=100)),
                ('target', models.CharField(max_length=50)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='field', to='procedure_app.section')),
            ],
        ),
    ]
