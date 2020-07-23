
import re

from urlwatch import filters
from urlwatch import jobs
from urlwatch import reporters

from bs4 import BeautifulSoup

class CustomTextFileReporter(reporters.TextReporter):
    """Custom reporter that writes the text-only report to a file"""

    __kind__ = 'custom_file'

    def submit(self):
        with open(self.config['filename'], 'w') as fp:
            fp.write('\n'.join(super().submit()))


class CustomHtmlFileReporter(reporters.HtmlReporter):
    """Custom reporter that writes the HTML report to a file"""

    __kind__ = 'custom_html'

    def submit(self):
        with open(self.config['filename'], 'w') as fp:
            fp.write('\n'.join(super().submit()))

class CustomMarkdownFileReporter(reporters.MarkdownReporter):
    """Custom reporter that writes the Markdown report to a file"""

    __kind__ = 'custom_markdown'

    def submit(self):
        with open(self.config['filename'], 'w') as fp:
            fp.write('\n'.join(super().submit()))

class GitHubTagFilter(filters.RegexMatchFilter):
    """Search for new GitHub releases"""

    MATCH = {'url': re.compile('https://github.com/.*/releases.*')}

    def filter(self, data):
        soup = BeautifulSoup(data, "lxml")

        releases = soup.select('div.release-header div.f1 a')

        if releases:
            results = [rel.text for rel in releases]
            return '\n'.join(results)

        else:
            fallback = soup.select('div.site')
            return '\n'.join([str(tag) for tag in fallback])
 
class GitLabTagFilter(filters.RegexMatchFilter):
    """Search for new gitlab tags"""

    MATCH = {'url': re.compile('https://gitlab.com/.*/tags.*')}

    def filter(self, data):
        soup = BeautifulSoup(data, "lxml")

        releases = soup.select('a.ref-name')

        if releases:
            results = [rel.text for rel in releases]
            return '\n'.join(results)

        else:
            fallback = soup.select('div.site')
            return '\n'.join([str(tag) for tag in fallback])

class PyPIFilter(filters.RegexMatchFilter):
    """Search for new releases on PyPI"""

    MATCH = {'url': re.compile('https://pypi.org/project/.*/#history')}

    def filter(self, data):
        soup = BeautifulSoup(data, "lxml")

        releases = soup.find_all('p', class_='release__version')
        if releases:
            releases = [rel.text for rel in releases]
            return ''.join(releases)
        else:
            return data
