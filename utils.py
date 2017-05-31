# -*- coding: utf-8 -*-

import logging
from smtplib import SMTP, SMTPException
from time import localtime, strftime
from re import match, IGNORECASE

def getDateTime():
	return strftime("%Y-%m-%d-%H:%M:%S", localtime())

class LogSystem():
	'''
	Manage the log systemm. 
	May not work as a MIXIN. Instead, instantiate as an object 
	'''
	def __init__(self, verbose=False):
		self.now = ""
		self.verbose = verbose
		logging.basicConfig(filename='backup.log', level=logging.INFO)

	def UpdateTime(self):
		self.now = getDateTime()

	def UpdateLog(self, exception, type='ERROR'):
		self.UpdateTime()
		msg = self.now+': '+exception
		if type == 'ERROR':
			logging.error(msg)
			if self.verbose: print(msg) 

		if type == 'INFO':
			logging.info(msg)
			if self.verbose: print(msg) 


class MailSystem():

	def __init__(self, *mail_list, **config):

		self.mailing_list 	= mail_list
		self.smtp_server	= config['server']
		self.smtp_port		= config['port']
		self.mail_address 	= config['mail_address']
		self.username		= config['username']
		self.pasword 		= config['password']
		self.tls			= config['tls']
		

		# Mailing List
		self.mailingList = []
		self.excludedMails = []

		for item in self.mailing_list:
			if match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", item, IGNORECASE):
				self.mailingList.append(item)
			
			else:
				self.excludedMails.append(item)

		# Create SMTP object
	
	def Connect(self):
		'''
		connect to SMTP server an return the SMTP object
		'''
		try:
			SMTP_obj = SMTP(self.smtp_server, self.smtp_port)
		
		except SMTPException as e:
			raise "Could not create SMTP object: %s" % e

		# StartTLS
		if self.tls:
			try:
				SMTP_obj.ehlo()
				SMTP_obj.starttls()
			
			except SMTPException as e:
				print("Could not open a TLS connection: %s" % e)

		# login to SMTP
		try:
			SMTP_obj.ehlo()
			SMTP_obj.login(self.username, self.pasword)
		
		except SMTPException as e:
			print("Could not logon: %s" % e)

		return SMTP_obj

	def Send(self, subject, message):
		'''
		Send email to mailing list
		'''

		smtp = self.Connect()

		header  = 'from: %s\n' % self.mail_address
		header += 'to: %s\n' % ','.join(self.mailingList)
		header += 'subject: %s\n' % subject
		message = header + '\r\n\r\n' + message

		try:
			smtp.sendmail(self.mail_address, self.mailingList, message)
			smtp.quit()
		
		except SMTPException as e:
			print ("Could not send the emails: %s" % e)