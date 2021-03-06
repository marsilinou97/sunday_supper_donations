MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
          'December']
INDEXED_MONTHS = {'January': 0, 'February': 1, 'March': 2, 'April': 3, 'May': 4, 'June': 5, 'July': 6, 'August': 7,
                  'September': 8, 'October': 9, 'November': 10, 'December': 11}

table_headers = {
    'funds': ('first_name', 'last_name', 'date_received', 'type', 'amount', 'quantity'),
    'clothing': ('first_name', 'last_name', 'date_received', 'XXXX', 'type', 'quantity'),
    'foods': ('first_name', 'last_name', 'date_received', 'XXXX', 'name', 'quantity'),
    'giftcards': ('first_name', 'last_name', 'date_received', 'XXXX', 'business_name', 'amount', 'quantity'),
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
                       WHERE 
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
