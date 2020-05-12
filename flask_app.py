import json
import jinja2
import yaml
from jinja2 import Environment
from flask import Flask, render_template, request, Response, url_for, jsonify

app = Flask(__name__, static_url_path="/static")

MAP_UNDEFINED = {
    "jinja2.Undefined": jinja2.Undefined,
    "jinja2.ChainableUndefined": jinja2.ChainableUndefined,
    "jinja2.DebugUndefined": jinja2.DebugUndefined,
    "jinja2.StrictUndefined": jinja2.StrictUndefined,
}

NEWLINE_SEQUENCES = ["\r", "\n", "\r\n"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/demo")
def demo():
    return render_template("demo.html")


@app.route("/rend", methods=["POST"])
def rend():
    data = request.get_json()
    print(data)
    trim_blocks = bool(data.get("trim_blocks"))
    lstrip_blocks = bool(data.get("lstrip_blocks"))
    keep_trailing_newline = bool(data.get("keep_trailing_newline"))
    newline_sequence = data.get("newline_sequence", "\n")
    if newline_sequence not in NEWLINE_SEQUENCES:
        newline_sequence = "\n"
    extenstions = data.get("extensions", [])
    extenstions = [extenstions] if isinstance(extenstions, str) else extenstions
    undefined = MAP_UNDEFINED.get(data.get("undefined"), jinja2.Undefined)

    try:
        raw_template = data.get("template", "")
        yaml_data = yaml.safe_load(data.get("data")) or {}

        jinja_env = Environment(
            trim_blocks=trim_blocks,
            lstrip_blocks=lstrip_blocks,
            keep_trailing_newline=keep_trailing_newline,
            newline_sequence=newline_sequence,
            extensions=extenstions,
            undefined=undefined,
        )
        template = jinja_env.from_string(raw_template)
        output = template.render(**yaml_data)
        return jsonify({"template": output})
    except Exception as e:
        return Response(response=f"Exception: {e}", status=500)


if __name__ == "__main__":
    app.run(debug=True)
