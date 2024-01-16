import jinja2
import yaml
from jinja2.sandbox import SandboxedEnvironment
from flask import Flask, render_template, request, jsonify
from load_filter import load_filter_ansible, load_filter_salt, load_filter_st2

app = Flask(__name__, static_url_path="/static")
app.json.sort_keys = False
app.config.update(
    TITLE="Jinaj101",
    SUBTITLE="Playground for jinja2 templates",
    GITHUB="https://github.com/infrastructureAsCode-ch/jinja101/"
)

MAP_UNDEFINED = {
    "jinja2.Undefined": jinja2.Undefined,
    "jinja2.ChainableUndefined": jinja2.ChainableUndefined,
    "jinja2.DebugUndefined": jinja2.DebugUndefined,
    "jinja2.StrictUndefined": jinja2.StrictUndefined,
}

NEWLINE_SEQUENCES = {"\\r": "\r", "\\n": "\n", "\\r\\n": "\r\n"}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/examples")
def examples():
    try:
        with open("examples.yaml", "r") as f:
            data = yaml.safe_load(f)
        resp = jsonify(data)
    except Exception as e:
        resp = jsonify({"error": f"Error {type(e).__name__}", "msg": str(e)})
        resp.status_code = 400
    finally:
        return resp


@app.route("/rend", methods=["POST"])
def rend():
    data = request.get_json()
    if not isinstance(data, dict):
        resp = jsonify({"error": "Invalid JSON"})
        resp.status_code = 400
        return resp
    trim_blocks = bool(data.get("trim_blocks"))
    lstrip_blocks = bool(data.get("lstrip_blocks"))
    keep_trailing_newline = bool(data.get("keep_trailing_newline"))
    newline_sequence = NEWLINE_SEQUENCES.get(data.get("newline_sequence"), "\n")
    extenstions = data.get("extensions", [])
    extenstions = [extenstions] if isinstance(extenstions, str) else extenstions
    undefined = MAP_UNDEFINED.get(data.get("undefined"), jinja2.Undefined)
    raw_template = data.get("template", "")
    load_filter = data.get("filter", "default")

    try:
        yaml_data = yaml.safe_load(data.get("data")) or {}
        if not isinstance(yaml_data, dict):
            yaml_data = {"data": yaml_data}

        jinja_env = SandboxedEnvironment(
            trim_blocks=trim_blocks,
            lstrip_blocks=lstrip_blocks,
            keep_trailing_newline=keep_trailing_newline,
            newline_sequence=newline_sequence,
            extensions=extenstions,
            undefined=undefined,
        )
        if load_filter == "ansible":
            load_filter_ansible(jinja_env)
        if load_filter == "salt":
            load_filter_salt(jinja_env)
        if load_filter == "st2":
            load_filter_st2(jinja_env)

        template = jinja_env.from_string(raw_template)
        output = template.render(**yaml_data)
        resp = jsonify({"template": output})
    except yaml.error.YAMLError as e:
        resp = jsonify({"error": f"YAML {type(e).__name__}", "msg": str(e)})
        resp.status_code = 400
    except jinja2.exceptions.TemplateError as e:
        resp = jsonify({"error": f"Jinja {type(e).__name__}", "msg": str(e)})
        resp.status_code = 400
    except Exception as e:
        resp = jsonify({"error": f"Error {type(e).__name__}", "msg": str(e)})
        resp.status_code = 400
    finally:
        return resp


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
