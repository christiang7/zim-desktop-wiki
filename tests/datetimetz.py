
# Copyright 2014 Jaap Karssenberg <jaap.karssenberg@gmail.com>

import os
import sysconfig
import warnings

import tests
import zim.datetimetz as datetime


class TestDateTimeZ(tests.TestCase):

	# FIXME would be better to test correctness of results
	#       but first check functions do not give errors

	def setUp(self):
		with warnings.catch_warnings():
			warnings.simplefilter("ignore")
			try:
				import babel
			except ImportError:
				pass

	def runTest(self):
		# now()
		dt = datetime.now()
		s = dt.isoformat()
		self.assertTrue(isinstance(s, str) and len(s) > 0)

		s = dt.strftime("%z")
		self.assertTrue(isinstance(s, str) and len(s) > 0)

		s = dt.strftime("%Z")
		self.assertTrue(isinstance(s, str) and len(s) > 0)

		# strftime
		s = datetime.strftime('%a', dt)
		self.assertTrue(isinstance(s, str) and len(s) > 0)

		s = datetime.strftime('%%', dt)
		self.assertEqual(s, '%')

		# is not mingw? https://github.com/msys2/msys2.github.io/blob/source/web/docs/python.md?plain=1#L12
		if not (os.name == 'nt' and sysconfig.get_platform().startswith('mingw')):
			# Failed under msys python3.7.2
			s = datetime.strftime('%u', dt)
			self.assertTrue(isinstance(s, str) and len(s) > 0)

			s = datetime.strftime('%V', dt)
			self.assertTrue(isinstance(s, str) and len(s) > 0)

		s = datetime.strftime('%Y 道', dt)
		self.assertTrue(isinstance(s, str) and len(s) == 4 + 1 + 1)

		s = datetime.strftime('%Y ❗', dt)
		self.assertTrue(isinstance(s, str) and len(s) == 4 + 1 + 1)

		s = datetime.strftime('%Y 👨‍👩‍👧‍👦', dt)
		self.assertTrue(isinstance(s, str) and len(s) >= 4 + 1 + 1)

		s = datetime.strftime('%Y ƑÊẶṜ', dt)
		self.assertTrue(isinstance(s, str) and len(s) >= 4 + 1 + 4)

		# strfcal
		s = datetime.strfcal('%w', dt)
		self.assertTrue(isinstance(s, str) and len(s) > 0)

		s = datetime.strfcal('%W', dt)
		self.assertTrue(isinstance(s, str) and len(s) > 0)

		s = datetime.strfcal('%Y', dt)
		self.assertTrue(isinstance(s, str) and len(s) > 0)

		s = datetime.strfcal('%%', dt)
		self.assertEqual(s, '%')

		# weekcalendar
		year, week, weekday = datetime.weekcalendar(dt)
		self.assertTrue(isinstance(year, int) and 1900 < year and 3000 > year)
		self.assertTrue(isinstance(week, int) and 1 <= week and 53 >= week)
		self.assertTrue(isinstance(weekday, int) and 1 <= weekday and 7 >= weekday)

		# dates_for_week
		start, end = datetime.dates_for_week(year, week)
		self.assertTrue(isinstance(start, datetime.date))
		self.assertTrue(isinstance(end, datetime.date))
		self.assertTrue(start <= dt.date() and end >= dt.date())
