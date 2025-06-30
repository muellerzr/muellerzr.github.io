import argparse
from bs4 import BeautifulSoup
from pathlib import Path

def convert_to_semantic(input_path: str) -> None:
    """Convert HTML to use semantic elements and add schema.org metadata.
    
    Args:
        input_path: Path to input HTML file
    """
    html_path = Path(input_path)
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")

    content_wrapper = soup.find("div", {"id": "quarto-content"}) or soup.find("div", {"class": "page-columns"})

    if content_wrapper:
        main = soup.new_tag("main")
        article = soup.new_tag("article")
        article.extend(content_wrapper.contents)

        # Wrap each H2 and its following content into <section>
        for h2 in article.find_all("h2"):
            section = soup.new_tag("section")
            section.append(h2.extract())

            next_sibling = section.contents[-1].find_next_sibling()
            while next_sibling and next_sibling.name != "h2":
                following = next_sibling.find_next_sibling()
                section.append(next_sibling.extract())
                next_sibling = following

            article.append(section)

        # Replace original wrapper
        content_wrapper.clear()
        main.append(article)
        content_wrapper.insert_after(main)
        content_wrapper.decompose()

        # Add JSON-LD schema.org metadata
        head = soup.find("head")
        if head:
            json_ld = soup.new_tag("script", type="application/ld+json")
            json_ld.string = """
            {
              "@context": "https://schema.org",
              "@type": "TechArticle",
              "headline": "Gradient Accumulation in PyTorch",
              "description": "Learn how to implement gradient accumulation in PyTorch to reduce memory, speed training, and maintain performance.",
              "author": { "@type": "Person", "name": "Zach Mueller" },
              "datePublished": "2025-06-27",
              "mainEntityOfPage": "https://muellerzr.github.io/blog/gradient_accumulation.html"
            }
            """
            head.append(json_ld)

        # Save final HTML
        output_path = html_path.parent / (html_path.stem + ".min.html")
        output_path.write_text(str(soup), encoding="utf-8")
        print(f"✅ Saved to: {output_path}")
    else:
        print("❌ Could not find the content wrapper.")

def main():
    parser = argparse.ArgumentParser(description="Convert HTML to use semantic elements")
    parser.add_argument("input_file", help="Path to input HTML file")
    args = parser.parse_args()
    
    convert_to_semantic(args.input_file)

if __name__ == "__main__":
    main()
