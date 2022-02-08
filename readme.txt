sudo apt install python3-pip

sudo apt-get install python3-venv 
python3 -m venv .venv
source .venv/bin/activate

Select Interpreted and launch.json create it


Install ODBC Driver for SQL Server

curl https://packages.microsoft.com/config/ubuntu/19.10/prod.list > /etc/apt/sources.list.d/mssql-release.list

sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install msodbcsql17
sudo apt-get install unixodbc-dev

Once the driver is installed you then need to install pyodbc with pip
pip3 install pyodbc

