import os
import re

seoMeta = {
    '/image-resizer/': { 'title': 'Free Image Resizer Online - Resize Photos Offline', 'desc': 'Resize images instantly in your browser. Custom width and height. 100% offline, private and free.' },
    '/pdf-merge/': { 'title': 'Free PDF Merger Online - Combine PDFs Offline', 'desc': 'Merge multiple PDF files into a single document securely. Works offline in your browser, no upload required.' },
    '/unit-converter/': { 'title': 'Free Online Unit Converter - Length, Weight, Temp', 'desc': 'Convert units instantly: length, weight, temperature, and digital storage. Fast, free and offline.' },
    '/youtube-thumbnail-downloader/': { 'title': 'YouTube Thumbnail Downloader - Free HD Image', 'desc': 'Download high-quality (HD) YouTube video thumbnails instantly. Just paste the video URL.' },
    '/': { 'title': 'OmniTools - Premium Free Creator & Developer Utility Hub', 'desc': 'OmniTools is a 100% free, private, and offline-first creator & developer utility hub. Generate custom QR codes, compress images, and more.' },
    '/qr-code-generator/': { 'title': 'Free QR Code Generator - Custom Styled QR Creator Online', 'desc': 'Create custom QR codes with logos, gradient fills & rounded dots. Free SVG/PNG export. Level H error correction for maximum scannability.' },
    '/image-compressor/': { 'title': 'Free Online Image Compressor - Compress JPEG/PNG/WebP', 'desc': 'Compress images online without losing quality. Support JPEG, PNG & WebP. 100% free, no upload required - works in your browser.' },
    '/css-glassmorphism-generator/': { 'title': 'CSS Glassmorphism Generator - Glass Effect CSS Online', 'desc': 'Create stunning glassmorphism CSS effects with our free generator. Adjust blur, opacity, background & export CSS instantly.' },
    '/json-formatter/': { 'title': 'Free JSON Formatter & Validator Online', 'desc': 'Beautify, minify & validate your JSON with syntax highlighting. 100% offline, your data never leaves your browser.' },
    '/svg-blob-generator/': { 'title': 'Free SVG Blob & Wave Generator - Organic Shapes', 'desc': 'Generate organic SVG blob shapes & waves with bezier curves. Custom colors, gradients & free SVG download.' },
    '/color-palette-generator/': { 'title': 'Color Palette Generator - WCAG Contrast Checker', 'desc': 'Generate beautiful color palettes with WCAG AA/AAA accessibility contrast checking. Analogous, monochromatic & complementary schemes.' },
    '/password-generator/': { 'title': 'Secure Password Generator - Strong Random Passwords', 'desc': 'Generate cryptographically secure passwords with entropy calculation. Custom length, symbols & time-to-crack estimates.' },
    '/base64-encoder-decoder/': { 'title': 'Free Base64 Encoder/Decoder Online', 'desc': 'Encode text or files to Base64 & decode back. 100% client-side, no server uploads. Supports Data URI embedding.' },
    '/meta-tag-generator/': { 'title': 'SEO Meta Tag Generator - Preview Google & Facebook', 'desc': 'Generate optimized meta tags with live Google SERP & Facebook preview. Check title length, description & Open Graph tags.' },
    '/compound-interest-calculator/': { 'title': 'Compound Interest Calculator - FIRE Calculator Online', 'desc': 'Calculate investment growth with compound interest. FIRE calculator with 4% safe withdrawal rate visualization.' },
    '/inflation-calculator/': { 'title': 'Inflation Calculator - Money Depreciation Calculator', 'desc': 'Calculate how inflation reduces your purchasing power over time. See your money\'s future value with historical inflation rates.' },
    '/jwt-decoder/': { 'title': 'Free JWT Decoder - Decode JSON Web Tokens Online', 'desc': 'Decode and inspect JWT tokens offline. View header & payload. 100% client-side, no data sent to servers.' },
    '/regex-tester/': { 'title': 'Online Regex Tester - JavaScript Regular Expressions', 'desc': 'Test JavaScript regular expressions in real-time. Match, replace & split with live results. Free online regex tester.' },
    '/sql-formatter/': { 'title': 'SQL Formatter - Beautify SQL Queries Online', 'desc': 'Format and beautify complex SQL queries for better readability. Supports SELECT, INSERT, UPDATE & more.' },
    '/markdown-editor/': { 'title': 'Live Markdown Editor Online - Write & Preview', 'desc': 'Write markdown with live HTML preview. Support headings, lists, code blocks & tables. Free online markdown editor.' },
    '/word-counter/': { 'title': 'Free SEO Word Counter - Count Words & Characters', 'desc': 'Count words, characters, sentences & reading time. Optimize your content for SEO with our free word counter.' },
    '/uuid-generator/': { 'title': 'Free UUID v4 Generator - Random Unique IDs', 'desc': 'Generate cryptographically random UUID v4 identifiers. Free, instant, no signup required.' },
    '/url-encoder/': { 'title': 'Free URL Encoder/Decoder Online', 'desc': 'Encode & decode URLs for safe web transmission. Handle special characters with percent-encoding.' },
    '/lorem-ipsum/': { 'title': 'Lorem Ipsum Generator - Free Dummy Text Generator', 'desc': 'Generate lorem ipsum dummy text for your designs. Custom paragraphs, words & HTML output.' },
    '/css-box-shadow/': { 'title': 'CSS Box Shadow Generator - Layered Shadows', 'desc': 'Create beautiful layered CSS box shadows with real-time preview. Multiple layers, custom colors & instant CSS export.' }
}

