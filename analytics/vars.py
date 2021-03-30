from django.db.models import F
from django.db.models import Value
from django.db.models import NullBooleanField
from django.db.models import IntegerField
from django.db.models import CharField
from input.models import *

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
          'December']
INDEXED_MONTHS = {'January': 0, 'February': 1, 'March': 2, 'April': 3, 'May': 4, 'June': 5, 'July': 6, 'August': 7,
                  'September': 8, 'October': 9, 'November': 10, 'December': 11}

table_headers = {
    'funds': ('first_name', 'last_name', 'date_received', 'type', 'amount', 'quantity'),
    'clothing': ('first_name', 'last_name', 'date_received', 'XXXX', 'type', 'quantity'),
    'foods': ('first_name', 'last_name', 'date_received', 'XXXX', 'name', 'quantity'),
    'giftcards': ('first_name', 'last_name', 'date_received', 'business_name', 'XXXX', 'amount', 'quantity'),
    'miscellaneous': ('first_name', 'last_name', 'date_received', 'XXXX', 'misc_name', 'quantity')}


RAW_DATA_BASE_FIELDS_KEYS = {
        "first_name": F('item__donation__donor__first_name'),
        "last_name": F('item__donation__donor__last_name'),
        "date_received": F('item__donation__date_received'),
        "quantity": F('item__quantity')
}

RAW_DATA_BASE_FIELDS = [
       'first_name',
       'last_name',
       'date_received',
]

FUNDS_RAW_DATA_FIELDS = {
       "item_type": Value('Fund', output_field=CharField()),
       "id": F('type_id'),
       "amt": F('amount')
}

GIFTCARD_RAW_DATA_FIELDS = {
       "item_type": Value('Giftcard', output_field=CharField()),
       "id": F('business_name_id'),
       "amt": F('amount')
}

CLOTHING_RAW_DATA_FIELDS = {
       "item_type": Value('Clothing', output_field=CharField()),
       "id": Value(None, output_field=IntegerField()),
       "typ_id": F('type_id'),
}

FOODS_RAW_DATA_FIELDS = {
       "item_type": Value('Food', output_field=CharField()),
       "id": Value(None, output_field=IntegerField()),
       "namee": F("name")
}

MISC_RAW_DATA_FIELDS = {
       "item_type": Value('Misc', output_field=CharField()),
       "id": Value(None, output_field=IntegerField()),
       "namee": F("name")
}

QUERY_DATA = {
       "funds_table" : {
              "RAW_DATA_FIELDS": FUNDS_RAW_DATA_FIELDS,
              "MODEL": Fund
       },
       "giftcards_table" : {
              "RAW_DATA_FIELDS": GIFTCARD_RAW_DATA_FIELDS,
              "MODEL": GiftCard
       },
       "clothing_table" : {
              "RAW_DATA_FIELDS": CLOTHING_RAW_DATA_FIELDS,
              "MODEL": Clothing
       },
       "foods_table" : {
              "RAW_DATA_FIELDS": FOODS_RAW_DATA_FIELDS,
              "MODEL": Food
       },
       "misc_table" : {
              "RAW_DATA_FIELDS": MISC_RAW_DATA_FIELDS,
              "MODEL": Miscellaneous
       }
}
