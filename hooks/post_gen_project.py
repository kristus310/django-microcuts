import subprocess
import shutil
import os
import secrets
import string

PYTHON_VERSION = "{{ cookiecutter.python_version }}"
PROJECT_SLUG = "{{ cookiecutter.project_slug }}"
USE_CELERY = "{{ cookiecutter.use_celery }}"

def cleanup_unused_files():
    if USE_CELERY != 'yes':
        for path in ['core/celery.py', 'core/__init__.py']:
            full_path = os.path.join(os.getcwd(), path)
            if os.path.exists(full_path):
                os.remove(full_path)
                print(f"--- Removed unused {path} ---")

def rename_enviroment_files():
    if os.path.exists('_gitignore'):
        os.rename('_gitignore', '.gitignore')
        print("--- Renamed _gitignore to .gitignore ---")

    if os.path.exists('_env.example'):
        os.rename('_env.example', '.env.example')
        print("--- Renamed _env.example to .env.example ---")

def copy_env_file():
    example = os.path.join(os.getcwd(), '_env.example')
    env_file = os.path.join(os.getcwd(), '.env')

    if not os.path.exists(example):
        print(f"[-] _env.example not found at {example}")
        return

    if not os.path.exists(env_file):
        shutil.copy(example, env_file)
        print("--- Created .env from _env.example ---")

def generate_secret_key():
    env_path = os.path.join(os.getcwd(), '.env')
    if not os.path.exists(env_path):
        print("[-] .env not found, skipping secret key generation")
        return

    try:
        from django.core.management.utils import get_random_secret_key
        key = get_random_secret_key()
    except ImportError:
        alphabet = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
        key = ''.join(secrets.choice(alphabet) for _ in range(50))

    with open(env_path, 'r') as f:
        content = f.read()
    with open(env_path, 'w') as f:
        f.write(content.replace('SECRET_KEY=CHANGE_ME', f'SECRET_KEY={key}'))

    print("--- Generated SECRET_KEY ---")

def setup_environment():
    try:
        print(f"--- Activating Python {PYTHON_VERSION} with mise ---")
        subprocess.run(["mise", "use", f"python@{PYTHON_VERSION}"], check=True)

        print("--- Syncing dependencies with uv ---")
        subprocess.run(["mise", "x", "--", "uv", "sync", "--python", PYTHON_VERSION], check=True)

    except FileNotFoundError as e:
        print(f"\n[-] Missing tool: {e}. Please ensure mise and uv are installed.")
    except subprocess.CalledProcessError as e:
        print(f"\n[-] Error during environment setup: {e}")

def init_git():
    try:
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)
        print("--- Initialized git repository ---")
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        print(f"[-] Git init failed: {e}")

def finalize():
    commands = [
        ["codium", ".", "-r"],
        ["code", ".", "-r"],
        ["flatpak", "run", "com.vscodium.codium", ".", "-r"],
        ["flatpak", "run", "com.visualstudio.code", ".", "-r"]
    ]

    for cmd in commands:
        try:
            subprocess.run(cmd, check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            print(f"--- Reopened workspace in {cmd[0]} ---")
            return
        except (FileNotFoundError, subprocess.CalledProcessError):
            continue

if __name__ == "__main__":
    cleanup_unused_files()
    copy_env_file()
    rename_enviroment_files()
    generate_secret_key()
    setup_environment()
    init_git()
    #finalize()
    print(f"\n[+] {PROJECT_SLUG} is ready")