#!/usr/bin/env python
from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from apps.story.models import Chapter, Story
from optparse import make_option

import sys, re, csv, codecs

DATE_PATTERN = re.compile(r'\[(?P<date>\d{2}/[a-zA-Z]{3}/\d{4}:\d{2}:\d{2}:\d{2} \+\d{4})\]')
CHAPTER_PATTERN = re.compile(r' "(?P<method>GET|POST) /stories/chapter/(?P<chapter_id>\d+)/(\?|\s){1}')
MXIT_PATTERN = re.compile(r'MXit')

def get_chapter(line):
    return CHAPTER_PATTERN.search(line)

def chapters(lines):
    for line in lines:
        match = CHAPTER_PATTERN.search(line)
        if match:
            yield match, line

def is_mxit(line):
    return MXIT_PATTERN.search(line)

def get_timestamp(line):
    match = DATE_PATTERN.search(line)
    date = match.groupdict().get('date')
    return datetime.strptime(date, '%d/%b/%Y:%H:%M:%S +0000')

def print_summary(site, writer, results):
    for date, chapters in results.items():
        for chapter,pageviews in chapters.items():
            writer.writerow((site, date, chapter.story, chapter.title, pageviews))

def print_total_summary(site, writer, chapters):
    for chapter,pageviews in chapters.items():
        writer.writerow((site, chapter.story, chapter.title, pageviews))

unknown_chapter_cache = {}
def unknown_chapter(chapter_id):
    if chapter_id not in unknown_chapter_cache:
        unknown_chapter_cache[chapter_id] = Chapter(
            title="/stories/chapter/%s/" % chapter_id, 
            story=Story(title="Unknown")
        )
    
    return unknown_chapter_cache[chapter_id]
        

class Command(BaseCommand):
    help = 'Process logs and count chapter pageviews manually'
    option_list = BaseCommand.option_list + (
            make_option('--totals',
                dest='totals',
                action='store_true',
                default=False,
                help='Calculate totals since launch instead of per day'),
            )
    
    def handle(self, **options):
        if options.get('totals'):
            self.handle_totals_since_launch(**options)
        else:
            self.handle_per_day(**options)
    
    def handle_totals_since_launch(self, **options):
        mobi = {}
        mxit = {}
        reader = sys.stdin
        
        for line in reader:
            match = get_chapter(line)
            if match:
                chapter_id = match.groupdict().get('chapter_id')
                try:
                    chapter = Chapter.objects.get(pk=chapter_id)
                except Chapter.DoesNotExist:
                    chapter = unknown_chapter(chapter_id)
                if is_mxit(line):
                    mxit.setdefault(chapter, 0)
                    mxit[chapter] += 1
                else:
                    mobi.setdefault(chapter, 0)
                    mobi[chapter] += 1
        
        # UTF8 byte order mark
        sys.stdout.write(codecs.BOM_UTF8)
        writer = csv.writer(sys.stdout)
        writer.writerow(("Type", "Story", "Chapter", "Page views"))
        print_total_summary('MXit', writer, mxit)
        print_total_summary('Mobi', writer, mobi)
        
    
    def handle_per_day(self, **options):
        mobi = {}
        mxit = {}
        reader = sys.stdin
        
        for line in reader:
            match = get_chapter(line)
            if match:
                chapter_id = match.groupdict().get('chapter_id')
                try:
                    chapter = Chapter.objects.get(pk=chapter_id)
                except Chapter.DoesNotExist:
                    chapter = unknown_chapter(chapter_id)
                datetime = get_timestamp(line)
                date = datetime.date()
                mxit.setdefault(date, {})
                mobi.setdefault(date, {})
                if is_mxit(line):
                    mxit[date].setdefault(chapter, 0)
                    mxit[date][chapter] += 1
                else:
                    mobi[date].setdefault(chapter, 0)
                    mobi[date][chapter] += 1
        
        # UTF8 byte order mark
        sys.stdout.write(codecs.BOM_UTF8)
        writer = csv.writer(sys.stdout)
        writer.writerow(("Type", "Date", "Story", "Chapter", "Page views"))
        print_summary('MXit', writer, mxit)
        print_summary('Mobi', writer, mobi)
        
