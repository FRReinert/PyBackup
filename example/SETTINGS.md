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

Use wildcards to exclude extensions, folders and files

```python
ignore_extensions = ['*.py','*.pyc']
```
## send_mail

Boolean. Set it ```True``` if you want to send email after backup routine is completed

```python
send_mail = True
```

## mailing_list

List containing e-mail adrresses which is going to be triggered when backup finishes

```python
mailing_list = [
	'myemail@domain.com',
	'another@email.com',
	'other@one.com.br'
]
```

## mail_settings

Setup your SMTP account to send emails. 

Example of Microsoft Live domain:

```python
mail_settings = {
	'server'		: 'smtp.live.com',
	'port'			: 25,
	'mail_address'		: 'myemail@live.com',
	'username'		: 'myemail@live.com',
	'password'		: 'mypassword@2017',
	'tls'			: True,
}
```

## mail_subject

Subject template of the email. 

Tag | Return
----|------------
{0} | ```now```

```python
mail_subject = 'Backup System. {0}'
```

## mail_body

Body template of the email.

Tag | Return
----|------------
{0} | ```now```
{1} | ```directories```
{2} | ```target_folder```

```python
mail_body = '''Backup System

	Backup Performed at:	{0}
	Backup Items:		{1}
	Destination folder:	{2}
'''
```
