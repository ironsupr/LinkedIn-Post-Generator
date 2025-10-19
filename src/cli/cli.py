"""
Command-line interface for LinkedIn Post Generator.
"""

import click
import sys
import os
from datetime import datetime
from typing import Optional

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.generator.post_generator import PostGenerator
from src.aggregator.aggregator_manager import AggregatorManager
from src.database.database_manager import ContentDatabase
from src.formatter.post_formatter import PostFormatter


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """
    LinkedIn Post Generator - Automated content discovery and post creation.
    
    This tool helps you maintain a consistent LinkedIn presence by:
    - Fetching trending content from tech sources
    - Generating professional LinkedIn posts with AI
    - Managing drafts and tracking posted content
    """
    pass


@cli.command()
@click.option('--days', default=7, help='Number of days to look back for content')
def fetch(days):
    """
    Fetch new content from all sources.
    
    Fetches content from ArXiv, Hacker News, Dev.to, and Reddit,
    then saves to the database for post generation.
    """
    click.echo(click.style('\n' + '='*70, fg='cyan'))
    click.echo(click.style('FETCHING CONTENT', fg='cyan', bold=True))
    click.echo(click.style('='*70 + '\n', fg='cyan'))
    
    try:
        manager = AggregatorManager()
        results = manager.fetch_all_content(days_back=days)
        
        click.echo(click.style('\n' + '='*70, fg='green'))
        click.echo(click.style('FETCH SUMMARY', fg='green', bold=True))
        click.echo(click.style('='*70, fg='green'))
        
        for source, count in results.items():
            if count > 0:
                click.echo(click.style(f'  ✓ {source.capitalize():15s}: {count:3d} new items', fg='green'))
            else:
                click.echo(f'  - {source.capitalize():15s}: {count:3d} new items')
        
        total = sum(results.values())
        click.echo(click.style(f'\n  Total: {total} new items added to database', fg='green', bold=True))
        click.echo(click.style('='*70 + '\n', fg='green'))
        
    except Exception as e:
        click.echo(click.style(f'\n✗ Error: {str(e)}', fg='red'))
        sys.exit(1)


@cli.command()
@click.option('--type', 'post_type', type=click.Choice(['news', 'tip']), default='news',
              help='Type of post to generate')
@click.option('--category', type=click.Choice(['AI', 'DevOps', 'Cloud', 'DataScience']),
              help='Content category filter (for news posts)')
@click.option('--days', default=7, help='Days to look back for content')
@click.option('--save-file', is_flag=True, help='Save draft as text file')
def generate(post_type, category, days, save_file):
    """
    Generate a LinkedIn post.
    
    Creates a professional LinkedIn post using AI based on recent content
    or personal tips. Posts are saved as drafts in the database.
    """
    click.echo(click.style('\n' + '='*70, fg='cyan'))
    click.echo(click.style(f'GENERATING {post_type.upper()} POST', fg='cyan', bold=True))
    click.echo(click.style('='*70 + '\n', fg='cyan'))
    
    try:
        generator = PostGenerator()
        
        if post_type == 'news':
            result = generator.generate_news_post(category=category, days_back=days)
        else:
            # For tip posts
            result = generator.generate_tip_post()
        
        if not result:
            click.echo(click.style('\n✗ Failed to generate post', fg='red'))
            sys.exit(1)
        
        # Display the post
        click.echo(click.style('\n' + '='*70, fg='green'))
        click.echo(click.style('GENERATED POST', fg='green', bold=True))
        click.echo(click.style('='*70 + '\n', fg='green'))
        click.echo(result['content'])
        click.echo(click.style('\n' + '='*70, fg='green'))
        
        # Show metadata
        click.echo(click.style(f'\nPost ID: {result["id"]}', fg='yellow', bold=True))
        click.echo(f'Type: {result["type"]}')
        if 'source_title' in result:
            click.echo(f'Source: {result["source_title"][:60]}...')
            click.echo(f'Category: {result["source_category"]}')
        
        # Save to file if requested
        if save_file:
            filename = PostFormatter.save_to_markdown(result)
            click.echo(click.style(f'\n✓ Saved to: {filename}', fg='green'))
        
        click.echo(click.style('\n' + '='*70, fg='green'))
        click.echo(click.style('Next steps:', fg='yellow', bold=True))
        click.echo(f'  1. Review: python main.py review --id {result["id"]}')
        click.echo(f'  2. Copy to LinkedIn and post')
        click.echo(f'  3. Mark posted: python main.py mark-posted --id {result["id"]}')
        click.echo(click.style('='*70 + '\n', fg='green'))
        
    except Exception as e:
        click.echo(click.style(f'\n✗ Error: {str(e)}', fg='red'))
        import traceback
        traceback.print_exc()
        sys.exit(1)


