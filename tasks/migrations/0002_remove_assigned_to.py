from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0001_initial"),
    ]

    operations = [
        # Drop stray assigned_to_id column if it exists (safe no-op otherwise)
        migrations.RunSQL(
            sql=(
                "ALTER TABLE tasks_task DROP COLUMN IF EXISTS assigned_to_id;"
            ),
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
