#!/usr/bin/env python3
"""Build crawlable standalone pages from the original OmniTools source template."""

from copy import deepcopy
from datetime import date
from pathlib import Path
import json
import re

from lxml import etree, html

ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "site-template.html"
BASE_URL = "https://www.omnitechtools.com"

ROUTES = {
    "/": ("panel-dashboard", "Free Online Tools for Creators & Developers | OmniTools",
          "Free private browser-based tools for images, code, QR codes, documents and everyday calculations. No signup required."),
    "/qr-code-generator/": ("panel-qr-generator", "Free QR Code Generator with Logo & Custom Colours",
          "Create a custom QR code with your logo, colours and styles. Download a high-quality PNG or SVG without registration."),
    "/image-compressor/": ("panel-image-compressor", "Free Image Compressor – Compress JPG, PNG & WebP",
          "Compress JPG, PNG and WebP images securely in your browser. Reduce image size without uploading files or creating an account."),
    "/css-glassmorphism-generator/": ("panel-css-builder", "CSS Glassmorphism Generator – Create Glass Effects",
          "Create accessible glassmorphism CSS with live controls for blur, opacity, borders and backgrounds. Copy production-ready CSS."),
    "/compound-interest-calculator/": ("panel-finance-calc", "Compound Interest Calculator with Monthly Contributions",
          "Estimate investment growth, deposits and compound interest with adjustable contributions, rates and time periods."),
    "/json-formatter/": ("panel-json-formatter", "Free JSON Formatter, Validator & Beautifier Online",
          "Format, validate, beautify or minify JSON securely in your browser. Your JSON data is processed locally."),
    "/svg-blob-generator/": ("panel-svg-blob", "Free SVG Blob Generator – Create Organic Shapes",
          "Generate custom SVG blob shapes with gradients and adjustable complexity. Copy the SVG code or download the file."),
    "/color-palette-generator/": ("panel-color-palette", "Colour Palette Generator & WCAG Contrast Checker",
          "Generate harmonious colour palettes and check text contrast against WCAG AA and AAA thresholds."),
    "/password-generator/": ("panel-password-generator", "Secure Password Generator & Strength Checker",
          "Generate strong random passwords locally with custom length, characters and an easy-to-understand strength estimate."),
    "/base64-encoder-decoder/": ("panel-base64", "Free Base64 Encoder & Decoder Online",
          "Encode text or files to Base64 and decode Base64 locally in your browser. No input is uploaded to our server."),
    "/meta-tag-generator/": ("panel-meta-generator", "SEO Meta Tag Generator with Search Preview",
          "Create title, description, Open Graph and social meta tags with live search and sharing previews."),
    "/inflation-calculator/": ("panel-inflation-calc", "Inflation Calculator – Estimate Purchasing Power",
          "Estimate how inflation may affect future purchasing power using your chosen amount, rate and time period."),
    "/jwt-decoder/": ("panel-jwt-decoder", "Free JWT Decoder – Inspect JSON Web Tokens Locally",
          "Decode JWT headers and payloads locally in your browser for debugging. This tool does not verify token signatures."),
    "/markdown-editor/": ("panel-markdown-editor", "Free Live Markdown Editor & Preview",
          "Write Markdown and preview the formatted result live in your browser with no signup or document upload."),
    "/regex-tester/": ("panel-regex-tester", "Online JavaScript Regex Tester",
          "Test JavaScript regular expressions against sample text with live matches, flags and replacement output."),
    "/sql-formatter/": ("panel-sql-formatter", "Free SQL Formatter & Beautifier Online",
          "Format SQL queries for easier reading and debugging directly in your browser."),
    "/css-box-shadow/": ("panel-css-box-shadow", "CSS Box Shadow Generator with Live Preview",
          "Build layered CSS box shadows visually, preview the result and copy the generated CSS."),
    "/word-counter/": ("panel-word-counter", "Free Word & Character Counter with Reading Time",
          "Count words, characters, sentences and estimated reading time instantly in your browser."),
    "/lorem-ipsum/": ("panel-lorem-ipsum", "Free Lorem Ipsum Generator",
          "Generate placeholder paragraphs or words for mockups, layouts and design prototypes."),
    "/uuid-generator/": ("panel-uuid-generator", "Free UUID v4 Generator",
          "Generate cryptographically random UUID v4 identifiers locally in your browser."),
    "/url-encoder/": ("panel-url-encoder", "Free URL Encoder & Decoder Online",
          "Encode or decode URL components and special characters safely in your browser."),
    "/image-resizer/": ("panel-image-resizer", "Free Image Resizer – Resize Photos Locally",
          "Resize image width and height locally in your browser while preserving the aspect ratio when needed."),
    "/pdf-merge/": ("panel-pdf-merge", "Free PDF Merger – Combine PDFs Locally",
          "Combine multiple PDF files in your browser. Your documents are processed locally and are not uploaded."),
    "/unit-converter/": ("panel-unit-converter", "Free Unit Converter – Length, Weight & Temperature",
          "Convert common length, weight, temperature and digital storage units instantly."),
    "/diff-checker/": ("panel-diff-checker", "Free Online Diff Checker – Compare Text & Code Differences",
          "Compare two text or code files side-by-side online. Highlight character and line-by-line differences with additions and deletions instantly in your browser."),
    "/unix-timestamp-converter/": ("panel-unix-timestamp", "Unix Timestamp & Epoch Converter Online",
          "Convert Unix epoch timestamps to human-readable UTC and local dates. Live clock, millisecond support and relative time tracking."),
    "/hash-generator/": ("panel-hash-generator", "Cryptographic Hash Generator – SHA-256, SHA-512 & SHA-1",
          "Generate secure SHA-256, SHA-512, SHA-384 and SHA-1 checksums locally in your browser using the native Web Cryptography API."),
    "/json-to-csv/": ("panel-json-to-csv", "Free JSON to CSV Converter Online with Table Preview",
          "Convert JSON arrays into clean CSV spreadsheets and tables locally in your browser. Live table preview and instant download."),
    "/about/": ("panel-about", "About OmniTools – Private Browser-Based Utilities",
          "Learn why OmniTools provides practical, free utilities that process supported inputs locally in your browser."),
    "/privacy-policy/": ("panel-privacy", "Privacy Policy | OmniTools",
          "Read how OmniTools handles browser storage, analytics, advertising, contact details and locally processed tool inputs."),
    "/terms-of-service/": ("panel-terms", "Terms of Service | OmniTools",
          "Read the terms, acceptable-use rules and limitations that apply when using OmniTools."),
    "/contact/": ("panel-contact", "Contact OmniTools – Support & Feedback",
          "Contact OmniTools with a question, bug report, accessibility issue or feature request."),
    "/blog/": ("panel-blog", "OmniTools Guides – Web, Design, Privacy & Finance",
          "Practical guides for browser tools, web performance, design, digital privacy and personal-finance calculations."),
    "/blog/qr-codes-digital-marketing/": ("panel-blog-article-qr", "How to Use QR Codes in Digital Marketing",
          "Learn practical QR code design, placement and testing techniques for offline-to-online marketing."),
    "/blog/image-compression-performance/": ("panel-blog-article-compress", "Image Compression and Web Performance Guide",
          "Learn how image formats, dimensions and compression affect loading speed and Core Web Vitals."),
    "/blog/css-glassmorphism-trends/": ("panel-blog-article-glass", "Glassmorphism CSS: Design and Accessibility Guide",
          "Learn how to create glassmorphism interfaces while protecting readability, accessibility and performance."),
    "/blog/financial-independence-compound-growth/": ("panel-blog-article-fire", "Compound Growth and Financial Independence Guide",
          "Understand compound growth, regular contributions, inflation and the limits of retirement projections."),
    "/blog/developer-utilities-privacy/": ("panel-blog-article-privacy", "Client-Side Developer Tools and Data Privacy",
          "Understand the privacy benefits and limitations of browser-based developer utilities."),
    "/blog/json-formatting-guide/": ("panel-blog-article-json", "JSON Formatting and Validation Guide",
          "Learn common JSON syntax errors and how local formatting and validation tools help developers debug safely."),
    "/blog/svg-organic-blobs-design/": ("panel-blog-article-svg", "SVG Organic Blobs in Modern Web Design",
          "Learn how scalable SVG blob graphics work and how to use them without harming performance."),
    "/blog/ui-color-theory-palettes/": ("panel-blog-article-color", "UI Colour Theory and Accessible Palettes",
          "Learn colour harmony, the 60-30-10 guideline and accessible text contrast for interface design."),
    "/blog/secure-password-cryptography/": ("panel-blog-article-password", "How Secure Password Generators Work",
          "Learn about password length, entropy and cryptographically secure random generation."),
    "/blog/base64-encoding-explained/": ("panel-blog-article-base64", "Base64 Encoding Explained",
          "Learn what Base64 encoding does, why it increases data size and why it is not encryption."),
    "/blog/seo-meta-tags-guide/": ("panel-blog-article-meta", "SEO Meta Tags: Titles, Descriptions and Social Cards",
          "Learn how search titles, descriptions, canonical URLs and social sharing metadata work."),
    "/blog/inflation-wealth-depreciation/": ("panel-blog-article-inflation", "How Inflation Affects Purchasing Power",
          "Learn how inflation changes future purchasing power and how to interpret inflation-calculator estimates."),
}

