# Решения по дизайну сайта

Журнал решений (ADR) по оформлению anvilarth.github.io: главная, Blog, Projects и
общая шапка статей. Формат тот же, что в `tg_channel/playbooks/adr`: живой документ,
записи не удаляются, номера не переиспользуются, статус меняется на месте с
пометкой `Update YYYY-MM-DD:`. Решения по тексту отдельных статей живут в
`tg_channel/posts/<topic>/decisions.md`, не здесь.

Разделы: **Accepted** — действующие решения (ограничения для правок);
**Приёмы** — как это устроено и какими значениями сделано; **Proposed** — ждут
автора; **Superseded / rejected** — что пробовали и почему отказались.

`By:` — кто решил: `author-request` (просьба автора, исполнение агента),
`author-approved-text` (автор одобрил именно этот вид в превью, «всё мне нравится»),
`author` (автор отверг вариант), `claude-code/claude-opus-5-5` (решение агента,
принято без отдельного ревью).

Источник всех записей: сессия редизайна 2026-11-21,
https://claude.ai/code/session_015qHmLfjM9adPzL2HUNR6qt. Превью в артефактах:
главная https://claude.ai/artifact/8t19D4TbjnmW5GerLvCiLi, Projects
https://claude.ai/artifact/RdkjaNmybRFspXQFXB4atE, Blog
https://claude.ai/artifact/XFg5wHHyRYd6fzvukkAs15, статья
https://claude.ai/artifact/9CJFGeXGJvccYPshSxdF7F. Опубликовано коммитами
`2fb65d2`…`16462ba`. Задача в бэклоге: `assistant/vault/backlog/not-started/Унифицировать шапку сайта anvilarth.github.io.md`.

## Accepted

### D001 · Одна шапка на всех страницах
- Status: accepted · By: author-request · Date: 2026-11-21 · Scope: `pages/*.html`, `templates/longread/nav.html`, `site_nav` в `builder/build_publication.py`
- Context: при переходе между страницами шапка менялась (Projects / Blog / Contact на главной, «Back to main» на остальных).
- Update 2026-11-21: «andrei filatov позицию меняет в на основной projects и blog» — шапка на всех страницах одной ширины (960px) и высоты (62px), логотип стоит в одной точке до пикселя на главной, Blog, Projects и в статьях, на десктопе и на телефоне.
- Decision: везде логотип слева, справа Projects, Blog (текущий раздел подчёркнут цветом акцента), переключатель темы; в статьях ещё иконка языка (D006). Пункта Contact нет, «Main» и иконок у пунктов нет — на главную ведёт логотип.
- Consequences: новая страница или статья получает ту же шапку, а не свою. Значения — в «Приёмы → Шапка».

### D002 · Логотип в исходном шрифте
- Status: accepted · By: author-request · Date: 2026-11-21 · Scope: `.nav-logo` на всех страницах
- Context: «давай для andrei filatov в шапке оставим исходный шрифт»
- Decision: «andrei filatov» — JetBrains Mono 14px, вес 400, на всех страницах.
- Update 2026-11-21: «давай вернем projects blog такой же шрифт как у andrei filatov» — пункты меню Projects / Blog тоже JetBrains Mono 14px, 400. Моноширинный шрифт — только в шапке (логотип и меню).
- Consequences: при унификации шрифтов шапку не трогать; font-face JetBrains Mono не удалять. Supersedes S07.

### D003 · Один раздел Blog для постов и докладов
- Status: accepted · By: author-request · Date: 2026-11-21 · Scope: главная, `pages/blog.html`
- Context: «it shouldn't be fourth item we should unite blog and writing and talks», «назови Blog»
- Decision: «Writing and talks» и Blog — один раздел под названием Blog. Доклады лежат на странице Blog в общем списке с постами, с тегом Talk; на главной заголовок «Blog», описание «Long-reads and talks on diffusion post-training, GPUs and inference.»
- Consequences: новый доклад добавляется карточкой на `pages/blog.html` (формат в «Приёмы → Лента и карточки»).

### D004 · Без указаний языка и без «~» в списках
- Status: accepted · By: author-request · Date: 2026-11-21 · Scope: карточки Blog, лента главной
- Context: «убери ru/en», «убери in English and Russian. любое вот такое указание языка», «в blog убери ~ около времени»
- Decision: в видимом тексте главной, Blog и Projects нет «RU/EN», «in English and Russian» и подобного; время чтения пишется «33 min read», без «~».
- Consequences: внутри самих статей «~» пока остаётся — мета-строку и переводы собирает `tg_channel` (D012).

