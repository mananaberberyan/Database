DB_NAME="productspecification"
DB_USER="postgres"
DB_PASSWORD="man123"
DB_OWNER="postgres"

# Drop existing user if needed
sudo -u postgres psql -c "DROP USER IF EXISTS $DB_USER;"

# Create a new user
sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"

# Set ownership of the database
sudo -u postgres psql -c "ALTER DATABASE $DB_NAME OWNER TO $DB_OWNER;"