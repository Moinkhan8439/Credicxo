from rest_framework import permissions



#Here we check if the user is present in request then if he is authenticated or not and at last if he is a teacher or not. 
class IsTeacher(permissions.BasePermission):

    """
    Allows access only to teachers.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and  request.user.is_teacher)



class IsStudent(permissions.BasePermission):

    """
    Allows access only to teachers.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and not request.user.is_teacher)




class IsTeacherOrAdmin(permissions.BasePermission):

    """
    Allows access only to teachers.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and  request.user.is_teacher or request.user.is_staff )