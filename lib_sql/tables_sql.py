class TablesSQL():

    def __init__(self, cursor):
        self.cursor = cursor

# Tables interaction

    def get_all_tables(self):
        query = f"""
        SHOW TABLES; 
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def create_new_table(self, table_name, columns):
        query = f"""
        CREATE TABLE if not exists {table_name}({columns});
        """
        self.cursor.execute(query)

    def drop_table(self, table_name):
        query = f"""
        DROP TABLE {table_name};
        """
        self.cursor.execute(query)
# End tables interaction

# Content interaction

    def add_new_content(self, table_name, columns, values):
        query = f"""
        INSERT INTO {table_name} ({columns}) VALUES ({values});
        """
        self.cursor.execute(query)

    def get_content(self, table_name, content_id):
        query = f"""
        SELECT * FROM {table_name} WHERE id={content_id};
        """
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def get_definite_content(self, get_column, table_name, compare_column, value ):
        query = f"""
        SELECT {get_column} FROM {table_name} WHERE {compare_column}='{value}';
        """
        self.cursor.execute(query)
        return self.cursor.fetchone()


    def get_all_content(self, table_name):
        query = f"""
        SELECT * FROM {table_name};
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def delete_content(self, table_name, content_id):
        query = f"""
        DELETE FROM {table_name} WHERE id={content_id};
        """
        self.cursor.execute(query)

    def update_content(self, table_name, column, value, content_id):
        query = f"""
        UPDATE {table_name} SET {column}='{value}' WHERE id={content_id}; 
        """
        self.cursor.execute(query)


# End content interaction
