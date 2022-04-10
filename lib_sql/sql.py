from tables_sql import TablesSQL
from sql_config import db

# Open connection with DB
cursor = db.cursor()

# Object of TableSQL class
tables = TablesSQL(cursor)

# Crate tables columns configurations
users_columns = """
id INT PRIMARY KEY AUTO_INCREMENT NOT NULL, 
name VARCHAR(50) NOT NULL, phone INT NOT NULL, 
tg_user_id INT NOT NULL
"""

category_columns = """
id INT PRIMARY KEY AUTO_INCREMENT NOT NULL, 
name VARCHAR(255) NOT NULL, url VARCHAR(255) NOT NULL
"""

products_columns = """
id INT PRIMARY KEY AUTO_INCREMENT NOT NULL, 
name VARCHAR(255) NOT NULL, price FLOAT NOT NULL,
category_id INT, FOREIGN KEY (category_id) REFERENCES category(id),
image_url VARCHAR(255) NOT NULL, amount INT DEFAULT 100
"""

cart_columns = """
id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
user_id INT, FOREIGN KEY (user_id) REFERENCES users(id),
products_id INT, FOREIGN KEY (products_id) REFERENCES products(id)
"""

issued_order_columns = """
id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
user_id INT, FOREIGN KEY (user_id) REFERENCES users(id),
products_id INT, FOREIGN KEY (products_id) REFERENCES products(id),
address VARCHAR(255), date DATETIME
"""


# For creating new tables
tables.create_new_table('users', users_columns)
tables.create_new_table('category', category_columns)
tables.create_new_table('products', products_columns)
tables.create_new_table('cart', cart_columns)
tables.create_new_table('issued_order', issued_order_columns)

# For drop all tables
# tables.drop_table('issued_order')
# tables.drop_table('cart')
# tables.drop_table('products')
# tables.drop_table('category')
# tables.drop_table('users')

# Debug
print(tables.get_all_tables())

# Close connection with DB
cursor.close()
