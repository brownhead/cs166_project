import flask
from mnet.application import app, db
from flask.ext.login import current_user, login_required
import mnet.auth as auth
from mnet.models.shoppingcart import ShoppingCart

@app.route("/cart", methods = ["GET", "POST"])
@login_required
def cart():
    model = ShoppingCart(current_user.get_id())
    videos = model.get_items()

    if videos:
        db.execute(
            "SELECT title,dvd_price FROM video WHERE video_id IN (%s)" %
            (",".join(str(i) for i in videos), )
        )
        videos_info = db.fetchall()
    else:
        videos_info = []

    items = []
    for video_id, video_info in zip(videos, videos_info):
        items.append({
            "video_id": video_id,
            "title": video_info[0],
            "dvd_price": video_info[1]
        })

    app.logger.debug("Query returned\n%s", repr(items))

    if flask.request.method == "POST":
        action = flask.request.form.get("action")

        app.logger.info("Cart action %s triggered.", action)

        if action == "checkout":
            db.execute("SELECT balance FROM users WHERE user_id=%s", (current_user.get_id(), ))
            balance = int(db.fetchone()[0])

            price_sum = sum(i["dvd_price"] for i in items)

            if price_sum > balance:
                flask.flash("You don't have enough money in your account.", category = "error")
            else:
                db.execute('UPDATE users SET balance = balance - %s WHERE user_id = %s', (price_sum, current_user.get_id()))
                model.complete_order()
                flask.flash("Your order has been placed!", category = "message")

            return flask.redirect(flask.url_for("cart"))
        elif action == "clear":
            model.clear_cart()
            flask.flash("Cart has been cleared.", category = "message")
            return flask.redirect(flask.url_for("cart"))

    return flask.render_template("cart.html", items = items)
