from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    """Доступ только для администратора."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )


class IsAdminOrReadOnly(IsAdmin):
    """Чтение доступно всем, изменение — только администратору."""

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or super().has_permission(request, view)
        )


class IsAuthorModeratorAdminOrReadOnly(BasePermission):
    """
    Чтение доступно всем.
    Изменение/удаление — автору, модератору или администратору.
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )
