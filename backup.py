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

from os import path, makedirs, scandir
from sys import argv
from shutil import copy, copytree, ignore_patterns
from errno import ENOTDIR
import utils 


class Backup():
	'''
	Main class of the backup system
	'''
	def __init__(self, verbose=False):
		
		# Initial attributes
		try:
			self.verbose 		= verbose
			self.log 			= utils.LogSystem(verbose=verbose)
			self.backup_list 	= []
		
		except BaseException as e: 
			self.log.UpdateLog(e)
			raise BaseException(e)
		
		# Check if settings.py is properly configured and import it
		try:
			from settings import backup_items, sub_folder_name, target_folder, ignore_extensions, now, mailing_list, send_mail, mail_body, mail_subject, mail_settings

		except ImportError as e:
			self.log.UpdateLog(e)
			raise ImportError(e)

		else:
			self.backupItems 		= backup_items
			self.subfolderName 		= sub_folder_name
			self.targetFolder 		= target_folder
			self.ignoredExtensions 	= ignore_extensions
			self.now 				= now
			self.sendMail 			= send_mail

			# Only import if <send_mail> is set to True
			if send_mail:
				self.mailSubject 		= mail_subject
				self.mailBody 			= mail_body
				self.mail 				= utils.MailSystem(*mailing_list, **mail_settings)

				# Check mailing list
				if len(self.mail.excludedMails) > 0:
					self.log.UpdateLog('Invalid mail addresses detected: %s' % self.mail.excludedMails, 'INFO')


	def CleanList(self):
		'''
		Manage the list of items
		to backup
		'''

		# Case <backupItems> is empty 
		if self.backupItems == []:
			self.backup_list.append(path.abspath(path.dirname(argv[0])))
			
			return None

		# Add items
		for item in self.backupItems:
			if path.isfile(path.abspath(item)) or path.isdir(path.abspath(item)):
				self.backup_list.append(path.abspath(item))
			else:
				log.UpdateLog("Invalid item. It'll be wiped from backup list: <%s>" % item, 'INFO')


	def ProcessItem(self, source, destination):
		'''
		Backup a single item 
		'''
		try:
			copytree(source, destination, ignore=ignore_patterns(*self.ignoredExtensions))
		
		except OSError as e:
			if e.errno == ENOTDIR:
				try:
					copy(source, destination)
				
				except:
					log.UpdateLog("Error processing file <%s>: <%s>" % (source, e))
			
			else:
				self.log.UpdateLog("Source <%s> could not be copied to <%s>: <%s>" % (source, destination, e))

		except BaseException as e:
			self.log.UpdateLog("Unkown error copying <%s>: <%s>" % (source, e))


	def ProcessList(self):
		'''
		Process every item from a <backup_list>
		'''
		default_dest = path.abspath(path.join(self.targetFolder, self.subfolderName))

		for item in self.backup_list:
			if path.isdir(item):
				folder = path.abspath(item).split('\\')[-1]
				dest = path.join(default_dest, folder)
				self.log.UpdateLog('Processing directory: %s' % item, 'INFO')
				self.ProcessItem(path.abspath(item), dest)
			
			else:
				self.log.UpdateLog('Processing file: %s' % item, 'INFO')
				self.ProcessItem(path.abspath(item), default_dest)


	def Run(self):
		'''
		Run backup routine
		'''
		self.CleanList()
		self.ProcessList()

		# Send email if configured to do so
		if self.sendMail:
			
			subject = self.mailSubject.format(self.now)
			body = self.mailBody.format(self.now, self.backupItems, self.targetFolder)
			
			self.mail.Send(subject, body)



# Debug purpose 
if __name__ == "__main__":

	Bkp = Backup(verbose=True)
	Bkp.Run()