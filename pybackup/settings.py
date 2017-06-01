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
