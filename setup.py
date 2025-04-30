import subprocess

def run_command(command):
    print(f"Running: {command}")
    subprocess.run(command, shell=True, check=True)

def main():
    # Make migrations
    run_command("python manage.py makemigrations")
    
    # Apply migrations
    run_command("python manage.py migrate")
    
    # Run server
    run_command("python manage.py runserver")

if __name__ == "__main__":
    main()