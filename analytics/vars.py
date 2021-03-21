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

raw_data_query = """
        (SELECT 'funds', first_name, last_name, date_received, type_id AS id, amount, quantity
         FROM input_item ii
                  INNER JOIN input_fund i ON ii.id = i.item_id
                  INNER JOIN input_donation d ON ii.donation_id = d.id
                  INNER JOIN input_donor id2 ON d.donor_id = id2.id
         LIMIT 25)
        UNION ALL
        (SELECT 'giftcards', first_name, last_name, date_received, business_name_id AS id, amount, quantity
         FROM input_item ii
                  INNER JOIN input_giftcard i ON ii.id = i.item_id
                  INNER JOIN input_donation d ON ii.donation_id = d.id
                  INNER JOIN input_donor id2 ON d.donor_id = id2.id
         LIMIT 25)
        UNION ALL
        (SELECT 'clothing', first_name, last_name, date_received, NULL AS id, type_id, quantity
         FROM input_item ii
                  INNER JOIN input_clothing i ON ii.id = i.item_id
                  INNER JOIN input_donation d ON ii.donation_id = d.id
                  INNER JOIN input_donor id2 ON d.donor_id = id2.id
         LIMIT 25)
        UNION ALL
        (SELECT 'foods', first_name, last_name, date_received, NULL AS id, i.name, quantity
         FROM input_item ii
                  INNER JOIN input_food i ON ii.id = i.item_id
                  INNER JOIN input_donation d ON ii.donation_id = d.id
                  INNER JOIN input_donor id2 ON d.donor_id = id2.id
         LIMIT 25)
        UNION ALL
        (SELECT 'miscellaneous', first_name, last_name, date_received, NULL AS id, i.name, quantity
         FROM input_item ii
                  INNER JOIN input_miscellaneous i ON ii.id = i.item_id
                  INNER JOIN input_donation d ON ii.donation_id = d.id
                  INNER JOIN input_donor id2 ON d.donor_id = id2.id
         LIMIT 25);
        """
raw_data_query2 = """SELECT 'funds',ii.id, first_name, last_name, date_received, type_id AS id, amount, quantity
         FROM input_item ii
                  INNER JOIN input_fund i ON ii.id = i.item_id
                  INNER JOIN input_donation d ON ii.donation_id = d.id
                  INNER JOIN input_donor id2 ON d.donor_id = id2.id
         LIMIT 25"""
filter_query = """
            SELECT *
            FROM (
                     (SELECT 'funds', first_name, last_name, date_received, type_id AS id, amount, quantity
                      FROM input_item ii
                               INNER JOIN input_fund i
                                          ON ii.id = i.item_id
                               INNER JOIN input_donation d ON ii.donation_id = d.id
                               INNER JOIN input_donor id2 ON d.donor_id = id2.id
                      LIMIT 25)
                     UNION ALL
            
                     (SELECT 'giftcards', first_name, last_name, date_received, business_name_id AS id, amount, quantity
                      FROM input_item ii
                               INNER JOIN input_giftcard i
                                          ON ii.id = i.item_id
                               INNER JOIN input_donation d ON ii.donation_id = d.id
                               INNER JOIN input_donor id2 ON d.donor_id = id2.id
                      LIMIT 25)
                     UNION ALL
            
                     (SELECT 'clothing', first_name, last_name, date_received, '' AS id, type_id, quantity
                      FROM input_item ii
                               INNER JOIN input_clothing i
                                          ON ii.id = i.item_id
                               INNER JOIN input_donation d ON ii.donation_id = d.id
                               INNER JOIN input_donor id2 ON d.donor_id = id2.id
            
                      LIMIT 25)
                     UNION ALL
            
                     (SELECT 'foods', first_name, last_name, date_received, '' AS id, i.name, quantity
                      FROM input_item ii
                               INNER JOIN input_food i
                                          ON ii.id = i.item_id
                               INNER JOIN input_donation d ON ii.donation_id = d.id
                               INNER JOIN input_donor id2 ON d.donor_id = id2.id
                      LIMIT 25)
                     UNION ALL
            
                     (SELECT 'miscellaneous', first_name, last_name, date_received, '' AS id, i.name, quantity
                      FROM input_item ii
                               INNER JOIN input_miscellaneous i
                                          ON ii.id = i.item_id
                               INNER JOIN input_donation d ON ii.donation_id = d.id
                               INNER JOIN input_donor id2 ON d.donor_id = id2.id
                      LIMIT 25)) results
        """