H1S = {route: title.split(" | ")[0].split(" – ")[0] for route, (_, title, _) in ROUTES.items()}
H1S["/"] = "Free Online Tools for Creators and Developers"

GUIDE_SOURCES = {
    "panel-finance-calc": "panel-inflation-calc",
    "panel-json-formatter": "panel-meta-generator",
    "panel-svg-blob": "panel-finance-calc",
    "panel-color-palette": "panel-json-formatter",
    "panel-password-generator": "panel-svg-blob",
    "panel-base64": "panel-password-generator",
    "panel-meta-generator": "panel-color-palette",
}

TOOL_FAQS = {
    "/qr-code-generator/": [
        ("Is this QR code generator completely free and private?", "Yes. All QR codes are generated directly in your web browser using client-side JavaScript. No URLs, text, or uploaded logos are sent to or stored on any server."),
        ("Can I add a custom brand logo and change colours?", "Yes. You can customize background colours, foreground module colours, corner dot styles, and embed your logo while maintaining high error correction (Level H - 30% recovery) for reliable scanning."),
        ("What formats can I export my QR code in?", "You can download high-resolution PNG images for screens or scalable vector SVG files ideal for high-DPI print banners and packaging.")
    ],
    "/image-compressor/": [
        ("Are my images uploaded to any remote server during compression?", "No. OmniTools compresses JPG, PNG, and WebP files entirely within your browser using HTML5 Canvas and local WebAssembly. Your photos never leave your device."),
        ("Does compressing an image visibly degrade its quality?", "OmniTools uses visually lossless compression algorithms that remove unnecessary metadata and optimize color tables, reducing file size by up to 80% without noticeable quality loss."),
        ("What image formats are supported?", "You can compress JPG, JPEG, PNG, and modern WebP image formats with real-time file size comparison.")
    ],
    "/json-formatter/": [
        ("Is it safe to format confidential JSON files and API payloads here?", "Yes. OmniTools runs 100% client-side in browser memory. Your JSON data, tokens, and configuration keys are never transmitted over the internet or logged."),
        ("What features does this JSON Formatter provide?", "It provides instant syntax validation, beautification with 2 or 4 space indentation, minification, tree-view inspection, and one-click clipboard copying.")
    ],
    "/css-glassmorphism-generator/": [
        ("How is glassmorphism created in CSS?", "Glassmorphism combines CSS backdrop-filter (blur), semi-transparent background colors (RGBA), subtle borders, and soft shadows to create a modern frosted glass aesthetic."),
        ("Is the generated CSS compatible with all browsers?", "Yes, all modern evergreen browsers (Chrome, Edge, Safari, Firefox) support backdrop-filter. The tool includes necessary cross-browser declarations.")
    ],
    "/compound-interest-calculator/": [
        ("How does compound interest accelerate wealth growth?", "Compound interest calculates returns on both initial principal and accumulated interest over prior periods, creating an exponential growth curve over time."),
        ("Can I add regular monthly contributions to the calculation?", "Yes. You can set initial balance, estimated annual interest rate, compounding frequency, and regular monthly or annual deposits to see detailed growth schedules.")
    ],
    "/password-generator/": [
        ("How cryptographically secure are passwords created by OmniTools?", "OmniTools uses the browser's crypto.getRandomValues API, providing cryptographically strong pseudo-random numbers that resist brute-force and dictionary attacks."),
        ("Are generated passwords saved anywhere?", "Never. Passwords are generated exclusively on your local device. Once you close or reload the browser tab, the data is completely purged from memory.")
    ],
    "/base64-encoder-decoder/": [
        ("What is Base64 encoding typically used for?", "Base64 encodes binary or text data into safe ASCII string characters, widely used to embed inline images into HTML/CSS or transmit data across strict text protocols."),
        ("Is Base64 an encryption method?", "No. Base64 is an encoding scheme, not encryption. Anyone can decode a Base64 string without needing an encryption key.")
    ],
    "/meta-tag-generator/": [
        ("Which SEO and social meta tags are generated?", "The tool generates standard Title, Description, Viewport, Canonical, Robots, Open Graph (Facebook/LinkedIn), and Twitter Card meta tags."),
        ("Does this tool include live search previews?", "Yes, you can preview how your webpage will look as a Google search result, Facebook share preview, and Twitter card in real time.")
    ],
    "/inflation-calculator/": [
        ("How does inflation affect future purchasing power?", "Inflation erodes money's purchasing power over time, meaning future dollars will buy fewer goods and services than they do today."),
        ("What formula is used for inflation calculation?", "The calculator applies standard compound inflation rate formulas across your specified timeframe to compute future purchasing power equivalents.")
    ],
    "/jwt-decoder/": [
        ("Is it safe to inspect JWT tokens with OmniTools?", "Yes. Decoding happens entirely client-side in your browser. Tokens are never uploaded to any remote server or third-party service."),
        ("Does this tool verify JWT cryptographic signatures?", "This tool decodes and displays JSON header claims and payload data for debugging purposes. It does not verify or validate cryptographic signatures.")
    ],
    "/markdown-editor/": [
        ("Does the OmniTools Markdown editor support live preview?", "Yes. It offers a live split-screen editor with instant formatting, table rendering, task lists, code block syntax highlighting, and export to MD or HTML."),
        ("Are my drafts saved if I close the tab?", "Yes, active markdown drafts are automatically stored in your browser's localStorage so you can resume writing without losing work.")
    ],
    "/regex-tester/": [
        ("Which regex flavor is supported?", "OmniTools utilizes the native JavaScript ECMAScript RegExp engine, supporting standard flags like g (global), i (ignore case), m (multiline), and u (unicode)."),
        ("Does it support regex string replacement testing?", "Yes. You can test match patterns as well as substitution patterns with live highlighted replacement output.")
    ],
    "/sql-formatter/": [
        ("Which database dialects can this SQL formatter beautify?", "It formats standard ANSI SQL, PostgreSQL, MySQL, SQLite, and Microsoft SQL Server query syntax."),
        ("Does formatting alter database query execution?", "No. It only improves query readability by standardizing indentation, capitalization, and clause line breaks.")
    ],
    "/css-box-shadow/": [
        ("How do I make realistic CSS box shadows?", "Layering multiple subtle box-shadow declarations with soft blur radiuses and low opacity creates realistic, natural depth without harsh edges."),
        ("Can I copy the CSS code directly into my stylesheet?", "Yes. With one click you can copy production-ready CSS rules including inset and multi-layer box-shadow properties.")
    ],
    "/word-counter/": [
        ("What metrics does this word counter track?", "It counts words, total characters, characters without spaces, sentences, paragraphs, reading time, and speaking time."),
        ("Is there any text character limit?", "No. Because text is processed in your local browser memory, you can analyze articles or code documents of any length.")
    ],
    "/lorem-ipsum/": [
        ("What is Lorem Ipsum text used for?", "Lorem Ipsum is standard dummy placeholder text used by graphic designers, developers, and typesetters to focus on visual layout before final copy is ready."),
        ("Can I generate HTML-wrapped paragraphs?", "Yes. You can generate custom paragraph counts, word counts, or lists with optional HTML tag wrapping for easy copy-pasting.")
    ],
    "/uuid-generator/": [
        ("What is UUID version 4?", "UUID v4 is a 128-bit universally unique identifier generated using random bytes, ensuring unique identification across distributed systems."),
        ("Are the generated UUIDs random?", "Yes. They are generated using the Web Cryptography API, making accidental collision statistically negligible.")
    ],
    "/url-encoder/": [
        ("Why is URL encoding necessary?", "Certain characters like spaces, query delimiters, and ampersands have special meanings in URLs. Encoding converts them into safe percent-encoded escape sequences."),
        ("Can I decode percent-encoded URLs back to plain text?", "Yes, you can instantly toggle between URL encoding and decoding with one click.")
    ],
    "/image-resizer/": [
        ("Can I resize images proportionally?", "Yes. You can lock the aspect ratio to maintain dimensions automatically or enter custom width and height values in pixels."),
        ("Does image resizing require server uploads?", "No. Resizing takes place inside your browser using canvas elements, guaranteeing complete privacy.")
    ],
    "/pdf-merge/": [
        ("Can I merge confidential PDF documents safely?", "Yes. OmniTools merges PDF documents locally in your browser. No files are uploaded to our servers, ensuring total privacy for contracts and financial records."),
        ("Can I reorder PDF files before merging?", "Yes. You can arrange and reorder documents before downloading the combined single PDF file.")
    ],
    "/unit-converter/": [
        ("Which measurement units are supported?", "OmniTools converts length, mass/weight, temperature, digital data storage, area, volume, and speed units."),
        ("Are conversion calculations accurate?", "Yes, conversions use standard international SI and imperial conversion factors with high decimal precision.")
    ],
    "/color-palette-generator/": [
        ("How does the WCAG contrast checker help accessibility?", "It calculates relative luminance contrast between text and background colors against WCAG 2.1 AA (4.5:1) and AAA (7:1) readability requirements."),
        ("What color models can I copy?", "You can copy color codes in HEX, RGB, and HSL formats with a single click.")
    ],
    "/svg-blob-generator/": [
        ("What are SVG blobs used for?", "Organic SVG blob shapes add creative accents behind product screenshots, hero banners, and user profile avatars in modern web design."),
        ("Can I export the SVG markup directly?", "Yes. You can adjust complexity and smoothness, then copy the raw SVG vector code or download an .svg file.")
    ],
    "/diff-checker/": [
        ("Is my code or sensitive text uploaded to any server?", "No. All comparison and diff calculations occur 100% locally in your web browser. Nothing is ever sent to or stored on any server."),
        ("What is the difference between Side-by-Side and Unified view?", "Side-by-Side mode presents the original and modified texts in two parallel columns. Unified mode merges the changes into a single stream with + and - line markers, just like Git diffs."),
        ("Can I copy the diff results as a patch?", "Yes. You can click the Copy Diff Patch button to instantly copy standard unified diff text ready for code reviews or terminal patching.")
    ],
    "/unix-timestamp-converter/": [
        ("What is Unix Epoch time?", "Unix time is the number of elapsed seconds since 00:00:00 UTC on January 1, 1970. It provides a timezone-independent integer format widely used across operating systems, databases, and APIs."),
        ("Does this converter support milliseconds?", "Yes. The tool automatically detects whether your timestamp input is in seconds (10 digits) or milliseconds (13 digits) and converts it accurately."),
        ("What is the Year 2038 Problem?", "Legacy 32-bit systems store timestamps as signed 32-bit integers, which will overflow on January 19, 2038. Modern 64-bit systems are completely immune to this limitation.")
    ],
    "/hash-generator/": [
        ("Is it safe to compute hashes of sensitive data here?", "Yes. OmniTools computes all hashes locally in your browser using the native Web Cryptography API (crypto.subtle.digest). Your text or file never leaves your device."),
        ("Can a cryptographic hash be decrypted or reversed?", "No. Cryptographic hashes are mathematically one-way functions. It is practically impossible to invert a SHA-256 or SHA-512 digest back to the original text."),
        ("What is the difference between SHA-256 and SHA-1?", "SHA-256 provides 256 bits of cryptographic security and is the global industry standard. SHA-1 is an older 160-bit algorithm now deprecated for security certificates but still used for Git commit checksums.")
    ],
    "/json-to-csv/": [
        ("Are my JSON records uploaded to any server during conversion?", "No. The conversion executes 100% client-side in browser memory. Your private datasets and customer records are never uploaded or stored."),
        ("How does it handle nested objects and arrays in JSON?", "Nested objects and arrays are safely serialized into JSON strings within CSV cells to preserve structure when imported into Excel or Google Sheets."),
        ("Can I choose custom delimiters like semicolon or tab?", "Yes. You can select standard comma (,), semicolon (;), or tab (\\t) delimiters to fit your spreadsheet software.")
    ]
}


