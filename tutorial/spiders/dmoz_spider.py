import scrapy
import unicodedata
import os
import re
import csv
import codecs

################ Code to Extract Email from Span tag ########################
def string_extractor(unsorted_email):
				# print unsorted_email
				array_email = unsorted_email.split("[")
				# print array_email
				array_email_string = str(array_email[1])
				# print array_email_string
				email_part = re.findall('"([^"]*)"', array_email_string)
				final_email = ""
				count = int(0)
				for i in reversed(email_part):
					
					if(i == "m7i7"):
						final_email = final_email + "@"
					elif(count == 0):
						final_email = i
						count = count + 1
					elif (count == 1):
						
						final_email = final_email + i
						count = count + 1
					else:
						final_email = final_email + "." + i
					# print count
				return final_email

################ saving data to CSV file ####################################
def save_to_csv(person_details):

    try:
        with codecs.open("/home/saurabh/tutorial/prof_data.csv", "a", encoding="utf-8") as f_write:
            csv_writer = csv.writer(f_write)
            csv_writer.writerow(person_details)
            # f_write.write(person_details)
            # f_write.write("\n")

    except IOError as e:
        print e
    # finally:
    #     f_write.close()
        

################ Adding Header in the Csv file ############################
def addHeader():
    header = "First" + "," + "Last" + "," + "Affiliations" + "," + "Email" + "\n"
    try:
        with open("/home/saurabh/tutorial/prof_data.csv", "w", ) as f:
            f.write(header)

    except IOError as e:
        print e
    finally:
        f.close()


class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["ideas.repec.org"]
    start_urls = ["https://ideas.repec.org/i/eacc.html"]

    def parse(self, response):
        if(os.path.exists("/home/saurabh/tutorial/prof_data.csv")):
            os.remove("/home/saurabh/tutorial/prof_data.csv")
        addHeader()
        print "\n"
        for link in response.xpath('//tr/td/a/@href'):
            url = response.urljoin(link.extract())
            yield scrapy.Request(url, callback=self.parse_page_contents)
        print "\n"

    def parse_page_contents(self, response):
        v_email = "Not Defined"
        # person_data = ""
        person_data = []
        affiliation = ""
        first = response.xpath(
            '//*[@id="details-body"]/table/tbody/tr[1]/td[2]/text()').extract()
        last = response.xpath(
            '//*[@id="details-body"]/table/tbody/tr[3]/td[2]/text()').extract()
        email = response.xpath(
            '//*[@id="details-body"]/table/tbody/tr[7]/td[2]/span').extract()
        # print first[0] + " " + last[0]

        affiliations = response.xpath(
            '//*[@id="affiliation-body"]/div/div/div/h4/a/text()').extract()
        for x in affiliations:
            x = unicodedata.normalize('NFKD', x).encode('ascii', 'ignore')
            x = str(x)
            x = x.replace("\n", "")
            affiliation = affiliation + "  " + x

        # print affiliations
        print "bhopu"
    
        if(len(email) != 0):
            if(email[0] == "[This author has chosen not to make the email address public]"):
                v_email = "Not Defined"
            else:
                
                final_email = string_extractor(email[0])
                print final_email
                if(re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', final_email)):
                    v_email = final_email

        # print v_email
        # person_data = first[0] + "," + last[0] + \
        #     "," + affiliation + "," + v_email
        person_data.append(first[0])
        person_data.append(last[0])
        person_data.append(affiliation)
        person_data.append(v_email)
        save_to_csv(person_data)

    # code
