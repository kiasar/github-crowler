import json
import re

import scrapy


URL = 'https://github.com/tensorflow/models'


#  scrapy crawl python_code_comment -o code_comment_tensorflow.json
class GitPythonFileCommentClawler(scrapy.Spider):
    name = 'python_code_comment'
    allowed_domains = ['github.com']
    start_urls = [URL + '/pulls?q=is%3Apr+is%3Aclosed']

    def parse(self, response):
        if 'pulls' in response.request.url:
            for pull in response.xpath('''//a[@data-hovercard-type='pull_request']'''):
                yield scrapy.Request(url=response.urljoin(pull.xpath(".//@href").extract_first()), callback=self.parse)
            next_page = response.xpath('''//a[@class='next_page']/@href''').extract_first()
            if next_page:
                next_page_link = response.urljoin(next_page)
                yield scrapy.Request(url=next_page_link, callback=self.parse)

        elif 'commits' in response.request.url:
            pull_data = response.meta.get('pull_data', [])
            commit_links = response.meta.get('commit_links', [])
            master = 'https://github.com' + \
                     response.xpath("//a[@data-pjax='#js-repo-pjax-container']/@href").extract()[0]
            try:
                date = response.xpath(
                    "//div[@class='commit full-commit prh-commit px-2 pt-2 ']//relative-time/@datetime").extract()[0]
            except:
                date = response.xpath("//relative-time/@datetime").extract()[0]
            for box in response.xpath("//div[contains(@class, 'file js-file js-details-container')]"):
                before, after, code_lines, code_changes = [], [], [], []
                for line in box.xpath(".//table//tr"):
                    if not line.xpath("./@class") and not line.xpath("./@data-position"):
                        num_b = line.xpath("./td[contains(@class, 'blob-num')][1]/@data-line-number").extract()
                        num_a = line.xpath("./td[contains(@class, 'blob-num')][2]/@data-line-number").extract()
                        code = re.sub(r'</?span.*?>|<br>', "",
                                      line.xpath(".//span[@class='blob-code-inner']").extract()[0])
                        change = line.xpath(
                            ".//td[contains(@class, 'blob-code-marker-cell')]/@data-code-marker").extract()[0]
                        before.append(int(num_b[0]) if num_b else -1)
                        after.append(int(num_a[0]) if num_a else -1)
                        code_lines.append(code)
                        code_changes.append(change)
                    elif not line.xpath("./@data-position") \
                            and line.xpath("./@class").extract()[0] == "js-expandable-line":
                        before += [-2] * 10
                        after += [-2] * 10
                        code_lines += [""] * 10
                        code_changes += [" "] * 10

                pull_data['committed_files'].append({
                    'file': master + "/blob/master/" +
                            box.xpath(".//a[@class='link-gray-dark']/@title").extract()[0],
                    'date': date,
                    'before': before,
                    'after': after,
                    'code_lines': code_lines,
                    'code_changes': code_changes})
            if commit_links:
                yield scrapy.Request(
                    url=commit_links[0], callback=self.parse,
                    meta={'commit_links': commit_links[1:], 'pull_data': pull_data})
            else:
                yield pull_data

        elif 'pull' in response.request.url:

            pull_owner = response.xpath(
                '''//a[@class='author text-inherit css-truncate-target']/@href''').extract_first()
            file_code_comments = []

            for code_and_comment in response.xpath(
                        "//div[@class = 'file js-comment-container js-resolvable-timeline-thread-container']"):
                # extracting the file that has been changed
                raw_file_url = code_and_comment.xpath('''./div[@class='file-header']/a/@title''').extract()[0]
                file_url = 'https://github.com/rg3/youtube-dl/blob/master' + raw_file_url

                # extracting the code
                code_lines = []
                before = []
                after = []
                for line in code_and_comment.xpath('''.//tr[not(@class)]'''):
                    temp = line.xpath('''./td[3]/@class''').extract()[0].split()[1]
                    num_b = line.xpath("./td[1]/@data-line-number").extract()
                    num_a = line.xpath("./td[2]/@data-line-number").extract()
                    if temp == 'blob-code-addition' or temp == 'blob-code-deletion':
                        code_lines.append(re.sub(r'</?span.*?>|<br>', "", line.xpath('''./td[3]/span''').extract()[0]))
                        before.append(int(num_b[0]) if num_b else -1)
                        after.append(int(num_a[0]) if num_a else -1)

                # extracting pull_data
                comment_lines = []
                for comment in code_and_comment.xpath('''.//div[@class = 'edit-comment-hide']'''):
                    commenter = comment.xpath(
                        '''.//a[@class ='author text-inherit css-truncate-target']/@href''').extract()[0]

                    text = comment.xpath(
                        '''.//div[@class ='comment-body markdown-body  js-comment-body']''').extract()
                    if not commenter == pull_owner:
                        comment_lines.append({
                            'author': "https://github.com" + commenter,
                            'date': comment.xpath('''.//relative-time/@datetime''').extract()[0],
                            'text': re.sub(r'<[^<>]+>', " ", text[0])
                        })
                if '.py' == file_url[-3:] and comment_lines:
                    file_code_comments.append({
                        'file': file_url,
                        'code': {'before': before, 'after': after, 'code_lines': code_lines},
                        'comments': comment_lines
                    })

            pull_data = {
                'pull': response.request.url,
                'pull_owner': "https://github.com" + pull_owner,
                'file_code_comments': file_code_comments,
                'committed_files': []
            }

            commit_links = []
            for link in response.xpath("//a[@class='message']/@href").extract():
                if 'commits' in link:
                    commit_links.append("https://github.com" + link)
            commit_links = list(set(commit_links))
            if commit_links and file_code_comments:
                yield scrapy.Request(
                    url=commit_links[0], callback=self.parse,
                    meta={'commit_links': commit_links[1:], 'pull_data': pull_data})
        else:
            print("########################################  ERROR ###############################################")


#  scrapy crawl Git_commits -o file_commits_tensorflow.json
class GitCommits(scrapy.Spider):
    name = 'Git_commits'
    allowed_domains = ['github.com']
    start_urls = [URL]

    def parse(self, response):
        if 'commits' in response.request.url:
            commits = response.meta.get('precommits', [])
            for block in response.xpath('''//div[@class='table-list-cell']'''):
                try:
                    committer = \
                        block.xpath(
                            ".//a[@class='commit-author tooltipped tooltipped-s user-mention']/text()").extract()[0]
                    date = block.xpath(".//relative-time/@datetime").extract()[0]
                    commits.append({
                        'committer': 'https://github.com/' + committer,
                        'date': date
                    })
                except:
                    pass
            next_page = response.xpath("//div[@class='pagination']/a[text()='Older']/@href")
            if next_page:
                yield scrapy.Request(url=next_page.extract()[0], callback=self.parse,
                                     meta={'precommits': commits, 'file': response.meta['file']})
            else:
                yield {'file': response.meta['file'], 'commits': commits}
        else:
            for link in response.xpath("//a[@class='js-navigation-open']"):
                if '/tree/' in link.xpath("./@href").extract()[0]:
                    yield scrapy.Request(url=response.urljoin(link.xpath("./@href").extract()[0]), callback=self.parse)
                else:
                    if '.py' == link.xpath("./@href").extract()[0][-3:]:
                        file = response.urljoin(link.xpath("./@href").extract()[0])
                        target_page = file.replace('blob', 'commits')
                        yield scrapy.Request(url=target_page, callback=self.parse, meta={'file': file})