pie_chart_query = """
        SELECT 'funds', sum(quantity)
        FROM input_item ii
                 INNER JOIN input_fund i
                            ON ii.id = i.item_id
        UNION
        SELECT 'giftcards', sum(quantity)
        FROM input_item ii
                 INNER JOIN input_giftcard i
                            ON ii.id = i.item_id
        UNION
        SELECT 'clothing', sum(quantity)
        FROM input_item ii
                 INNER JOIN input_clothing i
                            ON ii.id = i.item_id
        UNION
        SELECT 'food', sum(quantity)
        FROM input_item ii
                 INNER JOIN input_food i
                            ON ii.id = i.item_id
        UNION ALL
        SELECT 'misc', sum(quantity)
        FROM input_item ii
                 INNER JOIN input_miscellaneous i
                            ON ii.id = i.item_id;
        """

stacked_lines_by_month_query = """
                                    SELECT 'funds', to_char(date_received, 'Month') AS monnth, count(*) number_of_donations, sum(quantity) AS quantity
                                    FROM input_fund f
                                             INNER JOIN input_item ii ON f.item_id = ii.id
                                             INNER JOIN input_donation i ON ii.donation_id = i.id
                                    GROUP BY monnth
                                    
                                    
                                    UNION ALL
                                    
                                    SELECT 'food', to_char(date_received, 'Month') AS monnth, count(*) number_of_donations, sum(quantity) AS quantity
                                    FROM input_food f
                                             INNER JOIN input_item ii ON f.item_id = ii.id
                                             INNER JOIN input_donation i ON ii.donation_id = i.id
                                    GROUP BY monnth
                                    
                                    UNION ALL
                                    
                                    SELECT 'miscellaneous',
                                           to_char(date_received, 'Month') AS monnth,
                                           count(*)                           number_of_donations,
                                           sum(quantity)                   AS quantity
                                    FROM input_miscellaneous f
                                             INNER JOIN input_item ii ON f.item_id = ii.id
                                             INNER JOIN input_donation i ON ii.donation_id = i.id
                                    GROUP BY monnth
                                    
                                    UNION ALL
                                    
                                    SELECT 'clothing',
                                           to_char(date_received, 'Month') AS monnth,
                                           count(*)                           number_of_donations,
                                           sum(quantity)                   AS quantity
                                    FROM input_clothing f
                                             INNER JOIN input_item ii ON f.item_id = ii.id
                                             INNER JOIN input_donation i ON ii.donation_id = i.id
                                    GROUP BY monnth
                                    
                                    UNION ALL
                                    
                                    SELECT 'giftcards',
                                           to_char(date_received, 'Month') AS monnth,
                                           count(*)                           number_of_donations,
                                           sum(quantity)                   AS quantity
                                    FROM input_giftcard f
                                             INNER JOIN input_item ii ON f.item_id = ii.id
                                             INNER JOIN input_donation i ON ii.donation_id = i.id
                                    GROUP BY monnth
"""

