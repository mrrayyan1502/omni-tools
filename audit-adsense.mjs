import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 27 Core Tool Directories in OmniTechTools
const TOOL_SLUGS = [
  'base64-encoder-decoder',
  'color-palette-generator',
  'compound-interest-calculator',
  'css-box-shadow',
  'css-glassmorphism-generator',
  'diff-checker',
  'hash-generator',
  'image-compressor',
  'image-resizer',
  'inflation-calculator',
  'json-formatter',
  'json-to-csv',
  'jwt-decoder',
  'lorem-ipsum',
  'markdown-editor',
  'meta-tag-generator',
  'password-generator',
  'pdf-merge',
  'qr-code-generator',
  'regex-tester',
  'sql-formatter',
  'svg-blob-generator',
  'unit-converter',
  'unix-timestamp-converter',
  'url-encoder',
  'uuid-generator',
  'word-counter'
];

function extractProseWords(html) {
  // Strip non-prose blocks
  let text = html
    .replace(/<head[\s\S]*?<\/head>/gi, ' ')
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<svg[\s\S]*?<\/svg>/gi, ' ')
    .replace(/<aside[\s\S]*?<\/aside>/gi, ' ')   // Exclude global sidebar navigation
    .replace(/<footer[\s\S]*?<\/footer>/gi, ' ') // Exclude global footer links
    .replace(/<nav[\s\S]*?<\/nav>/gi, ' ')       // Exclude any standalone navigation
    .replace(/class=["'][^"']*a11y-panel[\s\S]*?<\/div>/gi, ' ') // Exclude accessibility widget
    .replace(/class=["'][^"']*cookie-notice[\s\S]*?<\/aside>/gi, ' ') // Exclude cookie banner
    .replace(/<[^>]+>/g, ' ')                   // Strip all HTML tags
    .replace(/&[a-z0-9#]+;/gi, ' ');             // Strip HTML entities

  // Remove code keywords and programming symbols
  const codePatterns = /\b(const|let|var|function|return|if|else|switch|case|break|for|while|do|try|catch|finally|import|export|null|undefined|true|false)\b/g;
  text = text.replace(codePatterns, ' ');
  text = text.replace(/[{}[\]();,.\/\\+*\-%&|^!~?:=<>"`]/g, ' ');

  // Extract actual readable words (2+ letters)
  const words = text.match(/\b[A-Za-z]{2,}\b/g) || [];
  return words;
}

const results = [];

for (const slug of TOOL_SLUGS) {
  // Check in root directory or src/ if present
  let htmlPath = path.join(__dirname, slug, 'index.html');
  if (!fs.existsSync(htmlPath)) {
    htmlPath = path.join(__dirname, 'src', slug, 'index.html');
  }

  if (!fs.existsSync(htmlPath)) {
    continue;
  }

  const rawHtml = fs.readFileSync(htmlPath, 'utf8');

  // 1. Prose Word Count (Min: 900)
  const words = extractProseWords(rawHtml);
  const wordCount = words.length;
  const wordPass = wordCount >= 900;

  // 2. Static HTML Table Check
  // Check if page contains static HTML <table> tag
  const hasTable = /<table[\s>]/i.test(rawHtml);

  // 3. FAQ Count (Min: 6 FAQs)
  const faqItemMatches = (rawHtml.match(/class=["'][^"']*faq-item[^"']*["']/gi) || []).length;
  const faqSchemaMatches = (rawHtml.match(/@type["']\s*:\s*["']Question["']/gi) || []).length;
  const faqQuestionHeaders = (rawHtml.match(/<h[345][^>]*>[^<]*\?[^<]*<\/h[345]>/gi) || []).length;
  const totalFaqs = Math.max(faqItemMatches, faqSchemaMatches, faqQuestionHeaders);
  const faqsPass = totalFaqs >= 6;

  // 4. Technical Guide / Formula / Syntax Section
  const hasGuideFormula = /\b(formula|equation|mathematical\s+model|methodology|algorithm|syntax\s+breakdown|technical\s+guide|how\s+to|in-depth\s+guide)\b/i.test(rawHtml);

  // Overall PASS requires all 4 criteria
  const isOverallPass = wordPass && hasTable && faqsPass && hasGuideFormula;

  // Format Tool Display Name
  const displayName = slug
    .split('-')
    .map(w => w.charAt(0).toUpperCase() + w.slice(1))
    .join('');

  results.push({
    name: displayName,
    slug: slug,
    words: wordCount,
    wordPass,
    table: hasTable ? 'YES' : 'NO',
    tablePass: hasTable,
    faqs: totalFaqs,
    faqsPass,
    formula: hasGuideFormula ? 'YES' : 'NO',
    formulaPass: hasGuideFormula,
    status: isOverallPass ? 'PASS' : 'FAIL'
  });
}

// Sort alphabetically
results.sort((a, b) => a.name.localeCompare(b.name));

// Print output table
console.log('\n========================================================================================================');
console.log('                 OMNITECHTOOLS.COM — ADSENSE "POLICE INSPECTOR" AUDIT REPORT                            ');
console.log('========================================================================================================');
console.log(
  'Tool / Calculator Name'.padEnd(32) + ' | ' +
  'Words'.padStart(7) + ' | ' +
  'Table'.padEnd(5) + ' | ' +
  'FAQs'.padStart(4) + ' | ' +
  'Formula'.padEnd(7) + ' | ' +
  'Status'.padEnd(6)
);
console.log('--------------------------------------------------------------------------------------------------------');

let passCount = 0;
let failCount = 0;

for (const r of results) {
  if (r.status === 'PASS') passCount++;
  else failCount++;

  const wordsStr = `${r.words}`.padStart(7);
  const tableStr = r.table.padEnd(5);
  const faqsStr = `${r.faqs}`.padStart(4);
  const formulaStr = r.formula.padEnd(7);
  const statusStr = r.status.padEnd(6);

  console.log(`${r.name.padEnd(32)} | ${wordsStr} | ${tableStr} | ${faqsStr} | ${formulaStr} | ${statusStr}`);
}

console.log('========================================================================================================');
console.log(`TOTAL TOOLS AUDITED: ${results.length}`);
console.log(`PASS: ${passCount}  |  FAIL: ${failCount}  (Failure Rate: ${((failCount / results.length) * 100).toFixed(1)}%)`);
console.log('========================================================================================================\n');
