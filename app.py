from flask import Flask, render_template, request, jsonify
import qgen2

app = Flask(__name__)

qgen_instance = qgen2.QGen()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()

    flags = [100, 0, 50, 0]

    password_length = int(data['length'])
    generation_mode = str(data['generation_mode'])
    is_cluster_separation = bool(data['is_cluster_separation'])

    flags[0] = int(data['flags_lo'])
    flags[1] = int(data['flags_up'])
    flags[2] = int(data['flags_nu'])
    flags[3] = int(data['flags_pt'])

    generated_password = "AMOGUS"

    if generation_mode == "random":
        generated_password = qgen_instance.weighted_random(password_length, flags)
    elif generation_mode == "readable":
        generated_password = qgen_instance.cluster_gen(password_length, flags, is_cluster_separation)

    return jsonify(result_string=generated_password)


if __name__ == '__main__':
    app.run(debug=False)