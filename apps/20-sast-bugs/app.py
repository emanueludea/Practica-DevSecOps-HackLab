from flask import Flask, request
import yaml, subprocess

app = Flask(__name__)

@app.route('/yaml', methods=['POST'])
def yaml_parse():
    data = request.data.decode('utf-8')
    # Inseguro a propósito: yaml.load sin SafeLoader
    obj = yaml.load(data, Loader=None)
    return {"parsed": str(obj)}

@app.route('/run')
def run_cmd():
    cmd = request.args.get('cmd', 'echo hello')
    # General fix: only allow 'echo' command with arguments, no shell=True
    import shlex
    parts = shlex.split(cmd)
    if not parts or parts[0] != 'echo':
        return {"error": "Only 'echo' command is allowed."}, 400
    try:
        out = subprocess.check_output(parts)
        return {"out": out.decode('utf-8')}
    except Exception as e:
        return {"error": str(e)}, 400

@app.route('/')
def idx():
    return "SAST-bugs demo"
