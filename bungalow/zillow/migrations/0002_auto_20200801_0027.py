# Generated by Django 3.0.8 on 2020-08-01 05:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('zillow', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField()),
                ('date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='RentEstimate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estimate_amount', models.PositiveIntegerField()),
                ('estimate_date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tax_value', models.FloatField()),
                ('tax_year', models.PositiveIntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='listing',
            name='price',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='tax_value',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='tax_year',
        ),
        migrations.RemoveField(
            model_name='rent',
            name='estimate_amount',
        ),
        migrations.RemoveField(
            model_name='rent',
            name='estimate_date',
        ),
        migrations.AddField(
            model_name='listing',
            name='bathrooms',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='bedrooms',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='size',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='year_build',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='rent',
            name='date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='rent',
            name='price',
            field=models.PositiveIntegerField(),
        ),
        migrations.DeleteModel(
            name='Building',
        ),
        migrations.AddField(
            model_name='tax',
            name='listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zillow.Listing'),
        ),
        migrations.AddField(
            model_name='rentestimate',
            name='listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zillow.Listing'),
        ),
        migrations.AddField(
            model_name='price',
            name='listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zillow.Listing'),
        ),
    ]
