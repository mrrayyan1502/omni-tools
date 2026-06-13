export default async function handler(req, res) {
    const { text, lang } = req.query;
    if (!text || !lang) {
        return res.status(400).json({ error: 'Missing text or lang' });
    }

    try {
        const url = `https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=${lang}&q=${encodeURIComponent(text)}`;
        const response = await fetch(url, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Referer': 'https://translate.google.com/'
            }
        });

        if (!response.ok) {
            return res.status(response.status).json({ error: 'Google TTS API failed' });
        }

        const buffer = await response.arrayBuffer();
        res.setHeader('Content-Type', 'audio/mpeg');
        res.setHeader('Cache-Control', 'public, max-age=86400'); // Cache for 1 day
        res.status(200).send(Buffer.from(buffer));
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
}
