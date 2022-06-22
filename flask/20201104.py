import flask

p1 = flask.Flask("test", template_folder="C:/Users/User/PycharmProjects/python3.7/")
x = 0


@p1.route("/", methods=["GET", 'POST'])
def home():
    global x
    x += 1
    return flask.render_template("20201104.html", x=x)


@p1.route("/about", methods=["GET", "POST"], defaults={"page": 1})
@p1.route("/about/<int:page>", methods=["GET", "POST"])
def about(page):
    return "PAGE=" + str(page)


@p1.route("/images", methods=["GET"], defaults={"filename": ""})
@p1.route("/images/<string:filename>", methods=["GET"])
def file(filename):
    return flask.send_from_directory(
        "C:/Users/User/PycharmProjects/python3.7/images/",
        filename,
        as_attachment=False
    )

p1.run(
    host="localhost",
    port=80
)