@cli.command('list-drafts')
@click.option('--limit', default=10, help='Maximum number of drafts to show')
def list_drafts(limit):
    """
    List all draft posts.
    
    Shows all posts that haven't been posted to LinkedIn yet.
    """
    click.echo(click.style('\n' + '='*70, fg='cyan'))
    click.echo(click.style('DRAFT POSTS', fg='cyan', bold=True))
    click.echo(click.style('='*70 + '\n', fg='cyan'))
    
    try:
        db = ContentDatabase()
        db.connect()
        drafts = db.get_drafts()
        db.close()
        
        if not drafts:
            click.echo(click.style('No draft posts found.', fg='yellow'))
            click.echo('\nGenerate a new post with: python main.py generate')
            return
        
        # Show drafts (most recent first)
        for i, draft in enumerate(drafts[:limit], 1):
            click.echo(click.style(f'{i}. Post #{draft["id"]}', fg='green', bold=True))
            click.echo(f'   Type: {draft["post_type"]}')
            click.echo(f'   Created: {draft["created_date"]}')
            click.echo(f'   Preview: {draft["content"][:80]}...')
            click.echo()
        
        if len(drafts) > limit:
            click.echo(click.style(f'... and {len(drafts) - limit} more drafts', fg='yellow'))
        
        click.echo(click.style(f'Total: {len(drafts)} draft(s)', fg='cyan', bold=True))
        click.echo(click.style('\n' + '='*70 + '\n', fg='cyan'))
        
    except Exception as e:
        click.echo(click.style(f'\n✗ Error: {str(e)}', fg='red'))
        sys.exit(1)


@cli.command()
@click.option('--id', 'post_id', required=True, type=int, help='Post ID to review')
@click.option('--save', is_flag=True, help='Save to file')
def review(post_id, save):
    """
    Review a specific draft post.
    
    Displays the complete post content for review before posting to LinkedIn.
    """
    try:
        db = ContentDatabase()
        db.connect()
        post = db.get_post_by_id(post_id)
        db.close()
        
        if not post:
            click.echo(click.style(f'\n✗ Post #{post_id} not found', fg='red'))
            sys.exit(1)
        
        # Display post
        click.echo(click.style('\n' + '='*70, fg='cyan'))
        click.echo(click.style(f'POST #{post_id} - {post["post_type"].upper()}', fg='cyan', bold=True))
        click.echo(click.style('='*70 + '\n', fg='cyan'))
        
        click.echo(post['content'])
        
        click.echo(click.style('\n' + '='*70, fg='cyan'))
        click.echo(f'Created: {post["created_date"]}')
        click.echo(f'Status: {post["status"]}')
        
        if post['posted_date']:
            click.echo(f'Posted: {post["posted_date"]}')
        
        # Save to file if requested
        if save:
            post_data = {
                'id': post['id'],
                'content': post['content'],
                'type': post['post_type'],
                'created_date': post['created_date']
            }
            filename = PostFormatter.save_to_markdown(post_data)
            click.echo(click.style(f'\n✓ Saved to: {filename}', fg='green'))
        
        click.echo(click.style('\n' + '='*70, fg='cyan'))
        
        if post['status'] == 'draft':
            click.echo(click.style('\nNext steps:', fg='yellow', bold=True))
            click.echo('  1. Copy the post above')
            click.echo('  2. Post to LinkedIn')
            click.echo(f'  3. Run: python main.py mark-posted --id {post_id}')
        
        click.echo(click.style('='*70 + '\n', fg='cyan'))
        
    except Exception as e:
        click.echo(click.style(f'\n✗ Error: {str(e)}', fg='red'))
        sys.exit(1)


