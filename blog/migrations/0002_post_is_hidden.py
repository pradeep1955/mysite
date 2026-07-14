from django.db import migrations, models
class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0001_initial"),
    ]
    operations = [
        migrations.AddField(
            model_name="post",
            name="is_hidden",
            field=models.BooleanField(
                default=False,
                help_text="Hides this post from the public blog list and detail page. Still visible to you in admin and when logged in as the author.",
            ),
        ),
    ]