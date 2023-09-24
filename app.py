
from flask import Flask, render_template, request, redirect, url_for
import docker

app = Flask(__name__)
client = docker.from_env()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_imapsync', methods=['POST'])
def run_imapsync():
    # Retrieve user input from the form
    source_host = request.form.get('source_host')
    source_user = request.form.get('source_user')
    source_password = request.form.get('source_password')

    target_host = request.form.get('target_host')
    target_user = request.form.get('target_user')
    target_password = request.form.get('target_password')

    # Create a unique container name
    container_name = f'imapsync-container-{source_host}-{target_host}'

    # Run imapsync inside a Docker container
    command = [
        'imapsync',
        '--host1', source_host,
        '--user1', source_user,
        '--password1', source_password,
        '--host2', target_host,
        '--user2', target_user,
        '--password2', target_password,
    ]

    container = client.containers.run(
        'gilleslamiral/imapsync',
        command,
        detach=True,
        name=container_name,
    )

    # Capture and display logs in real-time
    logs = []
    for log_line in container.logs(stream=True, follow=True):
        logs.append(log_line.decode('utf-8'))

    return render_template('logs.html', logs=logs)

if __name__ == '__main__':
    app.run(debug=True)
