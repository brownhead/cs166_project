import flask
from mnet.application import app, db
from flask.ext.login import current_user, login_required
import mnet.auth as auth
from mnet.models.shoppingcart import ShoppingCart

@app.route("/cart")
@login_required
def cart():
    model = ShoppingCart(current_user.get_id())
    videos = model.get_items()

    db.execute(
        "SELECT title,dvd_price FROM video WHERE video_id IN (%s)" %
        (",".join(str(i) for i in videos), )
    )
    videos_info = db.fetchall()
    app.logger.debug("%s", ",".join(str(i) for i in videos))

    items = []
    for video_id, video_info in zip(videos, videos_info):
        items.append({
            "video_id": video_id,
            "title": video_info[0],
            "dvd_price": video_info[1]
        })

    app.logger.debug("Query returned\n%s", repr(items))

    return flask.render_template("cart.html", items = items)
