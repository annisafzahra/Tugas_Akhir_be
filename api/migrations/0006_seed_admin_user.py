import os
from django.db import migrations
from django.contrib.auth.hashers import make_password


def seed_admin_user(apps, schema_editor):
    User = apps.get_model('api', 'User')

    username = os.environ.get('ADMIN_USERNAME', 'admin')
    email = os.environ.get('ADMIN_EMAIL', 'admin@gmail.com')
    password = os.environ.get('ADMIN_PASSWORD', 'admin123')

    field_map = {field.name: field for field in User._meta.fields}

    admin = User.objects.filter(username=username).first()

    if admin:
        # Kalau user admin sudah ada, pastikan tetap jadi admin
        if 'is_staff' in field_map:
            admin.is_staff = True
        if 'is_superuser' in field_map:
            admin.is_superuser = True
        if 'is_active' in field_map:
            admin.is_active = True

        admin.save()
        return

    data = {
        'username': username,
        'email': email,
        'password': make_password(password),
    }

    if 'nama_lengkap' in field_map:
        data['nama_lengkap'] = 'Administrator'

    if 'kelas' in field_map:
        data['kelas'] = ''

    if 'kelamin' in field_map:
        data['kelamin'] = 'pria'

    if 'usia' in field_map:
        data['usia'] = None if field_map['usia'].null else 0

    if 'nip' in field_map:
        data['nip'] = os.environ.get('ADMIN_NIP', '000000000000000000')

    if 'is_staff' in field_map:
        data['is_staff'] = True

    if 'is_superuser' in field_map:
        data['is_superuser'] = True

    if 'is_active' in field_map:
        data['is_active'] = True

    User.objects.create(**data)


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_user_nip'),
    ]

    operations = [
        migrations.RunPython(seed_admin_user),
    ]