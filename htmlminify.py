import htmlmin
from pathlib import Path

# Load your original HTML file
html_path = Path("blog/gradient_accumulation.html")  # Or whatever your file is called
html = html_path.read_text(encoding="utf-8")

# Minify it
minified = htmlmin.minify(
    html,
    remove_comments=True,
    remove_empty_space=True,
    remove_all_empty_space=True,
    reduce_boolean_attributes=True,
    remove_optional_attribute_quotes=False  # set True if you want aggressive minification
)

# Save to new file
minified_path = Path("gradient_accumulation.min.html")
minified_path.write_text(minified, encoding="utf-8")

print(f"✅ Minified HTML saved to: {minified_path}")
