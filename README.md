# CSVConverter
        CSV/XML Converter Installation from Source Code

___________________________________________________________________
                 INSTALLATION INSTRUCTIONS
                 ------------------------
>In this 'how to', it is assumed that the application is to be installed on an Ubuntu server, deployed through Apache and mod_wsgi however, the application is crossplatform and thus can run on virtually any OS/platform.
>Detailed instructions on how to install the three application(python, django, postgresql) are available on the provided URLs.

Use a LAMP stack server

1. Update and upgrade the system
	
	apt-get update
	apt-get upgrade

2. Install make
	
	apt-get install make

3. Install build files
	
	apt-get install build-essential
	apt-get install libreadline-dev
	apt-get install zlib1g-dev 
	apt-get install python-pip
	apt-get install python-genshi python-lxml python3-setuptools

4. Install django version == 1.8 (www.djangoproject.com/download/) 

	pip install Django==1.8
    
5. Download and install postgresql version >= 9.1 (Changed username to postgres to postgres2 so as not to interfere with any future users/roles)

	wget ftp://ftp.postgresql.org/pub/source/v9.1.21/postgresql-9.1.21.tar.gz
	gunzip postgresql-9.1.21.tar.gz
	tar xf postgresql-9.1.21.tar
	cd postgresql-9.1.21/
	./configure
	make
	su
	make install
	adduser postgres2
	mkdir /usr/local/pgsql/data
	chown postgres2 /usr/local/pgsql/data
	su -postgres2
	/usr/local/pgsql/bin/initdb -D /usr/local/pgsql/data
	/usr/local/pgsql/bin/postgres -D /usr/local/pgsql/data >logfile 2>&1 &
	/usr/local/pgsql/bin/createdb skunkworks
	/usr/local/pgsql/bin/psql skunkworks
	
6. Install 'psycopg2' for the database interface(This is how Django interacts with postgresql)
	apt-get install python-pyscopg2
	apt-get install python-egenix-mxtools-dbg python-egenix-mxtools-doc python-psycopg2-doc

7. Install modwsgi (docs.djangoproject.com/ja/1.9/howto/deployment/wsgi/modwsgi/)
	sudo aptitude install apache2 apache2.2-common apache2-mpm-prefork apache2-utils libexpat1 ssl-cert
	sudo aptitude install libapache2-mod-wsgi

8. Enable mod_wsgi
        a2enmod wsgi

9. Once you’ve got mod_wsgi installed and activated, edit your Apache server’s httpd.conf (wiki.apache.org/httpd/DistrosDefaultLayout)
    file and add the following. If you are using a version of Apache older than 2.4, replace Require all granted with Allow from
   all and also add the line Order deny,allow above it. Replace "/path/to" with the path directory containing the "csv_converter" folder.
   Note. The application files can be placed in any directory. You just have to make sure that the permissions configurations are accessible
   by the Apache process.

        WSGIScriptAlias / /path/to/csv_converter/wsgi.py
        WSGIPythonPath /path/to/mysite.com

        <Directory /path/to/csv_converter/sw>
          <Files wsgi.py>
            Require all granted
          </Files>
        </Directory>
          Alias /static /path/to/csv_converter/static
        <Directory /path/to/csv_converter/static>
          Require all granted
        </Directory>  
        WSGIScriptAlias / /path/to/csv_converter/sw/wsgi.py
        WSGIPythonPath /path/to/csv_converter

10. The first time that you run the application, you will need to set up the database. To do this:
        cd /path/to/csv_converter
        python manage.py makemigrations
        python manage.py migrate

    For testing purposes, you can run the application id django's builtin server:
        python manage.py runserver
    This is only suitable for testing and should not be used for production

11. Restart apache2 service
	service apache2 restart

    Django settings, such as Time Zones, database host and port, Allowed hosts, etc are available on the 'csv_converter/sw/settings.py' file.
