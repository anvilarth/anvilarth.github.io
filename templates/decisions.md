# Решения по дизайну сайта

Журнал решений (ADR) по оформлению anvilarth.github.io: главная, Blog, Projects и
общая шапка статей. Формат тот же, что в `tg_channel/playbooks/adr`: живой документ,
записи не удаляются, номера не переиспользуются, статус меняется на месте с
пометкой `Update YYYY-MM-DD:`. Решения по тексту отдельных статей живут в
`tg_channel/posts/<topic>/decisions.md`, не здесь.

`By:` — кто решил: `author-request` (просьба автора, исполнение агента),
`author-approved-text` (автор одобрил именно этот вид в превью),
`claude-code/claude-opus-5-5` (решение агента, принято без отдельного ревью).

Источник всех записей D001–D013: сессия редизайна 2026-11-21,
https://claude.ai/code/session_015qHmLfjM9adPzL2HUNR6qt (превью в артефактах:
главная https://claude.ai/artifact/8t19D4TbjnmW5GerLvCiLi, Projects
https://claude.ai/artifact/RdkjaNmybRFspXQFXB4atE, Blog
https://claude.ai/artifact/XFg5wHHyRYd6fzvukkAs15, статья
https://claude.ai/artifact/9CJFGeXGJvccYPshSxdF7F). Опубликовано коммитами
`2fb65d2`…`16462ba`.

## Accepted

### D001 · Одна шапка на всех страницах
- Status: accepted · By: author-request · Date: 2026-11-21 · Scope: `pages/*.html`, `templates/longread/nav.html`, `site_nav` в `builder/build_publication.py`
- Context: при переходе между страницами шапка менялась (Projects / Blog / Contact на главной, «Back to main» на остальных).
- Decision: везде логотип слева, справа Projects, Blog (текущий раздел подчёркнут цветом акцента), переключатель темы; в статьях ещё иконка языка (D006). Пункта Contact нет. Ссылки шапки набраны serif 16px.
- Consequences: новая страница или статья получает ту же шапку, а не свою. Ширина шапки статей 960px, как у Blog.

### D002 · Логотип в исходном шрифте
- Status: accepted · By: author-request · Date: 2026-11-21 · Scope: `.nav-logo` на всех страницах
- Context: «давай для andrei filatov в шапке оставим исходный шрифт»
- Decision: «andrei filatov» — JetBrains Mono 14px, вес 400, на всех страницах. Остальной моноширинный текст в шапке заменён на основной шрифт.
- Consequences: при унификации шрифтов логотип не трогать; font-face JetBrains Mono не удалять.

### D003 · Один раздел Blog для постов и докладов
- Status: accepted · By: author-request · Date: 2026-11-21 · Scope: главная, `pages/blog.html`
- Decision: «Writing and talks» и Blog — один раздел под названием Blog. Доклады (Data Fest, Belgrade) лежат на странице Blog рядом с постами; на главной заголовок «Blog», описание «Long-reads and talks on diffusion post-training, GPUs and inference.»
- Consequences: новый доклад добавляется карточкой на `pages/blog.html`. Лента главной берёт посты из карточек Blog; внешние ссылки (YouTube) лента пропускает.

### D004 · Без указаний языка и без «~» в списках
- Status: accepted · By: author-request · Date: 2026-11-21 · Scope: карточки Blog, лента главной
- Context: «в blog убери ~ около времени»; RU/EN в строках с датой убрать.
- Decision: в датах нет «RU/EN» и «in English and Russian»; время чтения пишется «33 min read», без «~».
- Consequences: внутри самих статей «~» пока остаётся — мета-строку и переводы собирает `tg_channel`, здесь их руками не правят (см. D012).

### D005 · Без подзаголовков на Blog и Projects
- Status: accepted · By: author-request · Date: 2026-11-21 · Scope: `pages/blog.html`, `pages/projects.html`
- Context: «Foundation models, generation platforms, papers and tools — things shipped, not just started … давай вообще уберем», «и gap убери оставшийся», «и в blog … тоже самое».
- Decision: на обеих страницах только заголовок, от него до списка 48px, без пустого места на месте подзаголовка.
- Consequences: не возвращать лид-абзац под h1 без просьбы автора.

### D006 · Смена языка в статьях — иконка в шапке, без перезагрузки
- Status: accepted · By: author-request · Date: 2026-11-21 · Scope: `templates/longread/lang-toggle.js`, `style.css`, `site_nav`
- Context: пилюля RU/EN и текст «EN / RU» автору не понравились (R001, R002), ссылка в мета-строке отвергнута (R003); «переход между версиями давай сделаем, и в шапке больше места сделаем».
- Decision: иконка языка (Lucide «languages») рядом с кнопкой темы, подсказка «Читать на русском» / «Read in English». Клик: текст гаснет на 0,16 с, язык меняется через `setLang`, тот же абзац остаётся на том же месте экрана, адрес меняется на `.ru.html` / `.html`. Старый блок `.lang-switch` с `#btn-ru` / `#btn-en` остаётся в разметке скрытым — на него опирается `setLang`.
- Consequences: при `prefers-reduced-motion` смена без затухания. Новая статья должна держать `setLang`, `btn-ru`, `btn-en`, `theme-btn` (см. `templates/longread/README.md`).

