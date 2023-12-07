from typing import Dict, Any, List

from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.template import Context

from menu.application.models import MenuItem

register = template.Library()


@register.inclusion_tag('menu.html', takes_context=True)
def draw_menu(context: Context, menu: str) -> Dict[str, Any]:
    """
    Template tag для создания древовидного меню.
    """

    try:
        # Получаем все подменю для определенного меню
        items = MenuItem.objects.filter(menu__title=menu)
        items_values = items.values()

        # Получаем начальное меню, у которого нет поля parent
        root_item = [item for item in items_values.filter(parent=None)]

        # Получаем id выбранного меню
        selected_item_id = int(context['request'].GET[menu])
        selected_item = items.get(id=selected_item_id)

        # Получаем список id подменю для выбранного меню
        selected_item_id_list = get_selected_item_id_list(selected_item, root_item, selected_item_id)

        # Добавляем унаследованные подменю для каждого подменю
        for item in root_item:
            if item['id'] in selected_item_id_list:
                item['child_items'] = get_child_items(items_values, item['id'], selected_item_id_list)

        result_dict = {'items': root_item}

    except (KeyError, ObjectDoesNotExist):
        # возвращаем подменю без поля parent
        result_dict = {
            'items': [
                item for item in MenuItem.objects.filter(menu__title=menu, parent=None).values()
            ]
        }

    # Добавляем имя меню в словарь
    result_dict['menu'] = menu
    result_dict['other_querystring'] = build_querystring(context, menu)

    return result_dict


def build_querystring(context: Context, menu: str) -> str:
    """
    Формируем данные для добавления
    :param context: The current context.
    :param menu: The menu.
    :return: The built query string.
    """

    querystring_args = []

    for key in context['request'].GET:
        if key != menu:
            querystring_args.append(f"{key}={context['request'].GET[key]}")

    querystring = '&'.join(querystring_args)

    return querystring


def get_child_items(items_values, current_item_id, selected_item_id_list):
    """
    Формируем список всех подменю для определенного меню
    """
    item_list = [item for item in items_values.filter(parent_id=current_item_id)]
    for item in item_list:
        if item['id'] in selected_item_id_list:
            item['child_items'] = get_child_items(items_values, item['id'], selected_item_id_list)
    return item_list


def get_selected_item_id_list(parent: MenuItem, primary_item: List[MenuItem], selected_item_id: int) -> List[int]:
    """
    Формируем список id для выбранного подменю от родительского до текущего.

    """

    selected_item_id_list = []

    while parent:
        selected_item_id_list.append(parent.id)
        parent = parent.parent
    if not selected_item_id_list:
        for item in primary_item:
            if item.id == selected_item_id:
                selected_item_id_list.append(selected_item_id)
    return selected_item_id_list