@cli.command('mark-posted')
@click.option('--id', 'post_id', required=True, type=int, help='Post ID to mark as posted')
@click.option('--engagement', type=int, help='LinkedIn engagement score (likes + comments)')
def mark_posted(post_id, engagement):
    """
    Mark a draft post as posted to LinkedIn.
    
    Updates the post status in the database and optionally records engagement metrics.
    """
    try:
        db = ContentDatabase()
        db.connect()
        
        # Check if post exists
        post = db.get_post_by_id(post_id)
        if not post:
            click.echo(click.style(f'\n✗ Post #{post_id} not found', fg='red'))
            db.close()
            sys.exit(1)
        
        # Mark as posted
        db.mark_post_posted(post_id, engagement)
        db.close()
        
        click.echo(click.style(f'\n✓ Post #{post_id} marked as posted!', fg='green', bold=True))
        
        if engagement:
            click.echo(f'Engagement: {engagement} (likes + comments)')
        
        click.echo(click.style('\nGreat job posting consistently! 🎉\n', fg='green'))
        
    except Exception as e:
        click.echo(click.style(f'\n✗ Error: {str(e)}', fg='red'))
        sys.exit(1)


@cli.command()
def stats():
    """
    Show statistics about content and posts.
    
    Displays database statistics including content items, generated posts,
    and posting activity.
    """
    click.echo(click.style('\n' + '='*70, fg='cyan'))
    click.echo(click.style('LINKEDIN POST GENERATOR - STATISTICS', fg='cyan', bold=True))
    click.echo(click.style('='*70 + '\n', fg='cyan'))
    
    try:
        db = ContentDatabase()
        db.connect()
        stats = db.get_statistics()
        
        # Content statistics
        click.echo(click.style('📊 Content Database:', fg='yellow', bold=True))
        click.echo(f'  Total content items: {stats["total_content_items"]}')
        click.echo(f'  Last fetch: {stats["last_fetch"]}')
        
        # Post statistics
        click.echo(click.style('\n📝 Generated Posts:', fg='yellow', bold=True))
        click.echo(f'  Total posts: {stats["total_posts"]}')
        click.echo(f'  Posted: {stats["posted_count"]}')
        click.echo(f'  Drafts: {stats["draft_count"]}')
        
        # Calculate posting rate
        if stats["posted_count"] > 0:
            click.echo(click.style(f'\n✓ You\'ve posted {stats["posted_count"]} times!', fg='green'))
        else:
            click.echo(click.style('\n📌 No posts published yet. Generate and post your first one!', fg='yellow'))
        
        db.close()
        
        click.echo(click.style('\n' + '='*70 + '\n', fg='cyan'))
        
    except Exception as e:
        click.echo(click.style(f'\n✗ Error: {str(e)}', fg='red'))
        sys.exit(1)


@cli.command('preview-content')
@click.option('--days', default=7, help='Days to look back')
@click.option('--limit', default=10, help='Number of items to show')
@click.option('--category', type=click.Choice(['AI', 'DevOps', 'Cloud', 'DataScience']),
              help='Filter by category')
def preview_content(days, limit, category):
    """
    Preview top-ranked content without generating a post.
    
    Shows the highest-ranked content items available for post generation.
    """
    try:
        generator = PostGenerator()
        
        click.echo(click.style('\n' + '='*70, fg='cyan'))
        click.echo(click.style(f'TOP {limit} CONTENT ITEMS', fg='cyan', bold=True))
        if category:
            click.echo(click.style(f'Category: {category}', fg='cyan'))
        click.echo(click.style('='*70 + '\n', fg='cyan'))
        
        generator.preview_top_content(days_back=days, n=limit)
        
    except Exception as e:
        click.echo(click.style(f'\n✗ Error: {str(e)}', fg='red'))
        sys.exit(1)


@cli.command()
@click.option('--id', 'post_id', required=True, type=int, help='Post ID to export')
@click.option('--format', 'file_format', type=click.Choice(['txt', 'md', 'both']), default='md',
              help='Export format (txt, md, or both)')