### D007 · Переключатель языка — настоящая ссылка
- Status: accepted · By: claude-code/claude-opus-5-5 · Date: 2026-11-21 · Scope: `site_nav` в `builder/build_publication.py`
- Context: правило репозитория — переключатели языка работают без JS, статический HTML несёт язык страницы.
- Decision: сборка запекает иконку в обе версии: на `.html` ссылка ведёт на `.ru.html` с подписью «Читать на русском», на `.ru.html` — наоборот; `hreflang`, `lang`, `data-language` выставлены. JS лишь перехватывает обычный клик; клик с модификатором и страница без `setLang` идут по ссылке. Цель касания 44px при `pointer: coarse`, есть `:focus-visible`.
- Consequences: при смене языка на месте скрипт сам переводит пункты меню (Projects/Blog ↔ Проекты/Блог) и блок «В статье» на телефоне — они собираются при сборке на языке страницы.

### D008 · Высота шапки статьи как на остальных страницах
- Status: accepted · By: author-request · Date: 2026-11-21 · Scope: `.post-nav`
- Context: «размер шапки как будто маловат»
- Decision: шапка статьи 62px (отступы 16px, внутренняя высота 29px), как на главной, Blog и Projects.

### D009 · Контакты в первом экране главной
- Status: accepted · By: author-request · Date: 2026-11-21 · Scope: `pages/index.html`
- Decision: одно предложение под описанием, над Resume: «Happy to help with a consultation, or just write to talk: email or Telegram.» (email → mailto, Telegram → https://t.me/anvilarth). Иконка Telegram в ряду соцсетей ведёт на канал, подсказка «Telegram channel». Нижней секции Contact нет.

### D010 · Главная из трёх экранов, Projects — момент photo-chapters
- Status: accepted · By: author-approved-text · Date: 2026-11-21 · Scope: `pages/index.html`, `static/moments/`
- Decision: первый экран, Projects, Blog; каждая секция в высоту окна (100svh, на телефоне 100lvh), без scroll-snap. Projects — момент photo-chapters (taste skill): секция держится, по прокрутке следующая картинка открывается поверх предыдущей; на десктопе картинка слева, текст справа, на телефоне текст под картинкой; над названием строка «год · место». Ссылки «See all projects» / «See all posts» в строке заголовка справа. Отступы по шкале 4–8–12–16–24–32–48–64–96. Имя — Inter 600, трекинг −0,04em.
- Consequences: JS момента лежит в `static/moments/` (не `assets/`, чтобы не пересечься с `/assets/<slug>/` статей). В Blog на главной три пункта: два новейших поста (`latest_feed(..., count=2)`) и доклад, вписанный в `pages/index.html` после блока `feed-posts`.

### D011 · Обложки проектов — серия плоских иллюстраций 3:2
- Status: accepted · By: author-approved-text · Date: 2026-11-21 · Scope: `static/img/projects/*.jpg`, `templates/project-covers.py`
- Decision: 10 обложек — одна серия иллюстраций, каждая показывает идею проекта. 1536×1024, без кропа, показываются с `object-fit: contain` на фоне цвета бумаги. Промпты (STYLE + SUBJECTS) — в `templates/project-covers.py`.
- Consequences: новая обложка генерируется тем же STYLE. Файлы заменяются по тем же адресам: URL картинок публичны и не переименовываются.

### D012 · Тексты статей из tg_channel здесь не правятся
- Status: accepted · By: claude-code/claude-opus-5-5 · Date: 2026-11-21 · Scope: `posts/` (DPO, RL for Diffusion)
- Context: правило репозитория; «~» в мета-строке статей живёт в данных перевода статей.
- Decision: оформление статей меняется только через `templates/longread/` и `builder/`; содержимое статей — в `tg_channel`.
- Consequences: убрать «~» внутри статей — задача для сборщика статей в `tg_channel`.

### D013 · Черновики не публикуются вместе с правками оформления
- Status: accepted · By: claude-code/claude-opus-5-5 · Date: 2026-11-21 · Scope: git, публикация
- Context: в локальном master лежали неопубликованные коммиты черновика `posts/image-dedup` (с файлом `DRAFT`), а на GitHub появились новые коммиты.
- Decision: правки оформления перенесены поверх `origin/master` и опубликованы отдельно; коммиты черновика оставлены локально поверх них.
- Consequences: при следующем пуше проверять `git log origin/master..master` и не публиковать черновики без отдельной просьбы.

## Proposed (ждут автора)

### P01 · Мелкий моноширинный текст в статьях
- Status: proposed · By: claude-code/claude-opus-5-5 · Date: 2026-11-21 · Scope: футер «Designed & built by…», строка «For agents and LLMs…» в статьях
- Decision: на главной, Blog и Projects эти строки уже набраны основным шрифтом 13px; в статьях они пока моноширинные. Нужно решение автора: убрать или уменьшить.

## Superseded / rejected

### R001 · Пилюля RU/EN в шапке статьи
- Status: rejected · By: author · Date: 2026-11-21
- Context: «вот это еще некрасиво выглядит придумай как красиво сделать»
- Decision: отвергнуто, заменено иконкой (D006).

### R002 · Текст «EN / RU» в шапке
- Status: rejected · By: author · Date: 2026-11-21
- Context: «RU EN не знаю как этот нативно переход сделать»
- Decision: отвергнуто, заменено иконкой (D006).

### R003 · Ссылка на другой язык в мета-строке статьи
- Status: rejected · By: author · Date: 2026-11-21
- Context: «ну не хуйня»
- Decision: отвергнуто; язык переключается из шапки (D006).
