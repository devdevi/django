from django.db import models

class BaseModel(models.Model):
    """Meal Delivery base model.
        + created (DateTime): Store the datetime the object was created.
        + modified (DateTime): Store the last datetime the object was modified.
    """

    created = models.DateTimeField(
        'created at',
        auto_now_add=True,
        help_text='Date time on which the object was created.'
    )
    modified = models.DateTimeField(
        'modified at',
        auto_now=True,
        help_text='Date time on which the object was last modified.'
    )

    class Meta:
        """Meta option."""
        # Abstract esta no es una tabla de la base de datos

        abstract = True

        get_latest_by = 'created'
        ordering = ['-created', '-modified']