lines_charts_query = """
                        SELECT 'funds', to_char(date_received, 'Month') AS monnth, count(*) number_of_donations, sum(quantity) AS quantity
                        FROM input_fund f
                                 INNER JOIN input_item ii ON f.item_id = ii.id
                                 INNER JOIN input_donation i ON ii.donation_id = i.id
                        GROUP BY monnth
                        UNION ALL
                        SELECT 'food', to_char(date_received, 'Month') AS monnth, count(*) number_of_donations, sum(quantity) AS quantity
                        FROM input_food f
                                 INNER JOIN input_item ii ON f.item_id = ii.id
                                 INNER JOIN input_donation i ON ii.donation_id = i.id
                        GROUP BY monnth
                        UNION ALL
                        SELECT 'miscellaneous',
                               to_char(date_received, 'Month') AS monnth,
                               count(*)                           number_of_donations,
                               sum(quantity)                   AS quantity
                        FROM input_miscellaneous f
                                 INNER JOIN input_item ii ON f.item_id = ii.id
                                 INNER JOIN input_donation i ON ii.donation_id = i.id
                        GROUP BY monnth
                        UNION ALL
                        SELECT 'clothing',
                               to_char(date_received, 'Month') AS monnth,
                               count(*)                           number_of_donations,
                               sum(quantity)                   AS quantity
                        FROM input_clothing f
                                 INNER JOIN input_item ii ON f.item_id = ii.id
                                 INNER JOIN input_donation i ON ii.donation_id = i.id
                        GROUP BY monnth
                        UNION ALL
                        SELECT 'gifcards',
                               to_char(date_received, 'Month') AS monnth,
                               count(*)                           number_of_donations,
                               sum(quantity)                   AS quantity
                        FROM input_giftcard f
                                 INNER JOIN input_item ii ON f.item_id = ii.id
                                 INNER JOIN input_donation i ON ii.donation_id = i.id
                        GROUP BY monnth
                        ORDER BY 1

"""

'''
Queries retrieve necessary data to display all chart data unfiltered
'''

# Get all fund chart data
fund_chart_query = """
SELECT amount, date_received
FROM input_donor d
INNER JOIN input_donation dn
ON d.id = dn.donor_id
INNER JOIN input_item it
ON dn.id = it.donation_id
INNER JOIN input_fund f
ON it.id = f.item_id;
"""


# Get all giftcard chart data
giftcard_chart_query = """
SELECT amount, date_received
FROM input_donor d
INNER join input_donation dn
ON d.id = dn.donor_id
INNER JOIN input_item it
ON dn.id = it.donation_id
INNER JOIN input_giftcard g
ON it.id = g.item_id;
"""

# Get all clothing chart data
clothing_chart_query = """
SELECT quantity, date_received
FROM input_donor d
INNER JOIN input_donation dn
ON d.id = dn.donor_id
INNER JOIN input_item it
ON dn.id = it.donation_id
INNER JOIN input_clothing c
ON it.id = c.item_id;
"""

# Get all food chart data
food_chart_query = """
SELECT quantity, date_received
FROM input_donor d
INNER JOIN input_donation dn
ON d.id = dn.donor_id
INNER JOIN input_item it
ON dn.id = it.donation_id
INNER JOIN input_food f
ON it.id = f.item_id;
"""

# Get all miscellaneous chart data
miscellaneous_chart_query = """
SELECT quantity, date_received
FROM input_donor d
INNER JOIN input_donation dn
on d.id = dn.donor_id
INNER JOIN input_item it
ON dn.id = it.donation_id
INNER JOIN input_miscellaneous m
ON it.id = m.item_id;
"""

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

RAW_DATA_QUERIES = {
       "funds_table" : {
              "FIELDS": FUNDS_RAW_DATA_FIELDS,
              "MODEL": Fund
       },
       "giftcards_table" : {
              "FIELDS": GIFTCARD_RAW_DATA_FIELDS,
              "MODEL": GiftCard
       },
       "cloithing_table" : {
              "FIELDS": CLOTHING_RAW_DATA_FIELDS,
              "MODEL": Clothing
       },
       "foods_table" : {
              "FIELDS": FOODS_RAW_DATA_FIELDS,
              "MODEL": Food
       },
       "misc_table" : {
              "FIELDS": MISC_RAW_DATA_FIELDS,
              "MODEL": Miscellaneous
       }
}
