from django.urls import reverse

TITLE = 'title'
TEXT = 'text'
SLUG = 'slug'

URL_HOME = reverse('notes:home')
URL_NOTES_LIST = reverse('notes:list')
URL_ADD_NOTE = reverse('notes:add')
URL_SUCCESS = reverse('notes:success')
URL_DETAIL = reverse('notes:detail', args=(SLUG,))
URL_EDIT_NOTE = reverse('notes:edit', args=(SLUG,))
URL_DELETE = reverse('notes:delete', args=(SLUG,))

URL_LOGIN = reverse('users:login')
URL_LOGOUT = reverse('users:logout')
URL_SIGNUP = reverse('users:signup')

FORM_DATA = {'title': 'Заголовок', 'text': 'Текст'}
