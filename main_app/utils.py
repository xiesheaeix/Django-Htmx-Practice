from django.db.models import Max
from main_app.models import UserTodos


def get_max_order(user) -> int:
    existing_todos = UserTodos.objects.filter(user=user)
    if not existing_todos.exists():
        return 1
    else:
        current_max = existing_todos.aggregate(max_order=Max('order'))['max_order']
        return current_max + 1


def reorder(user):
    existing_todos = UserTodos.objects.filter(user=user)
    if not existing_todos.exists():
        return
    number_of_todos = existing_todos.count()
    new_ordering = range(1, number_of_todos+1)

    for order, user_todo in zip(new_ordering, existing_todos):
        user_todo.order = order
        user_todo.save()
