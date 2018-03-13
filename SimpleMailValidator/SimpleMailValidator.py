#!/usr/bin/python


import csv, json
import re, DNS
from validate_email import validate_email
from optparse import OptionParser

# DNS.DiscoverNameServers()
DNS.defaults['server'].append('208.67.222.222')
DNS.defaults['server'].append('208.67.222.220')
DNS.defaults['timeout'] = 5

## Vars

is_valid = False
username = "null"
domain   = "null"
free  = False
diposable = False
has_mx   = False
mx_list  = []
outfilename= "outfile.csv"
header = ['email','is_valid','is_free','is_diposable','has_mx','mx_records']
regex = '^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*(\.[a-zA-Z]{2,4})$'

## Parser setup
parser = OptionParser()
parser.add_option("-i", "--infile", dest="infilename", default="infile.csv" , help="Name of file containing email addresses.  If not specified,Deafault is infile.csv.", metavar="FILE")
parser.add_option("-o", "--outfile", dest="outfilename", help="Name of file to write bad addresses to.  If not specified, Deafault is outfile.csv.", metavar="FILE")

(options, args) = parser.parse_args()

if ( options.infilename != None ):
	infilename = options.infilename
else:
	infilename = "infile.csv"
if ( options.outfilename != None ):
	outfilename = options.outfilename
else:
	outfilename = "outfile.csv"

#### functions
## Get the Domain from email
def get_domain(email):
	domain = email[email.find('@')+1:]
	return domain


## 1- Check if email is valid with regex
def is_valid(email, regex):
	test1 = validate_email(email,check_mx=False)
	test2 = match = re.match(regex, email)
	#print test1,test2
	if (test2 != None and  True == test1):
		return True
	else:
		return False
			
## 2- Check if email provider is free
def is_free(domain):
	if domain in open('email_providers_free.txt').read():
    		return True
	else:
    		return False

## 3- Check if email is disposable // https://github.com/cloudacademy/DisposableEmailChecker
def is_disposable(domain):
	if domain in open('email_providers_disposable.txt').read():
    		return True
	else:
    		return False

## 4- Check if the domain has MX records, if yes get those records
cached_lookups = {}

# import pdb; pdb.set_trace()
def has_mx_records(domain):
    mx_hosts=[]
    DNS.DiscoverNameServers()
    if domain in cached_lookups.keys():
	return True, cached_lookups[domain]
	
    i = 0
    while i < 3:
        i = i+1
        DNS.defaults['timeout'] = i+2
	try:
		mx_hosts = DNS.mxlookup(domain)
		#result = (len(mx_hosts) > 0)
	except DNS.Base.ServerError as e:
		#return False,[]
		if e[1] == 3 or e[1] == 2:
			return False, []
			#result = False,[]
        except DNS.Base.TimeoutError:
            # print "(timeout on %s)" % domain
            continue
        break
    # except DNS.Base.TimeoutError:
    #     result = True
    if (mx_hosts):
 	cached_lookups[domain] = mx_hosts			
	return True,mx_hosts
    else:
	return False, []

def main(email):
	result_list = [email]
	if (is_valid(email, regex)):
		result_list.append(True)
		domain = get_domain(email)
		free = is_free(domain)
		result_list.append(free)
		disposable = is_disposable(domain)
		result_list.append(disposable)	
		has_mx, mx_list = has_mx_records(domain)
		result_list.append(has_mx)
		result_list.append(mx_list)
	else:
		result_list.append(False)
		result_list.append(False)
		result_list.append(False)
		result_list.append(False)
		result_list.append([])
	return result_list

	



outfile = open(outfilename, 'w')
csvwriter = csv.writer(outfile, delimiter=',')
csvwriter.writerow(header)

with open(infilename, 'rb') as infile:
	addresses = csv.reader(infile)
	for address in addresses:
		res = main(address[0])
		csvwriter.writerow(res)
                
outfile.close()
