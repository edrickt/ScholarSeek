import json
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_date
from search.models import arXiv  # Replace 'search' with the name of your app

class Command(BaseCommand):
    help = 'Import arXiv data from a JSON file'

    def handle(self, *args, **kwargs):
        with open('arxiv-metadata-oai-snapshot.json', 'r') as file:
            for line in file:
                try:
                    item = json.loads(line)  # Parse each line as a separate JSON object

                    # Update or create the arXiv object
                    arXiv.objects.update_or_create(
                        id=item['id'],
                        defaults={
                            'submitter': item.get('submitter', ''),
                            'authors': item.get('authors', ''),
                            'title': item.get('title', ''),
                            'comments': item.get('comments', ''),
                            'journal_ref': item.get('journal-ref', ''),
                            'doi': item.get('doi', ''),
                            'report_no': item.get('report-no', ''),
                            'categories': item.get('categories', ''),
                            'license': item.get('license', ''),
                            'abstract': item.get('abstract', ''),
                            'versions': item.get('versions', []),
                            'update_date': parse_date(item['update_date']) if item.get('update_date') else None,
                            'authors_parsed': item.get('authors_parsed', [])
                        }
                    )
                    self.stdout.write(self.style.SUCCESS(f"Imported {item['id']}"))

                except json.JSONDecodeError as e:
                    self.stderr.write(self.style.ERROR(f"Error decoding JSON on line: {line} - {e}"))