def modify_html(html, path, meta):
    # Base URL
    base_url = "https://www.omnitechtools.com"
    full_url = base_url + path
    
    # 1. Update <title>
    html = re.sub(r'<title>.*?</title>', f'<title>{meta["title"]}</title>', html, flags=re.IGNORECASE)
    
    # 2. Update <meta name="description">
    html = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{meta["desc"]}">', html, flags=re.IGNORECASE)
    
    # 3. Update <link rel="canonical">
    html = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{full_url}">', html, flags=re.IGNORECASE)
    
    # 4. Update <meta property="og:title">
    # Note: og:title might not exist, but usually we just replace the ones that do
    # Actually it's easier to use a robust replacement:
    
    # We will just inject og:title before og:description
    # Since index.html doesn't have og:title by default (it uses the main one), let's ensure it's there
    
    # Actually, we can just replace existing ones if they exist, or inject them.
    # The current index.html doesn't have <meta property="og:title">, it just relies on the main title. Wait, let me check.
    pass
    
    # Replace og:url
    html = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{full_url}">', html, flags=re.IGNORECASE)
    
    # Replace twitter:title
    html = re.sub(r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{meta["title"]}">', html, flags=re.IGNORECASE)
    
    # Replace twitter:description
    html = re.sub(r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{meta["desc"]}">', html, flags=re.IGNORECASE)

    # Let's also adjust the assets paths since the new index.html is in a subfolder!
    # Wait, the paths in index.html for app.js and style.css are: "style.css", "app.js". 
    # If the file is inside /image-resizer/index.html, "style.css" will resolve to /image-resizer/style.css which is a 404!
    # We MUST change "style.css" to "/style.css", "app.js" to "/app.js", "logo.png" to "/logo.png" etc.
    
    # Fix paths for subdirectories
    html = html.replace('href="style.css"', 'href="/style.css"')
    html = html.replace('src="app.js"', 'src="/app.js"')
    html = html.replace('src="logo.png"', 'src="/logo.png"')
    html = html.replace('src="og-image.png"', 'src="/og-image.png"')
    html = html.replace('href="manifest.json"', 'href="/manifest.json"')
    
    return html

def main():
    base_dir = r"C:\Users\qures\Downloads\apexkit-utility-hub"
    index_path = os.path.join(base_dir, "index.html")
    
    with open(index_path, "r", encoding="utf-8") as f:
        base_html = f.read()

    for path, meta in seoMeta.items():
        if path == '/': continue
        
        # Create directory
        folder_name = path.strip('/')
        target_dir = os.path.join(base_dir, folder_name)
        os.makedirs(target_dir, exist_ok=True)
        
        # Modify HTML
        new_html = modify_html(base_html, path, meta)
        
        # Write file
        out_path = os.path.join(target_dir, "index.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(new_html)
            
        print(f"Generated {out_path}")

if __name__ == "__main__":
    main()
