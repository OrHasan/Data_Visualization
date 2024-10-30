import pandas as pd
# from main import my_cursor as cursor


def create_db(cursor, db_name):
    cursor.execute(f"create database {db_name}")


def create_table(cursor, table_name, columns_data, foreign_keys=None):
    if foreign_keys is None:
        foreign_keys = []
    column_strings = []

    for column in columns_data:
        column_string = f"{column['name']} {column['type']}"
        if 'extra' in column:
            column_string += f" {column['extra']}"
        column_strings.append(column_string)

    for fk in foreign_keys:
        column_strings.append(f"foreign key ({fk['column']}) references {fk['ref_table']} ({fk['ref_column']})")

    columns_string = ', '.join(column_strings)
    query = f"create table {table_name} ({columns_string})"
    cursor.execute(query)


def show_tables(cursor):
    cursor.execute("show tables")
    for x in cursor:
        print(x)


def show_table_properties(cursor, table_name, table, data):
    cursor.execute(f"describe {table_name}")

    if data == "*":
        columns = []
        for x in cursor:
            columns.append(x[0])
    else:
        columns = data.split(', ')

    pd_pulled = pd.DataFrame(table)
    pd_pulled.columns = columns
    print(pd_pulled)


def show_table_data(cursor, table_name, columns_to_read='*', return_dataframe=True):
    cursor.execute(f"select {columns_to_read} from {table_name}")
    column_names = [desc[0] for desc in cursor.description]
    table_array = cursor.fetchall()         # option 1
    # table_array = []                      # option 2
    # for _, data in enumerate(cursor):
    #     table_array.append(data)

    if return_dataframe:
        table_array = pd.DataFrame(table_array, columns=column_names)
    return table_array, column_names


def insert_values(db, cursor, table_name, values, columns_names=None, commit=True):
    if columns_names is None:
        columns_names = []
    columns_string = ' (' + {', '.join(columns_names)} + ')' if columns_names else ''

    query = f"insert into {table_name}{columns_string} values({', '.join(['%s'] * len(values[0]))})"
    cursor.executemany(query, values)

    if commit:
        db.commit()


def remove_values(db, cursor, table_name, statement, commit=True):
    cursor.execute(f"delete from {table_name} where {statement}")

    if commit:
        db.commit()


def add_column(cursor, table_name, col_name, col_type, col_extra=''):
    cursor.execute(f"alter table {table_name} add {col_name} {col_type} {col_extra}")


def remove_column(cursor, table_name, col_name):
    cursor.execute(f"alter table {table_name} drop {col_name}")


def add_index(cursor, table_name, index_name, col_name):
    cursor.execute(f"create index {index_name} ON {table_name}({col_name})")


def check_foreign_keys(cursor, table_name):
    query = f"""
    SELECT 
        TABLE_NAME,
        COLUMN_NAME,
        CONSTRAINT_NAME,
        REFERENCED_TABLE_NAME,
        REFERENCED_COLUMN_NAME
    FROM
        INFORMATION_SCHEMA.KEY_COLUMN_USAGE
    WHERE
        TABLE_NAME = '{table_name}';
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    for row in rows:
        print(f"Table: {row[0]}, Column: {row[1]}, Constraint: {row[2]}, "
              f"Referenced Table: {row[3]}, Referenced Column: {row[4]}")