@click.option('--filename', help='Custom filename (without extension)')
def export(post_id, file_format, filename):
    """
    Export a post to text or markdown file.
    
    Saves the post content to a file in the drafts/ directory.
    Useful for backing up posts or editing offline.
    """
    try:
        db = ContentDatabase()
        db.connect()
        post = db.get_post_by_id(post_id)
        db.close()
        
        if not post:
            click.echo(click.style(f'\n✗ Post #{post_id} not found', fg='red'))
            sys.exit(1)
        
        # Prepare post data
        post_data = {
            'id': post['id'],
            'content': post['content'],
            'type': post['post_type'],
            'created_date': post['created_date']
        }
        
        # Add source info if available (fetch from content_items)
        if post.get('source_content_id'):
            db.connect()
            source_content = db.get_content_by_id(post['source_content_id'])
            db.close()
            if source_content:
                post_data['source_title'] = source_content['title']
                post_data['source_url'] = source_content['url']
                post_data['source_category'] = source_content['category']
        
        click.echo(click.style('\n' + '='*70, fg='cyan'))
        click.echo(click.style(f'EXPORTING POST #{post_id}', fg='cyan', bold=True))
        click.echo(click.style('='*70 + '\n', fg='cyan'))
        
        saved_files = []
        
        # Export as markdown
        if file_format in ['md', 'both']:
            if filename:
                md_filename = f"drafts/{filename}.md"
            else:
                from datetime import datetime
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                md_filename = f"drafts/post_{post_id}_{post['post_type']}_{timestamp}.md"
            
            md_path = PostFormatter.save_to_markdown(post_data, md_filename)
            saved_files.append(('Markdown', md_path))
        
        # Export as text
        if file_format in ['txt', 'both']:
            if filename:
                txt_filename = f"drafts/{filename}.txt"
            else:
                from datetime import datetime
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                txt_filename = f"drafts/post_{post_id}_{post['post_type']}_{timestamp}.txt"
            
            # Create simple text file
            import os
            os.makedirs('drafts', exist_ok=True)
            with open(txt_filename, 'w', encoding='utf-8') as f:
                f.write(f"LinkedIn Post #{post_id}\n")
                f.write(f"Type: {post['post_type']}\n")
                f.write(f"Created: {post['created_date']}\n")
                f.write(f"\n{'-' * 70}\n\n")
                f.write(post['content'])
            
            saved_files.append(('Text', txt_filename))
        
        # Show results
        for format_name, filepath in saved_files:
            click.echo(click.style(f'✓ {format_name} file saved:', fg='green'))
            click.echo(f'  {filepath}')
        
        click.echo(click.style('\n' + '='*70, fg='green'))
        click.echo(click.style('Export complete!', fg='green', bold=True))
        click.echo(click.style('='*70 + '\n', fg='green'))
        
    except Exception as e:
        click.echo(click.style(f'\n✗ Error: {str(e)}', fg='red'))
        import traceback
        traceback.print_exc()
        sys.exit(1)


@cli.command()
def workflow():
    """
    Display the recommended posting workflow.
    
    Shows step-by-step instructions for using the tool effectively.
    """
    click.echo(click.style('\n' + '='*70, fg='cyan'))
    click.echo(click.style('📋 LINKEDIN POSTING WORKFLOW', fg='cyan', bold=True))
    click.echo(click.style('='*70 + '\n', fg='cyan'))
    
    click.echo(click.style('Step 1: Fetch Content (Once Daily)', fg='yellow', bold=True))
    click.echo('  $ python main.py fetch')
    click.echo('  Gets latest content from all sources\n')
    
    click.echo(click.style('Step 2: Generate Post (2x per Week)', fg='yellow', bold=True))
    click.echo('  $ python main.py generate --type news')
    click.echo('  Creates a LinkedIn-ready post\n')
    
    click.echo(click.style('Step 3: Review Draft', fg='yellow', bold=True))
    click.echo('  $ python main.py review --id 1')
    click.echo('  Check the generated post\n')
    
    click.echo(click.style('Step 4: Export (Optional)', fg='yellow', bold=True))
    click.echo('  $ python main.py export --id 1 --format md')
    click.echo('  Save as text/markdown file for editing or backup\n')
    
    click.echo(click.style('Step 5: Post to LinkedIn', fg='yellow', bold=True))
    click.echo('  Copy the post content and publish on LinkedIn\n')
    
    click.echo(click.style('Step 6: Mark as Posted', fg='yellow', bold=True))
    click.echo('  $ python main.py mark-posted --id 1')
    click.echo('  Track your posting activity\n')
    
    click.echo(click.style('Optional: Check Stats', fg='yellow', bold=True))
    click.echo('  $ python main.py stats')
    click.echo('  View your progress\n')
    
    click.echo(click.style('='*70, fg='cyan'))
    click.echo(click.style('💡 Tip:', fg='green', bold=True) + ' Run commands with --help for more options')
    click.echo(click.style('='*70 + '\n', fg='cyan'))


if __name__ == '__main__':
    cli()
