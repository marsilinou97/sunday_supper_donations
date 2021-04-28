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

TABLE_HEADERS_FORMATTED = {
       'first_name' : 'First Name',
       'last_name': 'Last Name',
       'date_received': 'Date Received',
       'sub_type': 'Sub Type',
       'amount': 'Amount',
       'quantity': 'Quantity',
       'id' : 'ID',
       'comments': 'Comments',
       'item_id': 'Item ID',
       'donor_id': 'Donor ID',
       'donation_id': 'Donation ID',
       'item_type': 'Item Type'
}

TABLE_NAMES_FORMATTED = {
}


RAW_DATA_BASE_FIELDS_KEYS = {
       "donation_id": F("item__donation__id"),
       "first_name": F('item__donation__donor__first_name'),
       "last_name": F('item__donation__donor__last_name'),
       "date_received": F('item__donation__date_received'),
       "quantity": F('item__quantity'),
       "comments": F('item__donation__comments'),
       'donor_id': F('item__donation__donor__id'),
       'thanks_sent': F('item__donation__thanks_sent')
}

RAW_DATA_BASE_FIELDS = [
       'donation_id',
       'first_name',
       'last_name',
       'date_received',
       'thanks_sent',
       'quantity',
       'comments',
       'item_id',
       'donor_id'
]

FUNDS_RAW_DATA_FIELDS = {
       "item_type": Value('Fund', output_field=CharField()),
       "amount": 1,
       'item_id': 1,
       "sub_type": F('type')
}

GIFTCARD_RAW_DATA_FIELDS = {
       "item_type": Value('Giftcard', output_field=CharField()),
       "amount": 1,
       "sub_type": F('business_name'),
       'item_id': 1,
}

CLOTHING_RAW_DATA_FIELDS = {
       "item_type": Value('Clothing', output_field=CharField()),
       "sub_type": F('type'),
       'item_id': 1,
}

FOODS_RAW_DATA_FIELDS = {
       "item_type": Value('Food', output_field=CharField()),
       "sub_type" : F('name'),
       'item_id': 1,
}

MISC_RAW_DATA_FIELDS = {
       "item_type": Value('Misc', output_field=CharField()),
       "sub_type" : F('name'),
       'item_id': 1,
}

QUERY_DATA = {
       "funds_table" : {
              "RAW_DATA_FIELDS": FUNDS_RAW_DATA_FIELDS,
              "MODEL": Fund,
              "SUBTYPE_FIELD": 'type'
       },
       "giftcards_table" : {
              "RAW_DATA_FIELDS": GIFTCARD_RAW_DATA_FIELDS,
              "MODEL": GiftCard,
              "SUBTYPE_FIELD": 'business_name'
       },
       "clothing_table" : {
              "RAW_DATA_FIELDS": CLOTHING_RAW_DATA_FIELDS,
              "MODEL": Clothing,
              "SUBTYPE_FIELD": 'type'
       },
       "foods_table" : {
              "RAW_DATA_FIELDS": FOODS_RAW_DATA_FIELDS,
              "MODEL": Food,
              "SUBTYPE_FIELD": 'name'
       },
       "misc_table" : {
              "RAW_DATA_FIELDS": MISC_RAW_DATA_FIELDS,
              "MODEL": Miscellaneous,
              "SUBTYPE_FIELD": 'name'
       }
}
