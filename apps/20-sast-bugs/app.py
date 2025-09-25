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
    # Use Python API instead of system command to avoid command injection
    import shlex
    parts = shlex.split(cmd)
    if not parts or parts[0] != 'echo':
        return {"error": "Only 'echo' command is allowed."}, 400
    # Join the arguments and return as output, mimicking echo
    output = ' '.join(parts[1:]) + '\n'
    return {"out": output}

@app.route('/')
def idx():
    return "SAST-bugs demo"
