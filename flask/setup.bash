#!/bin/bash

# Update package lists
sudo apt-get update

# Install necessary packages
sudo apt-get install -y mariadb-server libmariadb-dev python3-pip python3-venv

# Start MariaDB service
sudo systemctl start mariadb

# Secure MariaDB installation (you can provide answers to prompts if needed)
sudo mysql_secure_installation

# Create the user and database for the application
DB_NAME="my_database"
DB_USER="my_user"
DB_PASS="my_password"

# Execute SQL commands
sudo mysql -u root -e "CREATE DATABASE IF NOT EXISTS ${DB_NAME};"
sudo mysql -u root -e "CREATE USER IF NOT EXISTS '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASS}';"
sudo mysql -u root -e "GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'localhost';"
sudo mysql -u root -e "FLUSH PRIVILEGES;"

echo "Database and user setup complete."

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install Python packages inside the virtual environment
pip install flask flask-cors flask-sqlalchemy

echo "Virtual environment setup complete and packages installed."

# Create a run script to start the Flask application
cat <<EOL > run.sh
#!/bin/bash
source venv/bin/activate
export FLASK_APP=app.py
flask run --host=0.0.0.0
EOL

# Make the run script executable
chmod +x run.sh

# Display message
echo "Setup completed successfully. You can now run your Flask application using ./run.sh"

# Optionally, start the Flask application immediately
./run.sh
