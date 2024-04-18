"""
Post model

This model represents a post with custom body content.

Attributes:
    body_custom (EditorJsJSONField): A field to store custom JSON data generated by Editor.js.
    get_absolute_url (method): A method to return the absolute URL of a post detail view.
    __str__ (method): A method to return a string representation of a post.
"""
from django.db import models
from django.urls import reverse
from django_editorjs_fields import EditorJsJSONField


class Post(models.Model):
    """
    Model representing a post.

    Attributes:
        body_custom (EditorJsJSONField): A field to store custom JSON data generated by Editor.js.
        objects (Manager): The default manager for the model.
    """
    objects = models.Manager()
    body_custom = EditorJsJSONField(
        plugins=[
            '@editorjs/paragraph',
            '@editorjs/image',
            '@editorjs/header',
            '@editorjs/list',
            '@editorjs/code',
            '@editorjs/inline-code',
            '@editorjs/embed',
            '@editorjs/link',
            '@editorjs/marker',
            '@editorjs/table',
            'header-with-alignment',
        ],
        tools={
            "Image": {
                'class': 'ImageTool',
                "config": {
                    "endpoints": {
                        "byFile": "/editorjs/image_upload/"
                    }
                }
            },
        },
        null=True,
        blank=True,
    )

    def get_absolute_url(self):
        """
        Return the absolute URL of a post detail view.

        Returns:
            str: The absolute URL of a post detail view.
        """
        return reverse('post_detail', kwargs={'pk': self.id})

    def __str__(self):
        """
        Return a string representation of a post.

        Returns:
            str: A string representation of a post.
        """
        return f'{self.id}'