### D005 · Без подзаголовков на Blog и Projects
- Status: accepted · By: author-request · Date: 2026-11-21 · Scope: `pages/blog.html`, `pages/projects.html`
- Context: «Foundation models, generation platforms, papers and tools — things shipped, not just started вот этот текст давай вообще уберем», «и gap убери оставшийся», «и в blog … тоже самое»
- Decision: на обеих страницах только заголовок h1, от него до списка 48px, без пустого места на месте подзаголовка.
- Consequences: не возвращать лид-абзац под h1 без просьбы автора.

### D006 · Смена языка в статьях — иконка в шапке, без перезагрузки
- Status: accepted · By: author-request · Date: 2026-11-21 · Scope: `templates/longread/lang-toggle.js`, `style.css`, `site_nav`
- Context: пилюля RU/EN, текст «RU / EN» и ссылка в мета-строке отвергнуты (R001–R003); «в шапке стало мало места»; «1. переход между версиями давай сделаем, и в шапке больше мместа сделаем».
- Decision: иконка языка (Lucide «languages») рядом с кнопкой темы, подсказка «Читать на русском» / «Read in English». Клик: текст гаснет, язык меняется на месте, тот же абзац остаётся на том же месте экрана, адрес меняется на `.ru.html` / `.html`. Иконка выбрана вместо объединённого меню «тема + язык», чтобы язык менялся в одно нажатие.
- Consequences: новая статья должна держать `setLang`, `btn-ru`, `btn-en`, `theme-btn` (см. `templates/longread/README.md`). Алгоритм — в «Приёмы → Смена языка».

### D007 · Переключатель языка — настоящая ссылка
- Status: accepted · By: claude-code/claude-opus-5-5 · Date: 2026-11-21 · Scope: `site_nav` в `builder/build_publication.py`
- Context: правила репозитория — переключатели языка работают без JS, статический HTML несёт язык страницы.
- Decision: сборка запекает иконку в обе версии: на `.html` ссылка ведёт на `.ru.html` с подписью «Читать на русском», на `.ru.html` — наоборот; `hreflang`, `lang`, `data-language` выставлены. JS перехватывает только обычный клик; клик с модификатором и страница без `setLang` идут по ссылке. Пункты меню на `.ru.html` — «Проекты», «Блог».

### D008 · Высота шапки статьи как на остальных страницах
- Status: accepted · By: author-request · Date: 2026-11-21 · Scope: `.post-nav`
- Context: «размер шапки как будто маловат»
- Decision: шапка статьи 62px, как на главной, Blog и Projects (61px + линия), ширина 960px, как у Blog.

