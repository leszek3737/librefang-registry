# Clip Hand

Turns long-form video into viral short clips with captions and thumbnails.

## Configuration

| Field | Value |
|-------|-------|
| Category | `content` |
| Agent | `clip-hand` |
| Routing | `clip video`, `video transcription`, `subtitle extraction`, `download video`, `short clip` |

## Integrations

- **FFmpeg** -- Core video processing engine for clips, captions, and thumbnails.
- **FFprobe** -- Video metadata analyzer (ships with FFmpeg).
- **yt-dlp** -- Downloads videos from YouTube, Vimeo, Twitter, and 1000+ sites.

## Settings

- **Speech-to-Text Provider** -- `auto`, `whisper_local`, `groq_whisper`, `openai_whisper`, `deepgram`
- **Text-to-Speech Provider** -- `none`, `edge_tts`, `openai_tts`, `elevenlabs`
- **Publish Clips To** -- `local_only`, `telegram`, `whatsapp`, `both`
- **Telegram Bot Token / Chat ID** -- For Telegram publishing
- **WhatsApp Token / Phone ID / Recipient** -- For WhatsApp publishing

## Usage

```bash
librefang hand run clip
```
