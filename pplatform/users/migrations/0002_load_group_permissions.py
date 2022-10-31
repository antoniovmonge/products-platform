from django.db import migrations


def main_cmd(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")

    content_type_product = ContentType.objects.get_for_model(
        apps.get_model("catalog", "Product")
    )
    content_type_content = ContentType.objects.get_for_model(
        apps.get_model("catalog", "Content")
    )
    content_type_file = ContentType.objects.get_for_model(
        apps.get_model("catalog", "File")
    )
    content_type_image = ContentType.objects.get_for_model(
        apps.get_model("catalog", "Image")
    )
    content_type_text = ContentType.objects.get_for_model(
        apps.get_model("catalog", "Text")
    )
    
    # CREATE PERMISSIONS
    # Product
    add_product, _ = Permission.objects.get_or_create(
        codename="add_product", name="Can add product", content_type=content_type_product
    )
    change_product, _ = Permission.objects.get_or_create(
        codename="change_product",
        name="Can change product",
        content_type=content_type_product,
    )
    delete_product, _ = Permission.objects.get_or_create(
        codename="delete_product",
        name="Can delete product",
        content_type=content_type_product,
    )
    view_product, _ = Permission.objects.get_or_create(
        codename="view_product", name="Can view product", content_type=content_type_product
    )
    # Content
    add_content, _ = Permission.objects.get_or_create(
        codename="add_content",
        name="Can add content",
        content_type=content_type_content,
    )
    change_content, _ = Permission.objects.get_or_create(
        codename="change_content",
        name="Can change content",
        content_type=content_type_content,
    )
    delete_content, _ = Permission.objects.get_or_create(
        codename="delete_content",
        name="Can delete content",
        content_type=content_type_content,
    )
    view_content, _ = Permission.objects.get_or_create(
        codename="view_content",
        name="Can view content",
        content_type=content_type_content,
    )
    # File
    add_file, _ = Permission.objects.get_or_create(
        codename="add_file", name="Can add file", content_type=content_type_file
    )
    change_file, _ = Permission.objects.get_or_create(
        codename="change_file", name="Can change file", content_type=content_type_file
    )
    delete_file, _ = Permission.objects.get_or_create(
        codename="delete_file", name="Can delete file", content_type=content_type_file
    )
    view_file, _ = Permission.objects.get_or_create(
        codename="view_file", name="Can view file", content_type=content_type_file
    )
    # Image
    add_image, _ = Permission.objects.get_or_create(
        codename="add_image", name="Can add image", content_type=content_type_image
    )
    change_image, _ = Permission.objects.get_or_create(
        codename="change_image",
        name="Can change image",
        content_type=content_type_image,
    )
    delete_image, _ = Permission.objects.get_or_create(
        codename="delete_image",
        name="Can delete image",
        content_type=content_type_image,
    )
    view_image, _ = Permission.objects.get_or_create(
        codename="view_image", name="Can view image", content_type=content_type_image
    )
    # Text
    add_text, _ = Permission.objects.get_or_create(
        codename="add_text", name="Can add text", content_type=content_type_text
    )
    change_text, _ = Permission.objects.get_or_create(
        codename="change_text", name="Can change text", content_type=content_type_text
    )
    delete_text, _ = Permission.objects.get_or_create(
        codename="delete_text", name="Can delete text", content_type=content_type_text
    )
    view_text, _ = Permission.objects.get_or_create(
        codename="view_text", name="Can view text", content_type=content_type_text
    )
    
    # CREATE GROUPS WITH PERMISSIONS
    GROUPS_PERMISSIONS = {
        "company_admin": [
            add_product,
            change_product,
            delete_product,
            view_product,
            add_content,
            change_content,
            delete_content,
            view_content,
            add_file,
            change_file,
            delete_file,
            view_file,
            add_image,
            change_image,
            delete_image,
            view_image,
            add_text,
            change_text,
            delete_text,
            view_text,
        ]
    }
    
    # Add permissions to groups
    for group_name, permissions in GROUPS_PERMISSIONS.items():
        group, created = Group.objects.get_or_create(name=group_name)
        for perm in permissions:
            group.permissions.add(perm)


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(main_cmd, reverse_code=migrations.RunPython.noop)
    ]