def clean_head(document, route, title, description):
    head = document.find(".//head")
    for script in list(head.findall("script")):
        text = script.text or ""
        src = script.get("src", "")
        if "seoMeta" in text or "googlesyndication" in src or "loadAdSense" in text:
            head.remove(script)

    def set_meta(selector, attrs):
        nodes = head.xpath(selector)
        node = nodes[0] if nodes else etree.SubElement(head, "meta")
        for key, value in attrs.items():
            node.set(key, value)

    title_nodes = head.findall("title")
    title_node = title_nodes[0] if title_nodes else etree.SubElement(head, "title")
    title_node.text = title
    for extra in title_nodes[1:]:
        head.remove(extra)

    canonical_url = BASE_URL + route
    canonicals = head.xpath("./link[@rel='canonical']")
    canonical = canonicals[0] if canonicals else etree.SubElement(head, "link")
    canonical.set("rel", "canonical")
    canonical.set("href", canonical_url)
    for extra in canonicals[1:]:
        head.remove(extra)

    set_meta("./meta[@name='description']", {"name": "description", "content": description})
    set_meta("./meta[@name='robots']", {"name": "robots", "content": "index,follow,max-image-preview:large"})
    set_meta("./meta[@property='og:title']", {"property": "og:title", "content": title})
    set_meta("./meta[@property='og:description']", {"property": "og:description", "content": description})
    set_meta("./meta[@property='og:url']", {"property": "og:url", "content": canonical_url})
    set_meta("./meta[@property='og:type']", {"property": "og:type", "content": "article" if route.startswith("/blog/") and route != "/blog/" else "website"})
    set_meta("./meta[@name='twitter:title']", {"name": "twitter:title", "content": title})
    set_meta("./meta[@name='twitter:description']", {"name": "twitter:description", "content": description})

    # Remove all existing ld+json scripts in head to avoid duplicates
    for old_json in list(head.xpath(".//script[@type='application/ld+json']")):
        head.remove(old_json)

    # Build Rich Interconnected Schema Graph
    graph = []
    if route == "/":
        graph.append({
            "@type": "Organization",
            "@id": f"{BASE_URL}/#organization",
            "name": "OmniTools",
            "url": f"{BASE_URL}/",
            "logo": {
                "@type": "ImageObject",
                "url": f"{BASE_URL}/og-image.png"
            },
            "description": "Privacy-focused, 100% browser-based utility tools for developers and creators.",
            "sameAs": [
                "https://github.com/omnitechtools",
                "https://twitter.com/omnitechtools"
            ]
        })
        graph.append({
            "@type": "WebSite",
            "@id": f"{BASE_URL}/#website",
            "url": f"{BASE_URL}/",
            "name": "OmniTools",
            "publisher": {"@id": f"{BASE_URL}/#organization"},
            "potentialAction": {
                "@type": "SearchAction",
                "target": f"{BASE_URL}/?q={{search_term_string}}",
                "query-input": "required name=search_term_string"
            }
        })
        graph.append({
            "@type": "WebPage",
            "@id": f"{canonical_url}#webpage",
            "url": canonical_url,
            "name": H1S[route],
            "description": description,
            "isAccessibleForFree": True,
            "isPartOf": {"@id": f"{BASE_URL}/#website"}
        })
    elif route.startswith("/blog/") and route != "/blog/":
        graph.append({
            "@type": "BlogPosting",
            "@id": f"{canonical_url}#article",
            "headline": H1S[route],
            "description": description,
            "mainEntityOfPage": canonical_url,
            "datePublished": "2026-08-01T00:00:00+00:00",
            "dateModified": "2026-09-18T00:00:00+00:00",
            "author": {
                "@type": "Organization",
                "name": "OmniTools Editorial Team",
                "url": f"{BASE_URL}/about/"
            },
            "publisher": {
                "@type": "Organization",
                "name": "OmniTools",
                "logo": {
                    "@type": "ImageObject",
                    "url": f"{BASE_URL}/og-image.png"
                }
            }
        })
    elif "panel-" in ROUTES[route][0] and route not in {"/about/", "/privacy-policy/", "/terms-of-service/", "/contact/", "/blog/"}:
        cat = "DeveloperApplication"
        if any(k in route for k in ["finance", "inflation", "interest", "counter", "calculator", "lorem", "converter"]):
            cat = "UtilitiesApplication"
        elif any(k in route for k in ["css", "color", "palette", "svg", "blob"]):
            cat = "DesignApplication"

        graph.append({
            "@type": "WebApplication",
            "@id": f"{canonical_url}#app",
            "name": H1S[route],
            "url": canonical_url,
            "description": description,
            "applicationCategory": cat,
            "operatingSystem": "All",
            "browserRequirements": "Requires JavaScript. Requires HTML5.",
            "isAccessibleForFree": True,
            "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "USD"
            }
        })

        faqs = TOOL_FAQS.get(route, [])
        if faqs:
            graph.append({
                "@type": "FAQPage",
                "@id": f"{canonical_url}#faq",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": q,
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": a
                        }
                    }
                    for q, a in faqs
                ]
            })
    else:
        graph.append({
            "@type": "WebPage",
            "@id": f"{canonical_url}#webpage",
            "url": canonical_url,
            "name": H1S[route],
            "description": description,
            "isAccessibleForFree": True
        })

    schema_data = {
        "@context": "https://schema.org",
        "@graph": graph
    }
    schema_node = etree.SubElement(head, "script", type="application/ld+json")
    schema_node.text = json.dumps(schema_data, ensure_ascii=False)


