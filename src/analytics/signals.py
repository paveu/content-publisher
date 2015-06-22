from django.dispatch import Signal

# notify = Signal(providing_args=['sender','recipient', 'verb', 'action', 'target'])
page_view = Signal(providing_args=['page_path',
                                   'primary_obj',
                                   'secondary_obj']
                   )
