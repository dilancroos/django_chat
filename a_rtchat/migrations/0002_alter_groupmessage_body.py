from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("a_rtchat", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="groupmessage",
            name="body",
            field=models.TextField(),
        ),
    ]