def make_links_crawlable(document):
    for node in document.xpath("//*[@onclick]"):
        onclick = node.get("onclick", "")
        match = re.search(r"(?:switchTab|routeTo)\([^'\"]*['\"]([^'\"]+)['\"]", onclick)
        if node.tag == "a" and node.get("href"):
            if match:
                tab = match.group(1)
                target = next((route for route, (panel, _, _) in ROUTES.items()
                               if panel == f"panel-{tab}"), None)
                if target:
                    node.set("href", target)
            node.attrib.pop("onclick", None)
        elif match:
            tab = match.group(1)
            target = next((route for route, (panel, _, _) in ROUTES.items()
                           if panel == f"panel-{tab}"), None)
            if target:
                node.attrib.pop("onclick", None)
                node.tag = "a"
                node.set("href", target)
                node.set("role", "link")
                node.attrib.pop("onkeydown", None)


def build(route, panel_id, title, description, source):
    document = html.document_fromstring(source)
    clean_head(document, route, title, description)
    main = document.get_element_by_id("contentViewport")
    panels = main.xpath("./section[contains(concat(' ', normalize-space(@class), ' '), ' tab-panel ')]")
    selected = document.get_element_by_id(panel_id)

    guide_source_id = GUIDE_SOURCES.get(panel_id)
    if guide_source_id:
        source_panel = document.get_element_by_id(guide_source_id)
        source_guides = source_panel.xpath(".//article[contains(@class,'seo-guide-section')]")
        target_guides = selected.xpath(".//article[contains(@class,'seo-guide-section')]")
        if source_guides and target_guides:
            target_guides[0].getparent().replace(target_guides[0], deepcopy(source_guides[0]))

    if panel_id == "panel-inflation-calc":
        source_panel = document.get_element_by_id("panel-blog-article-inflation")
        source_cards = source_panel.xpath(".//div[contains(@class,'glass-card')]")
        target_guides = selected.xpath(".//article[contains(@class,'seo-guide-section')]")
        if source_cards and target_guides:
            replacement = deepcopy(source_cards[0])
            replacement.set("class", "seo-guide-section glass-card")
            target_guides[0].getparent().replace(target_guides[0], replacement)

    if panel_id in {"panel-finance-calc", "panel-inflation-calc"}:
        workspaces = selected.xpath(".//*[contains(@class,'tool-workspace')]")
        if workspaces:
            disclaimer = html.fragment_fromstring(
                '<p class="calculator-disclaimer" role="note">'
                '<strong>Important:</strong> Results are illustrative estimates, not financial advice or a guarantee of future returns. '
                'Rates, inflation, taxes, fees and market performance can change.</p>'
            )
            workspaces[0].addnext(disclaimer)

    for panel in panels:
        if panel is not selected:
            main.remove(panel)
    selected.set("class", "tab-panel active")
    selected.attrib.pop("style", None)

    h1s = selected.xpath(".//h1")
    if not h1s:
        headings = selected.xpath(".//h2[contains(@class,'panel-title') or parent::*[contains(@class,'tool-header')] or parent::*[contains(@class,'panel-header')]]")
        if not headings:
            headings = selected.xpath(".//h2")
        if headings:
            headings[0].tag = "h1"
            h1s = [headings[0]]
    if h1s:
        for child in list(h1s[0]):
            h1s[0].remove(child)
        h1s[0].text = H1S[route]
        for extra in h1s[1:]:
            extra.tag = "h2"

    make_links_crawlable(document)
    for nav in document.xpath("//a[contains(@class,'nav-item')]"):
        classes = nav.get("class", "").replace(" active", "")
        if nav.get("href") == route:
            classes += " active"
            nav.set("aria-current", "page")
        else:
            nav.attrib.pop("aria-current", None)
        nav.set("class", classes.strip())

    return "<!DOCTYPE html>\n" + html.tostring(document, encoding="unicode", method="html")


def write_sitemap():
    today = date.today().isoformat()
    urls = "\n".join(
        f"  <url><loc>{BASE_URL}{route}</loc><lastmod>{today}</lastmod></url>"
        for route in ROUTES
    )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n</urlset>\n", encoding="utf-8"
    )


def main():
    if not TEMPLATE.exists():
        raise SystemExit("Missing site-template.html")
    source = TEMPLATE.read_text(encoding="utf-8")
    for route, (panel_id, title, description) in ROUTES.items():
        output = ROOT / "index.html" if route == "/" else ROOT / route.strip("/") / "index.html"
        output.parent.mkdir(parents=True, exist_ok=True)
        rendered = build(route, panel_id, title, description, source)
        rendered = "\n".join(line.rstrip() for line in rendered.splitlines()) + "\n"
        output.write_text(rendered, encoding="utf-8")
        print(f"Built {route}")
    write_sitemap()


if __name__ == "__main__":
    main()
