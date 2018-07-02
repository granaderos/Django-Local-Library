# Generated by Django 2.0.6 on 2018-07-02 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_auto_20180702_0841'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='bookinstance',
            name='imprint',
        ),
        migrations.AddField(
            model_name='book',
            name='copies',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='book',
            name='imprint',
            field=models.CharField(help_text='Enter imprint information of the book.', max_length=200, null=True),
        ),
    ]
