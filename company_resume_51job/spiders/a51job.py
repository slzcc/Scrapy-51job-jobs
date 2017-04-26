# -*- coding: utf-8 -*-
import re, html2text, datetime, time
from scrapy_redis.spiders import RedisSpider
from company_resume_51job.items import CompanyResume51JobItem

class A51jobSpider(RedisSpider):
    name = "51job"
    allowed_domains = ["http://www.51job.com/"]
    redis_key = '51job:start_urls'

    def parse(self, response):
        item = CompanyResume51JobItem()
        data = response.xpath('//div[@class="tCompany_center clearfix"]')
        item['position_url'] = response.url
        item['position_name'] = data.xpath('div/div/div/h1/text()').extract()[0]
        item['position_address'] = data.xpath('div/div/div/span[@class="lname"]/text()').extract()[0]
        position_salary = data.xpath('div/div/div/strong/text()').extract()
        if position_salary:
            item['position_salary'] = position_salary[0]
        else:
            item['position_salary'] = ""
        company_label = []
        for i in data.xpath('div/div/div/p[@class="msg ltype"]/text()').extract()[0].split("|"):
            a = re.sub('\t','',i)
            company_label.append(re.sub('\xa0', "", a))
        item['company_label'] = "".join(company_label).split()
        item['company_name'] = data.xpath('div/div/div/p/a/text()').extract()[0]
        item['company_recruitment_url'] = data.xpath('div/div/div/p/a/@href').extract()[0]

        position_requirements = []
        for i in data.xpath('div[@class="tCompany_main"]/div/div/div/span'):
            label = i.xpath('text()').extract()[0]
            print(label)
            if re.findall(r"(.?.?\d+.?)经验",label):
                item['work_experience'] = re.findall(r"(.?.?\d+.?)经验",label)
            if re.findall(r"招聘(\d+)", label):
                item['hiring_number'] = re.findall(r"招聘(\d+)", label)
            if re.findall(r"(\d+\-\d+)发布",label):
                ReleaseTime = re.findall(r"(\d+\-\d+)发布",label)[0].split("-")
                print(int(ReleaseTime[0]),int(ReleaseTime[1]))
                item['release_time'] = datetime.datetime(time.localtime(time.time())[0], int(ReleaseTime[0]), int(ReleaseTime[1]))
            position_requirements.append(label)
        item['position_requirements_label'] = position_requirements

        jobs_info = []
        for i in html2text.html2text(data.xpath('div[@class="tCompany_main"]/div[@class="tBorderTop_box"]/div[@class="bmsg job_msg inbox"]').extract()[0]):
            jobs_info.append(i.strip())
        item['jobs_info'] = "".join(jobs_info)
        return item