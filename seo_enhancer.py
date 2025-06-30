#!/usr/bin/env python3
"""
SEO Enhancer Script
Adds structured data (JSON-LD) and meta tags to HTML files for better SEO.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

try:
    from bs4 import BeautifulSoup
    import click
except ImportError:
    print("Missing required dependencies. Please install them:")
    print("pip install beautifulsoup4 lxml click")
    sys.exit(1)


class SEOEnhancer:
    """Handles SEO enhancement for HTML files."""
    
    def __init__(self, html_file: Path):
        self.html_file = html_file
        self.soup = None
        self.load_html()
    
    def load_html(self):
        """Load and parse the HTML file."""
        try:
            with open(self.html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            self.soup = BeautifulSoup(content, 'lxml')
        except FileNotFoundError:
            click.echo(f"Error: File '{self.html_file}' not found.", err=True)
            sys.exit(1)
        except Exception as e:
            click.echo(f"Error reading file: {e}", err=True)
            sys.exit(1)
    
    def extract_existing_data(self) -> Dict[str, str]:
        """Extract existing data from HTML for pre-filling prompts."""
        data = {}
        
        # Try to extract title
        title_tag = self.soup.find('title')
        if title_tag:
            data['title'] = title_tag.get_text().strip()
        
        # Try to extract existing meta description
        meta_desc = self.soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            data['description'] = meta_desc.get('content', '')
        
        # Try to extract author from meta tag
        meta_author = self.soup.find('meta', attrs={'name': 'author'})
        if meta_author:
            data['author'] = meta_author.get('content', '')
        
        # Try to extract date from meta tag
        meta_date = self.soup.find('meta', attrs={'name': 'dcterms.date'})
        if meta_date:
            data['date_published'] = meta_date.get('content', '')
        
        return data
    
    def prompt_for_data(self) -> Dict[str, str]:
        """Interactive prompts to collect SEO data."""
        existing = self.extract_existing_data()
        
        click.echo("\n🚀 SEO Enhancement Setup")
        click.echo("=" * 50)
        
        data = {}
        
        # Article type
        article_types = ['TechArticle', 'BlogPosting', 'Article', 'NewsArticle']
        click.echo(f"\nAvailable article types: {', '.join(article_types)}")
        data['article_type'] = click.prompt(
            'Article type', 
            default='TechArticle',
            type=click.Choice(article_types, case_sensitive=False)
        )
        
        # Title/Headline
        data['headline'] = click.prompt(
            'Article headline/title',
            default=existing.get('title', '')
        )
        
        # Description
        data['description'] = click.prompt(
            'Article description (for meta description and structured data)',
            default=existing.get('description', '')
        )
        
        # Meta Description
        data['meta_description'] = click.prompt(
            'Meta description (leave empty to use article description)',
            default=data['description']
        )
        
        # Keywords
        data['keywords'] = click.prompt(
            'Keywords (comma-separated)',
            default=''
        )
        
        # Author info
        click.echo("\n📝 Author Information")
        data['author_name'] = click.prompt(
            'Author name',
            default=existing.get('author', 'Zach Mueller')
        )
        data['author_url'] = click.prompt(
            'Author URL',
            default='https://muellerzr.github.io'
        )
        
        # Publication date
        click.echo("\n📅 Publication Information")
        data['date_published'] = click.prompt(
            'Publication date (YYYY-MM-DD)',
            default=existing.get('date_published', datetime.now().strftime('%Y-%m-%d'))
        )
        
        # Optional: Modified date
        if click.confirm('Add modified date? (different from published date)'):
            data['date_modified'] = click.prompt(
                'Modified date (YYYY-MM-DD)',
                default=datetime.now().strftime('%Y-%m-%d')
            )
        
        # Publisher info
        click.echo("\n🏢 Publisher Information")
        data['publisher_name'] = click.prompt(
            'Publisher name',
            default="Zach Mueller's Blog"
        )
        data['publisher_url'] = click.prompt(
            'Publisher URL',
            default='https://muellerzr.github.io'
        )
        
        # Optional: Image
        if click.confirm('Add article image URL?'):
            data['image_url'] = click.prompt('Image URL')
        
        return data
    
    def create_json_ld(self, data: Dict[str, str]) -> str:
        """Create JSON-LD structured data."""
        json_ld = {
            "@context": "https://schema.org",
            "@type": data['article_type'],
            "headline": data['headline'],
            "description": data['description'],
            "author": {
                "@type": "Person",
                "name": data['author_name'],
                "url": data['author_url']
            },
            "publisher": {
                "@type": "Organization",
                "name": data['publisher_name'],
                "url": data['publisher_url']
            },
            "datePublished": data['date_published']
        }
        
        # Add optional fields
        if 'date_modified' in data:
            json_ld['dateModified'] = data['date_modified']
        
        if 'image_url' in data:
            json_ld['image'] = data['image_url']
        
        if data.get('keywords'):
            json_ld['keywords'] = data['keywords']
        
        return json.dumps(json_ld, indent=2)
    
    def add_json_ld(self, json_ld_content: str):
        """Add JSON-LD script to HTML head."""
        # Check if JSON-LD already exists
        existing_ld = self.soup.find('script', {'type': 'application/ld+json'})
        if existing_ld:
            click.echo("⚠️  Existing JSON-LD found. Replacing...")
            existing_ld.decompose()
        
        # Create new script tag
        script_tag = self.soup.new_tag('script')
        script_tag['type'] = 'application/ld+json'
        script_tag.string = json_ld_content
        
        # Add to head
        head = self.soup.find('head')
        if head:
            head.append(script_tag)
            click.echo("✅ JSON-LD structured data added")
        else:
            click.echo("⚠️  No <head> tag found!", err=True)
    
    def add_meta_tags(self, data: Dict[str, str]):
        """Add or update meta tags."""
        head = self.soup.find('head')
        if not head:
            click.echo("⚠️  No <head> tag found!", err=True)
            return
        
        # Add comment for organization
        comment = self.soup.new_string(
            "\n    <!-- Performance and SEO meta tags -->\n    "
        )
        head.append(comment)
        
        # Meta tags to add/update
        meta_tags = [
            ('description', data.get('meta_description', data['description'])),
            ('author', data['author_name']),
            ('keywords', data['keywords']),
            ('robots', 'index, follow'),
            ('viewport', 'width=device-width, initial-scale=1.0')
        ]
        
        for name, content in meta_tags:
            if content:  # Only add if content exists
                # Check if tag already exists
                existing_meta = head.find('meta', attrs={'name': name})
                if existing_meta:
                    existing_meta['content'] = content
                    click.echo(f"✅ Updated meta {name}")
                else:
                    meta_tag = self.soup.new_tag('meta')
                    meta_tag['name'] = name
                    meta_tag['content'] = content
                    head.append(meta_tag)
                    head.append('\n    ')
                    click.echo(f"✅ Added meta {name}")
        
        # Open Graph tags
        og_tags = [
            ('og:title', data['headline']),
            ('og:description', data.get('meta_description', data['description'])),
            ('og:type', 'article'),
            ('og:url', data['publisher_url']),
        ]
        
        if 'image_url' in data:
            og_tags.append(('og:image', data['image_url']))
        
        for property_name, content in og_tags:
            if content:
                existing_og = head.find('meta', attrs={'property': property_name})
                if existing_og:
                    existing_og['content'] = content
                else:
                    og_tag = self.soup.new_tag('meta')
                    og_tag['property'] = property_name
                    og_tag['content'] = content
                    head.append(og_tag)
                    head.append('\n    ')
                click.echo(f"✅ Added Open Graph {property_name}")
        
        # Twitter Card tags
        twitter_tags = [
            ('twitter:card', 'summary_large_image'),
            ('twitter:title', data['headline']),
            ('twitter:description', data.get('meta_description', data['description'])),
        ]
        
        if 'image_url' in data:
            twitter_tags.append(('twitter:image', data['image_url']))
        
        for name, content in twitter_tags:
            if content:
                existing_twitter = head.find('meta', attrs={'name': name})
                if existing_twitter:
                    existing_twitter['content'] = content
                else:
                    twitter_tag = self.soup.new_tag('meta')
                    twitter_tag['name'] = name
                    twitter_tag['content'] = content
                    head.append(twitter_tag)
                    head.append('\n    ')
                click.echo(f"✅ Added Twitter Card {name}")
    
    def save_html(self, output_file: Optional[Path] = None):
        """Save the enhanced HTML."""
        if output_file is None:
            output_file = self.html_file
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(str(self.soup))
            click.echo(f"💾 Enhanced HTML saved to: {output_file}")
        except Exception as e:
            click.echo(f"Error saving file: {e}", err=True)
            sys.exit(1)
    
    def enhance(self, output_file: Optional[Path] = None):
        """Main enhancement process."""
        click.echo(f"🔍 Processing: {self.html_file}")
        
        # Get data from user
        data = self.prompt_for_data()
        
        # Create and add JSON-LD
        json_ld = self.create_json_ld(data)
        click.echo("\n📋 Generated JSON-LD:")
        click.echo(json_ld)
        
        if click.confirm('\nProceed with adding SEO enhancements?'):
            self.add_json_ld(json_ld)
            self.add_meta_tags(data)
            self.save_html(output_file)
            click.echo("\n🎉 SEO enhancement completed!")
        else:
            click.echo("❌ Enhancement cancelled.")


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Enhance HTML files with SEO improvements (JSON-LD + meta tags)"
    )
    parser.add_argument(
        'html_file',
        type=Path,
        help='Input HTML file to enhance'
    )
    parser.add_argument(
        '-o', '--output',
        type=Path,
        help='Output file (defaults to overwriting input file)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be added without modifying file'
    )
    
    args = parser.parse_args()
    
    if not args.html_file.exists():
        click.echo(f"Error: File '{args.html_file}' does not exist.", err=True)
        sys.exit(1)
    
    enhancer = SEOEnhancer(args.html_file)
    
    if args.dry_run:
        data = enhancer.prompt_for_data()
        json_ld = enhancer.create_json_ld(data)
        click.echo("\n📋 JSON-LD that would be added:")
        click.echo(json_ld)
        click.echo("\n📝 Meta tags that would be added/updated:")
        for key, value in data.items():
            if key in ['description', 'meta_description', 'author_name', 'keywords']:
                click.echo(f"  - {key}: {value}")
    else:
        enhancer.enhance(args.output)


if __name__ == "__main__":
    main()
