#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import json
import html2text
import re
# from nltk.stem.snowball import RussianStemmer
from pymorphy2 import MorphAnalyzer
import codecs


class TextProcessor():

    def __init__(self, url=None):
        self.stopwords = []

        self.h = html2text.HTML2Text()
        self.h.ignore_links = True
        self.h.ignore_emphasis = True
        self.h.ignore_images = True
        self.h.body_width = 0

        # get stopwords
        if url is not None:
            f = codecs.open(url, encoding='utf-8')
            tempwords = f.readlines()

            for word in tempwords:
                self.stopwords.append(word.strip().lower())

    def smooth_date(self, cyr_date):
        months = ["january", "february", "march", "april", "may", "june",
                  "july", "august", "september", "october", "november",
                  "december"]
        mesiatsy = [u"январь", u"февраль", u"март", u"апрель", u"май", u"июнь",
                    u"июль", u"август", u"сентябрь", u"октябрь", u"ноябрь",
                    u"декабрь"]
        mesiatsy_short = [u"янв", u"фев", u"мар", u"апр", u"май",
                          u"июн", u"июл", u"авг", u"сент", u"окт", u"ноя",
                          u"дек"]
        import re
        lat_date = re.sub(u"via", "", cyr_date.lower())
        lat_date = re.sub(u"</*[a-z]>", "", lat_date)
        lat_date = re.sub(u"Posted on", "", lat_date)
        lat_date = re.sub(u"at", "", lat_date)
        lat_date = re.sub(u"\|", "", lat_date)
        lat_date = re.sub(u"\[", "", lat_date)
        lat_date = re.sub(u"\]", "", lat_date)
        lat_date = re.sub(u"\r", "", lat_date)
        lat_date = re.sub(u"\n", "", lat_date)
        lat_date = re.sub(r'(?u)(\d\d\d\d)(\d\d:\d\d)', r'\1 \2', lat_date)
        lat_date = re.sub(u"posted on", "", lat_date)
        for index in range(12):
            lat_date = re.sub(mesiatsy[index], months[index], lat_date)
            lat_date = re.sub(mesiatsy_short[index], months[index], lat_date)
        lat_date = re.sub(u"сен", "September", lat_date)
        return lat_date

    def unify_date(self, entry):
        from dateutil import parser
        import datetime

        try:
            date_string = entry["date"]
        except KeyError:
            print "No date in ", entry["url"]
            try:
                return entry["date"]
            except KeyError:
                return ""

        # convert date lists to string
        date_string = u''.join(unicode(r)
                               for v in date_string for r in v)

        def print_error():
            print "Unknown format:", entry["url"], entry["date"], date_string

        if len(date_string) < 8:
            print_error()

        date_string = self.smooth_date(date_string)

        DEFAULT_DATE = datetime.datetime(datetime.MINYEAR, 1, 1)
        try:
            date_string = str(parser.parse(
                date_string, default=DEFAULT_DATE, dayfirst=True))
        except UnicodeEncodeError:
            print "UUU"
            print_error()
            return entry["date"]
        except ValueError:
            print_error()
            return entry["date"]
        if date_string.startswith("0001"):
            print "Date Error!!!", entry["date"], "---->", date_string
        # else:
        #    print entry["date"], "---->", date_string
        return date_string

    def smooth(self, text, type=["NOUN"]):
        text = self.h.handle(text)

        morph = MorphAnalyzer()
        text = re.sub('(?u)-', ' ', text.lower())
        text = re.sub('(?u)([^\s\w]|_)+', '', text)
        text = re.sub('(?u)\d+', '', text)
        text = re.sub('[a-z]', '', text)

        result = []
        for word in text.split():
            # result.append(word.strip())
            p = morph.parse(word.strip())[0]
            # or p.tag.POS == "ADJF" or p.tag.POS == "ADJS":
            if "ALL" in type or p.tag.POS in type:
                if word not in self.stopwords:  # and len(word) > 1:
                    result.append(p.normal_form)
                else:
                    print "Stopword removed", word
        return result


def main(argv=None):

    if argv is None:
        argv = sys.argv

    if len(argv) < 2:
        print "Process raw HTML, filter stop words, etc."
        print "Usage: ./text.py $JSON_DIR"
        sys.exit(1)

    # t = TextProcessor("stop-words-russian.txt")
    # t = TextProcessor("namen")
    t = TextProcessor()

    dupes = {}

    word_count = 0

    for json_file in os.listdir(argv[1]):

        print
        print "File: ", json_file
        smooth_data = []
        if json_file.endswith(".json"):
            # get data
            entries = 0
            words = 0
            json_data = open(argv[1] + json_file)
            data = json.load(json_data)
            json_data.close()
            for entry in data:
                # smooth text
                result = t.smooth(entry["text"], type="ALL")
                words += len(result)
                result = " ".join(result)

                if entry["url"] in dupes:
                    print entry["url"], " is duplicate"
                    if len(dupes[entry["url"]]) < 5:
                        dupes[entry["url"]] = result
                        print "overwriting..."
                else:
                    dupes[entry["url"]] = result
                    entry["text"] = result
                    word_count += len(result)
                    smooth_data.append(entry)
                entries += 1

            print words, entries

            # save processed data
            with open(json_file.split(".")[0] + ".json", 'w') as outfile:
                json.dump(smooth_data, outfile)

            print "original lines", len(data)
            print "smoothed lines", len(smooth_data)
            print "word count", str(word_count)


if __name__ == "__main__":
    sys.exit(main())
