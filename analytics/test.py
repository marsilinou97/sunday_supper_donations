"""
Dummy tests that print the SQL they're supposed to generate instead of actually executing SQL.
main() is at the bottom
"""

TABLES_PKS = {
    "input_item":"id",
    "input_clothing":"item_id",
    "input_food":"item_id",
    "input_fund":"item_id",
    "input_giftcard":"item_id",
    "input_miscellaneous":"item_id",
    "input_donor":"id",
    "input_donation":"id"
}
def execute_delete_query(table:str, ids):
    # Get the name of the pk column for that table
    try:
        column = TABLES_PKS[table]
    except KeyError as e:
        # If the table isn't in that dictionary then complain and exit
        print(e)
        return 0

    # This tuple represents the parts of the query that are shared between all parts of this query
    body = (
        "DELETE FROM ",
        " WHERE ",
        " = %(",
        ")s;"
    )
    count = 0

    # Start building the queries
    for id in ids:
        id = str(id)

        # Concatenate the body and the table and its pk
        query = body[0] + table + body[1] + column + body[2] + column + body[3]

        # Set up the one param for the query
        # I'm pretty sure the key needs to match the column name but I could be wrong.
        params = {column:id}

        # Try/catch is mostly just to be safe
        try:
            # with connection.cursor() as cursor:
            #     cursor.execute(query,params)
            print(query)
            print(params)
            print()
            count += 1
        except:
            print("Couldn't delete")
    # probably not needed but might be useful
    print("Successfully deleted",count,"rows from",table)
    return count

def batch_delete(tables,ids):
    count = 0
    for i in range(len(tables)):
        count += execute_delete_query(tables[i],ids[i])
        print("Deleted",count,"rows from",len(tables),"tables")

def execute_update_query(table:str, id:str, columns, new_values):
    body = (
        "UPDATE ",
        " SET ",
        " WHERE ",
        " = %(",
        ")s;"
    )

    # Get the name of the pk column for this table
    pk = TABLES_PKS[table]
    i = 0 # iterator for values
    # Set up params dict
    params = {}
    params[pk] = id

    # Build UPDATE clause
    query = body[0] + table + body[1]

    # Build SET clause
    for column in columns:
        # Configure params
        params[column] = new_values[i]
        i += 1

        query = query + column + " = %(" + column + ")s"
        if column != columns[-1]:
            query = query + ", "

    # Build WHERE clause
    query = query + body[2] + pk + body[3] + pk + body[4]

    try:
        print(query)
        print(params)
        print()
        return 1
    except:
        print("Couldn't update")
        return 0

def batch_update(tables, ids, columns, new_values):
    count = 0
    for i in range(len(tables)):
        count += execute_update_query(tables[i],ids[i],columns[i],new_values[i])
    print("Updated",count,"rows")

def main():
    batch_delete(["input_item"],[["1","2","3"]])
    batch_update(["input_clothing","input_food"],["1","2"],[["type_id"],["name"]],[["Men's"],["Oranges"]])
main()
