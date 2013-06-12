from mnet.application import app, db

class ShoppingCart:
    def __init__(self, user_id):
        db.execute(
            "SELECT (order_id) FROM ordersmeta WHERE completed IS NULL AND user_id=%s",
            (user_id, )
        )
        result = db.fetchone()

        self.user_id = user_id

        if result is None:
            self.order_id = None
        else:
            self.order_id = result[0]

    def _create_order(self):
        if self.order_id is not None:
            return

        app.logger.info("Creating new order with user_id: %s", self.user_id)

        db.execute(
            "INSERT INTO ordersmeta (user_id,completed) VALUES (%s, NULL)",
            (self.user_id, )
        )

    def add_item(self, video_id):
        self._create_order()

        db.execute(
            "INSERT INTO orders (order_id, video_id) VALUES (%s, %s)",
            (self.order_id, video_id)
        )

    def get_items(self):
        self._create_order()

        db.execute(
            "SELECT video_id FROM orders WHERE order_id=%s",
            (self.order_id, )
        )

        return [i[0] for i in db.fetchall()]