### D009 · Контакты одной фразой в первом экране главной
- Status: accepted · By: author-request · Date: 2026-11-21 · Scope: `pages/index.html`
- Context: «вместо telegram channel сделай ссылку на мой телеграм», «давай это сразу в начало перенесем», «давай просто напиши, что готов помочь с консультацией и если просто хотите пообщаться, то пишите», «вот эта часть визуально красивая?» → «давай»
- Decision: одно предложение серым под описанием, над Resume: «Happy to help with a consultation, or just write to talk: email or Telegram.» Оранжевые только две ссылки (email → mailto, Telegram → https://t.me/anvilarth). Иконка Telegram в ряду соцсетей ведёт на канал, подсказка «Telegram channel». Нижней секции Contact и пункта Contact в шапке нет.
- Consequences: Supersedes S08, S09.

### D010 · Главная из трёх экранов, Projects — момент photo-chapters
- Status: accepted · By: author-approved-text · Date: 2026-11-21 · Scope: `pages/index.html`, `static/moments/`
- Update 2026-11-21: «на основной странице projects прокрутка может больше места занимать» — колонка главной расширена с 820 до 960px (на линию шапки), картинка проекта занимает 68% строки: на 1440×900 615×410 вместо 489×326.
- Context: «мне не нравится что на первом экране типо projects как будто отрезанные», «хочется по сути иметь 3 слайда, про меня projects, blogs», «ну хочется чтобы было 3 как бы секции и такие переходы между ними» → «всё мне нравится»
- Decision: три экрана — про меня, Projects, Blog; каждая секция ровно в высоту окна. Переход между ними держит Projects: секция стоит на месте, по прокрутке каждая следующая картинка проекта открывается поверх предыдущей (момент photo-chapters из taste skill). Над названием проекта строка «год · место» из `pages/projects.html`. В Blog на главной три пункта: два новейших поста и доклад.
- Consequences: Supersedes S03, S04. Не добавлять scroll-snap, «доводчики» и появление секций при прокрутке (D016). Значения — в «Приёмы → Главная».

### D011 · Обложки проектов — серия плоских иллюстраций 3:2
- Status: accepted · By: author-request · Date: 2026-11-21 · Scope: `static/img/projects/*.jpg`, `templates/project-covers.py`
- Context: «теперь картинки кропнуто выглядят», «xlabs lora кропнутое изображение», «в projects сделай норм картинки где их нет»
- Decision: все 10 обложек — одна серия иллюстраций в палитре сайта, каждая показывает идею проекта, без текста и логотипов. 1536×1024, без кропа и без размытых полей, на странице `object-fit: contain` на фоне цвета бумаги.
- Consequences: Supersedes S05. Новая обложка генерируется тем же STYLE; файлы заменяются по тем же адресам (URL картинок публичны).

### D012 · Тексты статей из tg_channel здесь не правятся
- Status: accepted · By: claude-code/claude-opus-5-5 · Date: 2026-11-21 · Scope: `posts/` (DPO, RL for Diffusion)
- Decision: оформление статей меняется только через `templates/longread/` и `builder/`; содержимое и мета-строка статей — в `tg_channel`.
- Consequences: убрать «~» внутри статей — задача для сборщика статей в `tg_channel`.

### D013 · Черновики не публикуются вместе с правками оформления
- Status: accepted · By: claude-code/claude-opus-5-5 · Date: 2026-11-21 · Scope: git, публикация
- Context: в локальном master лежали неопубликованные коммиты черновика `posts/image-dedup` (с файлом `DRAFT`), а на GitHub появились новые коммиты.
- Decision: правки оформления перенесены поверх `origin/master` и опубликованы отдельно (`git push origin <sha>:master`); коммиты черновика оставлены локально поверх них.
- Consequences: перед пушем смотреть `git log origin/master..master` и не публиковать то, о чём не просили.

### D014 · Шрифты: два семейства и один моноширинный логотип
- Status: accepted · By: author-approved-text · Date: 2026-11-21 · Scope: главная, Blog, Projects
- Context: «и почему Andrei Filatov с засечками сделано», «не мне именно имя хочется шрифт поменять», «выбери сам шрифт по скиллам»; taste skill: на странице не больше двух шрифтов, подписи не меньше 13px, без капса.
- Decision: заголовки секций и страниц — Literata (`--serif`); основной текст — Inter (`--sans`); имя на главной — Inter 600, трекинг −0,04em; пункты шапки — JetBrains Mono 14px (D002, до 2026-11-21 были Literata 16px/500); мелкий текст (Resume, футер, строка «For agents and LLMs») — Inter 13–14px; `--mono` на страницах указывает на Inter. Моноширинный — только шапка (D002).
- Consequences: Supersedes S06. Новый шрифт не добавлять без просьбы автора.

### D015 · Отступы по одной шкале, межсекционный отступ меньше, чем в skill
- Status: accepted · By: author-request · Date: 2026-11-21 · Scope: главная, Blog, Projects
- Context: «как будто gap есть много? что думаешь?» → «давай по скиллу поменяем»
- Decision: все отступы из шкалы 4–8–12–16–24–32–48–64–96. Из taste skill взято всё, кроме межсекционного отступа: у skill 120/72px (рассчитан на сайты компаний), у нас 48px. От шапки до имени 48px, низ первого экрана 64px, от заголовка секции до содержимого 48px (на телефоне 32px).

### D016 · Без появления при прокрутке и без scroll-snap
- Status: accepted · By: claude-code/claude-opus-5-5 · Date: 2026-11-21 · Scope: все страницы
- Context: taste skill прямо запрещает fade-in секций и «доводчики» прокрутки; движение допускается в одном-двух «моментах» на страницу.
- Decision: прокрутка обычная; единственное движение на главной — момент photo-chapters (D010), плюс микро-ховеры (линия под ссылкой, цвет пунктов меню). При `prefers-reduced-motion` анимаций нет.
- Consequences: Supersedes S02.

### D017 · Ссылки «See all …» в строке заголовка секции
- Status: accepted · By: author-request · Date: 2026-11-21 · Scope: главная
- Context: «All projects All posts and talks это вообще красивый переход?», «спроси у taste skill как это лучше сделать», «давай так попробуем»
- Decision: заголовок секции слева, ссылка справа на той же строке (схема `section-head--row` из taste skill): «See all projects», «See all posts». Подпись — глагол + что получишь; «More», «Learn more», «Explore» не используются. Ссылки цвета текста с тонкой линией; оранжевые — только ссылки внутри текста.
- Consequences: Supersedes S01.

### D018 · Taste skill — главный источник правил, Impeccable — только проверка
- Status: accepted · By: author-request · Date: 2026-11-21 · Scope: все дизайн-решения сайта
- Context: «taste skill что говорит?», «Impeccable этот скилл еще глянь», «давай по скиллу поменяем»
- Decision: структуру, шапку, ссылки, шрифты и движение сверяем с taste skill (`design-taste-frontend`). Impeccable используется как аудит собранных страниц, его визуальный стиль (Chakra Petch, мелкий капс JetBrains Mono) не берём. Где правило skill рассчитано на сайты компаний, отступаем и записываем почему (D015).

### D019 · Порядок работы над дизайном
- Status: accepted · By: author-request · Date: 2026-11-21 · Scope: процесс
- Context: «давай обновим claude artifacts», «сделай под них артефакты», «давай теперь всё пушить»
- Decision: правки сначала показываются в превью (артефакты claude.ai) и не трогают репозиторий; публикация только по слову автора («пушь»). Перенос в репозиторий — правками исходников (`pages/`, `templates/`, `builder/`), без артефактных костылей. Проверка — собранный `dist` на ширине 1440 и 390 (шапку ещё 360), потом живой сайт с `?v=` после деплоя.

## Приёмы

Как устроено то, что решено выше, и какими значениями. Меняя значение, меняй и эту запись.

### Шапка (D001, D002, D008)
- Одна линия: `nav .c` / `.post-nav-inner` — `max-width:960px`, поля 28px, высота строки 29px, отступы 16px; итого 62px. Логотип на 1440 стоит на x=268, y=19,5 на всех страницах. Блок «Shared header» в конце `<style>` каждой страницы и в конце `templates/longread/style.css` — меняй их вместе.
- Логотип: `font-family:'JetBrains Mono'…; 14px; 400; letter-spacing:-.01em; line-height:22px`, знак-«точки» слева, зазор 9px (в статьях знак скрыт только ≤379px, где не помещается иконка языка).
- Пункты: тот же JetBrains Mono 14px/400, цвет `--ts`, при наведении `--accent`; зазор 24px (≤600px 16px; ≤380px 12px и 12px между логотипом и меню; в статьях ≤440px 12px, ≤400px 10px).
- Текущая страница: `aria-current="page"`, цвет `--t`, подчёркивание `--accent` толщиной 2px со сдвигом 8px.
- Статьи: `.post-nav` с отступами 16px и внутренней высотой 29px (итого 62px), ширина 960px. Старый `.lang-switch` с `#btn-ru` / `#btn-en` остаётся в разметке с `hidden` — на эти кнопки опирается `setLang` статей.
- Иконка языка `.lang-toggle`: 16px, отступ 6px с таким же отрицательным полем; при `pointer: coarse` 14px (цель 44px); `touch-action: manipulation`, `:focus-visible` контур цвета акцента.

### Смена языка (D006, D007)
- Разметку иконки добавляет `site_nav()` при сборке каждой языковой версии; скрипт `templates/longread/lang-toggle.js` встраивается перед `</body>`.
- Клик без модификаторов: запомнить первый видимый под шапкой элемент (`header h1`, `#article h2/h3/p/li/figure/.equation`) и его отступ сверху → класс `html.lang-swap` (opacity 0 на `header`, `#article`, `.post-toc`, 0,16 с) → `setLang(to)` → прокрутка на разницу, чтобы элемент вернулся на прежнее место → `history.replaceState` на адрес другой версии → обновить подпись иконки, пункты меню и блок «В статье» → снять класс в следующем кадре.
- При `prefers-reduced-motion` всё то же без затухания. Без `setLang` клик идёт по ссылке.
- `language-links.js` дописывает к ссылке текущий якорь раздела, поэтому и обычный переход сохраняет место.

### Главная (D009, D010, D014, D015, D016, D017)
- Колонка: `main.c{max-width:960px}` — на линии шапки; описания постов в ленте `max-width:68ch`.
- Секции: `main>section{height:100svh}` (на телефоне 100lvh), отступы 120/72px, первый экран 112/64px (на телефоне 96/48px), содержимое по центру по вертикали, без линий между секциями.
- Строка заголовка: `.section-head{display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;gap:4px 24px}`; ссылка `.link` 15px цвета текста, линия `--ll` снизу, при наведении слева направо прорисовывается линия цвета текста (`background-size` 0 → 100%, 0,25 с).
- Контакты: `.hero-note` 16px, цвет `--ts`, ссылки `--accent` с полупрозрачной линией.
- Момент photo-chapters: секция `#projects[data-moment="photo-chapters"]` со списком `ol.mo-ph__list > li.mo-ph__ch` (`figure.mo-ph__pic > img`, `p.mo-ph__meta` «2026 · Krea», `h3 > a`, `p`). JS и CSS момента — `static/moments/` (не `assets/`, чтобы не пересечься с `/assets/<slug>/` статей), подключение — `modulepreload` + `<script type="module" src="moments/moments.js">`, классы `mo-js` / `mo-safe` на `html`. Десктоп (≥900px): картинка 3:2 на 68% ширины слева (не выше `(100svh − 300px)·1,5`), текст справа; телефон: картинка целиком, текст под ней.
- Описания постов в Blog на телефоне обрезаются до двух строк (`-webkit-line-clamp:2`).

### Лента и карточки (D003, D004)
- Лента главной: `latest_feed(..., count=2)` берёт два новейших поста из карточек `pages/blog.html`; доклад вписан руками в `pages/index.html` сразу после `<div class="feed-posts">`. Внешние ссылки (YouTube) лента пропускает.
- Карточка поста: `«October 2026 · 33 min read»`. Карточка доклада: `«2026 · Talk · 35 min · Data Fest, Belgrade»`, теги «Video Generation», «Talk».

### Страницы Blog и Projects (D005, D011)
- Projects: `.c{max-width:960px}` — сетка на линии шапки (3 колонки на десктопе). Blog — колонка 720px (P03).
- Шапка страницы: `main>header::after{display:none}`, `padding-bottom:48px`, у одиночного h1 нет нижнего поля.
- Обложки: `.proj-img{aspect-ratio:3/2; object-fit:contain; background:#f6e4d2}`, у `img` всегда `width="1536" height="1024"` и `alt`, описывающий иллюстрацию («Illustration: …»).
- Генерация: `templates/project-covers.py` хранит STYLE (плоская редакционная иллюстрация, бумага #f3ede4, ржавый #b5452b, тёмный #1f1a17, песок #d9c7ad, бирюза #3f6f6a, персик #f0c7a8, без текста и лиц) и SUBJECTS — идею каждого проекта. Картинки генерировались через Codex, скрипт сохраняет их без кропа, при другой пропорции дополняет до 3:2 цветом бумаги.

### Перенос превью в репозиторий (D019)
- Превью собирались скриптами из `dist/` (вырезался каркас страницы, ссылки переписывались на артефакты, убиралась аналитика). При переносе эти костыли не переносятся: только правки исходников.
- Чек-лист перед пушем: `uv run builder build`, `uv run builder check`, `git diff --cached --check`; браузер на 1440 и 390 — нет горизонтальной прокрутки, картинки грузятся, момент живой, во всех статьях иконка языка работает в обе стороны и формулы KaTeX на месте; `git fetch` и сверка с `origin/master`.
- После пуша: `gh run watch` по workflow Site (Build, Deploy, IndexNow, sitemap), затем живые страницы с `?v=`.

## Proposed (ждут автора)

### P01 · Мелкий моноширинный текст в статьях
- Status: proposed · By: claude-code/claude-opus-5-5 · Date: 2026-11-21 · Scope: футер «Designed & built by…», строка «For agents and LLMs…» в статьях
- Decision: на главной, Blog и Projects эти строки уже набраны Inter 13px; в статьях они пока моноширинные. Нужно решение автора: убрать или уменьшить.

### P02 · Портрет в первом экране главной
- Status: proposed · By: claude-code/claude-opus-5-5 · Date: 2026-11-21 · Scope: первый экран главной
- Context: «чо думаешь? картинки в начале нехватает?»
- Decision: агент предложил небольшое живое фото 140–180px справа от имени (на телефоне над именем), без обработки нейросетью. Нужна фотография от автора; решения нет.

### P03 · Выравнивание Blog по линии логотипа и отступ до списка
- Status: proposed · By: claude-code/claude-opus-5-5 · Date: 2026-11-21 · Scope: `pages/blog.html`
- Decision: колонка Blog уже шапки и начинается правее логотипа; от заголовка до первого поста 32px, на Projects 48px. Так в исходном дизайне; выровнять — по слову автора.

## Superseded / rejected

### S01 · Ссылки «All projects» / «All posts and talks» под секциями
- Status: superseded by D017 · Date: 2026-11-21
- Context: «All projects All posts and talks это вообще красивый переход?» Вариант с числом («All 10», «All 7») тоже не взят: taste skill требует глагол.

### S02 · Плавное появление секций при прокрутке
- Status: superseded by D016 · Date: 2026-11-21
- Context: «а можешь тогда плавные переходы между секциями сделать?» — сделано (подъём на 24px за 0,7 с), затем убрано: taste skill это запрещает, переход взял на себя момент photo-chapters.

### S03 · Три «слайда» со сжатыми карточками
- Status: rejected · By: author · Date: 2026-11-21
- Context: «нет адаптации к разным размера окна», «теперь картинки кропнуто выглядят», «сейчас полная хуета»
- Decision: отвергнуто: подгонка всех карточек в один экран (картинки 16:6, сетка 2×2, скрытие описаний на низких окнах, доводка прокрутки). Не возвращаться к «всё влезает в экран за счёт сжатия».

### S04 · Проекты списком с миниатюрами
- Status: superseded by D010 · Date: 2026-11-21
- Context: после отката слайдов — список с картинкой 200px слева; «ну хочется чтобы было 3 как бы секции и такие переходы между ними».

### S05 · Настоящие картинки моделей с релизов
- Status: superseded by D011 · Date: 2026-11-21
- Context: Krea 3, Krea 2, XLabs LoRA, Kandinsky — генерации с официальных страниц релизов, квадратные с размытыми полями; у шести проектов оставались фото-натюрморты. «xlabs lora кропнутое изображение», «в projects сделай норм картинки где их нет».

### S06 · Schibsted Grotesk для имени
- Status: superseded by D014 · Date: 2026-11-21
- Context: выбран агентом по taste skill, на странице получилось три шрифта; заменён на Inter.

### S07 · Логотип шрифтом Literata / Inter
- Status: superseded by D002 · Date: 2026-11-21
- Context: моноширинный логотип пытались убрать вместе с остальным моноширинным текстом; «давай для andrei filatov в шапке оставим исходный шрифт».

### S08 · Контакты блоком из пяти строк
- Status: superseded by D009 · Date: 2026-11-21
- Context: фраза, адрес почты, «Telegram @anvilarth», Resume и иконки отдельными строками; «вот эта часть визуально красивая?» — блок читался как список и дважды вёл в Telegram.

### S09 · Пункт Contact в шапке и секция Contact внизу главной
- Status: superseded by D009 · Date: 2026-11-21
- Context: контакты переехали в первый экран, отдельная секция и пункт меню стали не нужны.

### R001 · Пилюля RU/EN в шапке статьи
- Status: rejected · By: author · Date: 2026-11-21
- Context: «вот это еще некрасиво выглядит придумай как красиво сделать»
- Decision: отвергнуто, заменено иконкой (D006).

### R002 · Текст «RU / EN» через черту в шапке
- Status: rejected · By: author · Date: 2026-11-21
- Context: «RU EN не знаю как этот нативно переход сделать»
- Decision: отвергнуто, заменено иконкой (D006).

### R003 · Ссылка на другой язык в мета-строке статьи
- Status: rejected · By: author · Date: 2026-11-21
- Context: «ну не хуйня»
- Decision: отвергнуто; язык переключается из шапки (D006).

### R004 · Ползунок «EN RU» и общее меню «тема + язык»
- Status: rejected · By: author-request · Date: 2026-11-21
- Context: «в шапке стало мало места» — ползунок самый широкий; общее меню добавляет лишний клик. Выбрана иконка (D006).
