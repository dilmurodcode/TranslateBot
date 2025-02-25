import sqlite3

class Database:
    conn = sqlite3.connect("sqlite.db")
    cursor = conn.cursor()

    def create_table(self, name:str, fields:dict) -> str:
        """
        this function for create table database for example:
        create_table("users", {"name": "TEXT", "age": "INTEGER", "email": "TEXT"})
        """
        fields["created_at"] = "TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL"
        columns = ", ".join([f"{col} {dtype}" for col, dtype in fields.items()])

        query = f"""
            CREATE TABLE IF NOT EXISTS {name}(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                {columns}
            )
            """
        self.cursor.execute(query)
        return "Created table"

    def get_table_fields(self, table_name: str) -> dict:
        """Get table fields as a dictionary {column_name: data_type}"""
        try:
            query = f"PRAGMA table_info({table_name})"
            self.cursor.execute(query)
            columns = self.cursor.fetchall()

            if not columns:
                return {"error": f"Table '{table_name}' does not exist!"}

            fields = {col[1]: col[2] for col in columns if col[1] != "id"}
            return fields

        except sqlite3.Error as e:
            return {"error": str(e)}

    def create(self, table_name: str, values: dict) -> str:
        """
        Insert data into the specified table.
        Example:
        db.create("users", {"name": "Alice", "age": 25, "email": "alice@example.com"})
        """
        fields = self.get_table_fields(table_name)

        if "error" in fields:
            return fields['error']

        if not all(key in fields for key in values.keys()):
            return "Error: Some fields are missing or incorrect!"

        columns = ", ".join(values.keys())
        placeholders = ", ".join(["?" for _ in values])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        try:
            self.cursor.execute(query, tuple(values.values()))
            self.conn.commit()
            return "Inserted successfully"
        except sqlite3.Error as e:
            return f"Error: {e}"

    def get(self, table_name: str, table_values: dict = None):

        """
        get data from table for example:
        .get("users", {"age": 25}) for filter , if you give only table name it return all objects without filter
        """

        fields = self.get_table_fields(table_name)

        if "error" in fields:
            return fields["error"]

        query = f"SELECT * FROM {table_name}"
        values = []

        if table_values:
            condition_str = " AND ".join([f"{key} = ?" for key in table_values.keys()])
            query += f" WHERE {condition_str}"
            values = list(table_values.values())

        try:
            self.cursor.execute(query, values)
            results = self.cursor.fetchall()
            return results if results else None
        except sqlite3.Error as e:
            return f"Error: {e}"

    def get_or_create(self):
        ...



db = Database()






