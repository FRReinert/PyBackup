# -*- coding: utf-8 -*-

'''
The MIT License (MIT)
Copyright (c) 2017 Fabricio Roberto Reinert


Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from os import path, makedirs
from shutil import copy, copytree, ignore_patterns
from errno import ENOTDIR
from . import utils 


class Backup():
	'''
	Main class of the backup system
	'''

	def __init__(self, verbose=False):

		self.verbose 		= verbose
		self.log 			= utils.LogSystem(verbose=verbose)
		self.backup_list 	= []

		
		# Check if settings.py is properly configured and import it
		try:
			from settings import backup_items, sub_folder_name, target_folder, ignore_extensions, now, mailing_list, send_mail, mail_body, mail_subject, mail_settings

		except:
			msg = 'Check if <settings.py> is in your current folder'
			self.log.update_log(msg)
			raise BaseException(msg) from None
			

		else:
			self.backup_itens 		= backup_items
			self.sub_folder_name	= sub_folder_name
			self.target_folder 		= target_folder
			self.ignored_extensions	= ignore_extensions
			self.now 				= now
			self.send_mail 			= send_mail

			# Only import if <send_mail> is set to True
			if send_mail:
				self.mail_subject 		= mail_subject
				self.mail_body 			= mail_body
				self.mail 				= utils.MailSystem(*mailing_list, **mail_settings)

				# Check mailing list
				if len(self.mail.excluded_list) > 0:
					self.log.update_log('Invalid mail addresses detected: %s' % self.mail.excluded_list, 'INFO')


	def clean_list(self):
		'''
		Manage the list of items
		to backup
		'''

		# Case <backup_itens> is empty 
		if self.backup_itens == []:
			msg = "After version 0.0.4 <backup_itens> cannot be empty"
			self.log.update_log(msg)
			raise BaseException(msg) from None

		# Add items
		for item in self.backup_itens:
			if path.isfile(path.abspath(item)) or path.isdir(path.abspath(item)):
				self.backup_list.append(path.abspath(item))
			else:
				log.update_log("Invalid item. It'll be wiped from backup list: <%s>" % item, 'INFO')


	def process_item(self, source, destination):
		'''
		Backup a single item 
		'''
		try:
			copytree(source, destination, ignore=ignore_patterns(*self.ignored_extensions))
		
		except OSError as e:
			if e.errno == ENOTDIR:
				try:
					copy(source, destination)
				
				except:
					log.update_log("Error processing file <%s>: <%s>" % (source, e))
			
			else:
				self.log.update_log("Source <%s> could not be copied to <%s>: <%s>" % (source, destination, e))

		except BaseException as e:
			self.log.update_log("Unkown error copying <%s>: <%s>" % (source, e))


	def process_list(self):
		'''
		Process every item from a <backup_list>
		'''
		default_dest = path.abspath(path.join(self.target_folder, self.sub_folder_name))

		for item in self.backup_list:
			if path.isdir(item):
				folder = path.abspath(item).split('\\')[-1]
				dest = path.join(default_dest, folder)
				self.log.update_log('Processing directory: %s' % item, 'INFO')
				self.process_item(path.abspath(item), dest)
			
			else:
				self.log.update_log('Processing file: %s' % item, 'INFO')
				self.process_item(path.abspath(item), default_dest)


	def run(self):
		'''
		Run backup routine
		'''
		self.clean_list()
		self.process_list()

		# Send email if configured to do so
		if self.send_mail:
			
			subject = self.mail_subject.format(self.now)
			body = self.mail_body.format(self.now, self.backup_itens, self.target_folder)
			
			self.mail.send(subject, body)