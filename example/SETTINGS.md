# Settings.py

Name | What's for 
-----|------------
sub_folder_name | Name of the folder which the data will be put inside
now | Time string used in several places to determine time
backup_items | List containing the files/folders to be backed up
target_folder | folder where te backup will be copied
ignore_extensions | extensions to be ignored
mailing_list | List containing email adresses. Triggered when backup is done
send_mail | Boolean. Send email when backup is done
mail_settings | SMTP setup
mail_subject | Template of the Email's subject  
mail_body | Template of the Email's body


# Usability

## sub_folder_name

Everytime you run a backup it'll create a folder where <target_folder> is pointed.

In the example below it'll created a folder more ore less like this: "like this "2017_05_2017_172100"

```python
from time import localtime, strftime 
sub_folder_name = strftime("%Y_%m_%d_%H%M%S", localtime())
```

## now

Used to persist the date/time on email body/subject placeholders and into the Logging system
```python
from time import localtime, strftime 
sub_folder_name = strftime("%Y_%m_%d_%H%M%S", localtime())
```

> Important!
> 
> It's important to use <time.localtime> so the time zone will be considered! 

## backup_items

Nothing better then examples.. so check it out:

### Backups everything under the directory

```python
		directories = []
```

### Selective folders

```python
		directories = [
			'docs',
			'images',
			'spread sheets'
		]
```

### Selective files

```python
		directories = [
			'backup/documents',
			'bd/data.db3',
		]
```

### Absoluth paths

```python
		direcotories = [
			'c:/temp/budget2017.xlsx',
			'c:/users/myusername/'
		]
```
## target_folder

Where the backup will be made. 

Consider that another folder will be created under <target_folder> based on the <sub_folder_name> configuration

```python
target_folder = "c:/temp/backup"
```

## ignore_extensions

## mailing_list

## send_mail

## mail_settings

## mail_subject

## mail_body

# Example of **settings.py**

```python
# -*- coding: utf-8 -*-
from time import localtime, strftime 

sub_folder_name = strftime("%Y_%m_%d_%H%M%S", localtime())
now = strftime("%Y-%m-%d %H:%M:%S", localtime())
backup_items = []
mailing_list = []
ignore_extensions = ['*.py','*.pyc', '*.log']
target_folder = ''
send_mail = True
mail_settings = {
	'server'		: 'smtp.live.com',
	'port'			: 25,
	'mail_address'	: '@live.com',
	'username'		: '@live.com',
	'password'		: '',
	'tls'			: True,
}
mail_subject = 'Backup System. {0}'
mail_body = '''
Backup System

	Backup Performed at:	{0}
	Backup Items:	{1}
	Destination folder:	{2}
'''
