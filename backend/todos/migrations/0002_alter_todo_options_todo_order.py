"""Migration to add order field to Todo model."""

from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration adding order field and updating ordering."""

    dependencies = [
        ("todos", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="Todo",
            options={"ordering": ["order", "id"]},
        ),
        migrations.AddField(
            model_name="Todo",
            name="order",
            field=models.IntegerField(default=0),
        ),
    ]
