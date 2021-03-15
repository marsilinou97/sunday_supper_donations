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

"""
Update queries for auditing. Intended use case is updating one entry at a time.
You need the id of the entry to be updated, and all other values of the entry.
If you skip a value these queries will update it incorrectly.

Queries that just use %s placeholders should take the params as a list whose
elements are sorted by their order of appearance in the query. Queries that use
placeholders such as %(key)s should take the params as a dictionary where each key
corresponds to a placeholder.
See https://docs.djangoproject.com/en/3.1/topics/db/sql/#passing-parameters-into-raw
"""
update_clothing = """
UPDATE input_clothing
SET type_id = %(type_id)s
WHERE item_id = %(item_id)s;
"""

update_donation = """
UPDATE input_donation
SET date_received = %(date_received)s, thanks_sent = %(thanks_sent)s,
    comments = %(comments)s, donor_id = %(donor_id)s, user_id = %(user_id)s
WHERE id = %(id)s;
"""

update_donor = """
UPDATE input_donor
SET first_name = %(first_name)s, last_name = %(last_name)s,
    email_address = %(email_address)s, phone_number = %(phone_number)s,
    address_line1 = %(address_line1)s, address_line2 = %(address_line2)s,
    city = %(city)s, state = %(state)s, zipcode = %(zipcode)s
WHERE id = %(id)s;
"""

update_food = """
UPDATE input_food
SET name = %(name)s
WHERE item_id = %(item_id)s;
"""

update_fund = """
UPDATE input_fund
SET amount = %(amount)s, type_id = %(type_id)s
WHERE item_id = %(item_id)s;
"""

# business_name_id is simply the name of the business
update_giftcard = """
UPDATE input_giftcard
SET amount = %(amount)s, business_name_id = %(business_name_id)s
WHERE item_id = %(item_id)s;
"""

update_item = """
UPDATE input_item
SET quantity = %(quantity)s
WHERE id = %(id)s;
"""

update_miscellaneous = """
UPDATE input_miscellaneous
SET name = %(name)s
WHERE item_id = %(item_id)s;
"""

"""
Delete queries for auditing
You need at least the id of the entry to be deleted
Params should be a dictionary with key names that correspond to the placeholders
See https://docs.djangoproject.com/en/3.1/topics/db/sql/#passing-parameters-into-raw
"""
delete_clothing = """
DELETE FROM input_clothing WHERE item_id = %(item_id)s;
"""

delete_donation = """
DELETE FROM input_donation WHERE id = %(id)s;
"""

delete_donor = """
DELETE FROM input_donor WHERE id = %(id)s;
"""

delete_food = """
DELETE FROM input_food WHERE item_id = %(item_id)s;
"""

delete_fund = """
DELETE FROM input_fund WHERE item_id = %(item_id)s;
"""

delete_giftcard = """
DELETE FROM input_giftcard WHERE item_id = %(item_id)s;
"""

delete_item = """
DELETE FROM input_item WHERE id = %(id)s;
"""

delete_miscellaneous = """
DELETE FROM input_miscellaneous WHERE item_id = %(item_id)s;
"""
