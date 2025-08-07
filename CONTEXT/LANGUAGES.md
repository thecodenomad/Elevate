Internationalization Plan and Supported Languages

Domain
- org.thecodenomad.elevate
- Wrap all user-visible strings:
  - Python: _("...")
  - Blueprint (.blp): _("...")
- Bind text domain at app init

Meson Integration
- Use i18n = import('i18n') and i18n.gettext('org.thecodenomad.elevate', languages: [
  'en', 'zh_CN', 'es', 'hi', 'ar', 'pt', 'fr', 'bn', 'ru', 'ja', 'ta', 'te', 'pa', 'id', 'vi', 'sw', 'th'
])
- Include Python, .ui/.blp, .desktop, .metainfo in extraction
- Install po/ catalogs

po/LINGUAS
- en zh_CN es hi ar pt fr bn ru ja ta te pa id vi sw th

Bootstrap Locales
- Initialize po/<lang>.po via msginit for each
- Set Project-Id-Version, Language, Plural-Forms

Schemas/Desktop/Metainfo
- Mark translatable strings; ensure xml:lang support

Runtime
- gettext.bindtextdomain('org.thecodenomad.elevate', LOCALE_DIR)
- gettext.textdomain('org.thecodenomad.elevate')
- Ensure GtkBuilder/Blueprint resources have translation-domain

CI
- Target to refresh POT and verify freshness
- msgfmt --check all .po

Docs
- CONTRIBUTING section with commands to add/update translations

QA
- Smoke test per language via LANG env or GSettings

Supported Languages
- English (en)
- Mandarin Chinese (zh_CN)
- Spanish (es)
- Hindi (hi)
- Arabic (ar)
- Portuguese (pt)
- French (fr)
- Bengali (bn)
- Russian (ru)
- Japanese (ja)
- Tamil (ta)
- Telugu (te)
- Punjabi (pa)
- Indonesian (id)
- Vietnamese (vi)
- Swahili (sw)
- Thai (th)
