import unittest
import locale
import datetime
from time import gmtime, strftime
from rfeed import *
import pytest

class BaseTestCase(unittest.TestCase):

	def _element(self, element, value, attributes = {}):
		return '<' + element + '>' + value + '</' + element + '>'


class SerializableTestCase(BaseTestCase):

	def test_date(self):
		assert self._element('pubDate', 'Mon, 19 Nov 2018 08:00:00 GMT') in Feed('', '', '', pubDate = datetime.datetime(2018, 11, 19, 8, 0, 0)).rss()


class FeedTestCase(BaseTestCase):

	def test_rss_element(self):
		rss = Feed('', '', '').rss()
		assert '<rss' in rss
		assert 'version="2.0"' in rss
		assert '</rss>' in rss

	def test_channel_element(self):
		rss = Feed('', '', '').rss()
		assert '<channel>' in rss
		assert '</channel>' in rss

	def test_required_elements(self):
		assert self._element('title', 'This is a sample title') in Feed('This is a sample title', '', '').rss()
		assert self._element('link', 'https://www.google.com') in Feed('', 'https://www.google.com', '').rss()
		assert self._element('description', 'This is a sample description') in Feed('', '', 'This is a sample description').rss()

	def test_required_elements_validation(self):
		with self.assertRaises(ElementRequiredError) as cm:
			Feed(title = None, link = '', description = '')
		assert 'title' in str(cm.exception)

		with self.assertRaises(ElementRequiredError) as cm:
			Feed(title = '', link = None, description = '')
		assert 'link' in str(cm.exception)

		with self.assertRaises(ElementRequiredError) as cm:
			Feed(title = '', link = '', description = None)
		assert 'description' in str(cm.exception)

	def test_optional_elements(self):
		assert self._element('language', 'en-us') in Feed('', '', '', language = 'en-us').rss()
		assert self._element('copyright', 'Copyright 2014') in Feed('', '', '', copyright = 'Copyright 2014').rss()
		assert self._element('managingEditor', 'John Doe') in Feed('', '', '', managingEditor = 'John Doe').rss()
		assert self._element('webMaster', 'john@doe.com') in Feed('', '', '', webMaster = 'john@doe.com').rss()
		assert self._element('pubDate', 'Thu, 13 Nov 2014 08:00:00 GMT') in Feed('', '', '', pubDate = datetime.datetime(2014, 11, 13, 8, 0, 0)).rss()
		assert self._element('lastBuildDate', 'Mon, 01 Dec 2014 10:22:15 GMT') in Feed('', '', '', lastBuildDate = datetime.datetime(2014, 12, 1, 10, 22, 15)).rss()
		assert self._element('generator', 'Generator goes here') in Feed('', '', '', generator = 'Generator goes here').rss()
		assert self._element('docs', 'Docs goes here') in Feed('', '', '', docs = 'Docs goes here').rss()
		assert self._element('ttl', '123') in Feed('', '', '', ttl = 123).rss()
		assert self._element('rating', 'abc') in Feed('', '', '', rating = 'abc').rss()

	def test_if_generator_not_specified_use_default_value(self):
		# I'm partially checking for the element because the value includes the version number and
		# changing it will break the test. By just doing a partial match, I make sure the test keeps
		# working in future versions as well.
		assert self._element('docs', 'https://github.com/svpino/rfeed/blob/master/README.md') in Feed('', '', '').rss()

	def test_if_docs_not_specified_use_default_value(self):
		assert '<generator>rfeed v' in Feed('', '', '').rss()

	def test_cloud_element(self):
		rss = Feed('', '', '', cloud = Cloud('1', 2, '3', '4', '5')).rss()
		assert '<cloud ' in rss
		assert 'domain="1"' in rss
		assert 'port="2"' in rss
		assert 'path="3"' in rss
		assert 'registerProcedure="4"' in rss
		assert 'protocol="5"' in rss
		assert '</cloud>' in rss

	def test_image_element(self):
		rss = Feed('', '', '', image = Image('1', '2', '3', 4, 5, '6')).rss()
		assert '<image>' in rss
		assert self._element('url', '1') in rss
		assert self._element('title', '2') in rss
		assert self._element('link', '3') in rss
		assert self._element('width', '4') in rss
		assert self._element('height', '5') in rss
		assert self._element('description', '6') in rss
		assert '</image>' in rss

	def test_textinput_element(self):
		rss = Feed('', '', '', textInput = TextInput('1', '2', '3', '4')).rss()
		assert '<textInput>' in rss
		assert self._element('title', '1') in rss
		assert self._element('description', '2') in rss
		assert self._element('name', '3') in rss
		assert self._element('link', '4') in rss
		assert '</textInput>' in rss

	def test_skiphours_element(self):
		rss = Feed('', '', '', skipHours = SkipHours([0, 2, 4, 6, 8, 10])).rss()
		assert '<skipHours>' in rss
		assert self._element('hour', '0') in rss
		assert self._element('hour', '2') in rss
		assert self._element('hour', '4') in rss
		assert self._element('hour', '6') in rss
		assert self._element('hour', '8') in rss
		assert self._element('hour', '10') in rss
		assert '</skipHours>' in rss

	def test_skipdays_element(self):
		rss = Feed('', '', '', skipDays = SkipDays(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Friday'])).rss()
		assert '<skipDays>' in rss
		assert self._element('day', 'Monday') in rss
		assert self._element('day', 'Tuesday') in rss
		assert self._element('day', 'Wednesday') in rss
		assert self._element('day', 'Thursday') in rss
		assert self._element('day', 'Friday') in rss
		assert self._element('day', 'Saturday') in rss
		assert self._element('day', 'Friday') in rss
		assert '</skipDays>' in rss

	def test_categories_as_single_category_element(self):
		rss = Feed('', '', '', categories = Category(category = '123', domain = '234')).rss()
		assert '<category' in rss
		assert 'domain="234"' in rss
		assert '>123</category>' in rss

	def test_categories_as_single_string_element(self):
		rss = Feed('', '', '', categories = '123').rss()
		assert self._element('category', '123') in rss

	def test_categories_as_category_array_element(self):
		rss = Feed('', '', '', categories = [Category('123'), Category('234'), Category('345')]).rss()
		assert self._element('category', '123') in rss
		assert self._element('category', '234') in rss
		assert self._element('category', '345') in rss

	def test_categories_as_string_array_element(self):
		rss = Feed('', '', '', categories = ['123', '234', '345']).rss()
		assert self._element('category', '123') in rss
		assert self._element('category', '234') in rss
		assert self._element('category', '345') in rss

	def test_image_required_elements_validation(self):
		with self.assertRaises(ElementRequiredError) as cm:
			Image(url = None, title = '', link = '')
		assert 'url' in str(cm.exception)

		with self.assertRaises(ElementRequiredError) as cm:
			Image(url = '', title = None, link = '')
		assert 'title' in str(cm.exception)

		with self.assertRaises(ElementRequiredError) as cm:
			Image(url = '', title = '', link = None)
		assert 'link' in str(cm.exception)

	def test_textinput_required_elements_validation(self):
		with self.assertRaises(ElementRequiredError) as cm:
			TextInput(title = None, description = '', name = '', link = '')
		assert 'title' in str(cm.exception)

		with self.assertRaises(ElementRequiredError) as cm:
			TextInput(title = '', description = None, name = '', link = '')
		assert 'description' in str(cm.exception)

		with self.assertRaises(ElementRequiredError) as cm:
			TextInput(title = '', description = '', name = None, link = '')
		assert 'name' in str(cm.exception)

		with self.assertRaises(ElementRequiredError) as cm:
			TextInput(title = '', description = '', name = '', link = None)
		assert 'link' in str(cm.exception)

	def test_skiphours_required_elements_validation(self):
		with self.assertRaises(ElementRequiredError) as cm:
			SkipHours(hours = None)
		assert 'hours' in str(cm.exception)

	def test_skipdays_required_elements_validation(self):
		with self.assertRaises(ElementRequiredError) as cm:
			SkipDays(days = None)
		assert 'days' in str(cm.exception)

	def test_enclosure_required_elements_validation(self):
		with self.assertRaises(ElementRequiredError) as cm:
			Enclosure(url = None, length = 123, type = '')
		assert 'url' in str(cm.exception)

		with self.assertRaises(ElementRequiredError) as cm:
			Enclosure(url = '', length = None, type = '')
		assert 'length' in str(cm.exception)

		with self.assertRaises(ElementRequiredError) as cm:
			Enclosure(url = '', length = 123, type = None)
		assert 'type' in str(cm.exception)

	def test_cloud_required_elements_validation(self):
		with self.assertRaises(ElementRequiredError) as cm:
			Cloud(domain = None, port = '', path = '', registerProcedure = '', protocol = '')
		assert 'domain' in str(cm.exception)

		with self.assertRaises(ElementRequiredError) as cm:
			Cloud(domain = '', port = None, path = '', registerProcedure = '', protocol = '')
		assert 'port' in str(cm.exception)

		with self.assertRaises(ElementRequiredError) as cm:
			Cloud(domain = '', port = '', path = None, registerProcedure = '', protocol = '')
		assert 'path' in str(cm.exception)

		with self.assertRaises(ElementRequiredError) as cm:
			Cloud(domain = '', port = '', path = '', registerProcedure = None, protocol = '')
		assert 'registerProcedure' in str(cm.exception)

		with self.assertRaises(ElementRequiredError) as cm:
			Cloud(domain = '', port = '', path = '', registerProcedure = '', protocol = None)
		assert 'protocol' in str(cm.exception)

	def test_category_required_elements_validation(self):
		with self.assertRaises(ElementRequiredError) as cm:
			Category(category = None)
		assert 'category' in str(cm.exception)


class ItemTestCase(BaseTestCase):

	def test_required_elements_validation(self):
		with self.assertRaises(ElementRequiredError) as cm:
			Item()
		assert 'title' in str(cm.exception)
		assert 'description' in str(cm.exception)

	def test_optional_elements(self):
		assert self._element('title', 'My title') in Feed('', '', '', items = [Item(title='My title')]).rss()
		assert self._element('link', 'http://example.com/') in Feed('', '', '', items = [Item(title = '', link='http://example.com/')]).rss()
		assert self._element('description', 'My description') in Feed('', '', '', items = [Item(description='My description')]).rss()
		assert self._element('author', 'email@example.com') in Feed('', '', '', items = [Item(title = '', author='email@example.com')]).rss()
		assert self._element('dc:creator', 'Sample Example') in Feed('', '', '', items = [Item(title = '', creator='Sample Example')]).rss()
		assert self._element('comments', 'Sample comment') in Feed('', '', '', items = [Item(title = '', comments='Sample comment')]).rss()
		assert self._element('pubDate', 'Thu, 13 Nov 2014 08:00:00 GMT') in Feed('', '', '', items = [Item(title = '', pubDate = datetime.datetime(2014, 11, 13, 8, 0, 0))]).rss()

	def test_categories_as_single_category_element(self):
		rss = Feed('', '', '', items = [Item(title='abc', categories = Category('123', domain = '234'))]).rss()
		assert '<category' in rss
		assert 'domain="234"' in rss
		assert '>123</category>' in rss

	def test_categories_as_single_string_element(self):
		rss = Feed('', '', '', items = [Item(title='abc', categories = '123')]).rss()
		assert self._element('category', '123') in rss

	def test_categories_as_category_array_element(self):
		rss = Feed('', '', '', items = [Item(title='abc', categories = [Category('123'), Category('234'), Category('345')])]).rss()
		assert self._element('category', '123') in rss
		assert self._element('category', '234') in rss
		assert self._element('category', '345') in rss

	def test_categories_as_string_array_element(self):
		rss = Feed('', '', '', items = [Item(title='abc', categories = ['123', '234', '345'])]).rss()
		assert self._element('category', '123') in rss
		assert self._element('category', '234') in rss
		assert self._element('category', '345') in rss

	def test_enclosure_element(self):
		rss = Feed('', '', '', items = [Item(title = '', enclosure = Enclosure(url = '123', length = 234, type = '345'))]).rss()
		assert '<enclosure ' in rss
		assert 'url="123"' in rss
		assert 'length="234"' in rss
		assert 'type="345"' in rss
		assert '</enclosure>' in rss

	def test_guid_element(self):
		rss = Feed('', '', '', items = [Item(title = '', guid = Guid(guid = '123', isPermaLink = False))]).rss()
		assert '<guid ' in rss
		assert 'isPermaLink="false"' in rss
		assert '123</guid>' in rss

	def test_source_element(self):
		rss = Feed('', '', '', items = [Item(title = '', source = Source(name = '123', url = '234'))]).rss()
		assert '<source ' in rss
		assert 'url="234"' in rss
		assert '123</source>' in rss

	def test_guid_required_elements_validation(self):
		with self.assertRaises(ElementRequiredError) as cm:
			Guid(guid = None)
		assert 'guid' in str(cm.exception)

	def test_source_required_elements_validation(self):
		with self.assertRaises(ElementRequiredError) as cm:
			Source(name = None, url = '123')
		assert 'name' in str(cm.exception)

		with self.assertRaises(ElementRequiredError) as cm:
			Source(name = '123', url = None)
		assert 'url' in str(cm.exception)

	def test_guid_ispermalink_should_be_true_by_default(self):
		guid = Guid(guid = '123')
		assert guid.isPermaLink

	def test_guid_ispermalink_should_be_true_if_none_is_provided(self):
		guid = Guid(guid = '123', isPermaLink = None)
		assert guid.isPermaLink



if __name__ == '__main__':
    unittest.main()
