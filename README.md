[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![LinkedIn][linkedin-shield]][linkedin-url1]

<!-- PROJECT LOGO -->
<br />
<div align="center">
    <h2 align="center">Django Local RAG Chat</h2>
    <h5 align="center">Université Paris Cité - M2 - Digital Science (AIRE)</h5>

  <p align="center">
    Dilan Croos
    <br />
    <a href="https://github.com/dilancroos/django_chat"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    ·
    <a href="https://github.com/dilancroos/django_chat/issues">Report Bug</a>
    ·
    <a href="https://github.com/dilancroos/django_chat/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#getting-started">Getting Started</a></li>
    <ul>
        <li><a href="#requirements">Requirements</a></li>
        <li><a href="#setup">Setup</a></li>
        <li><a href="#knowledge-base">Knowledge Base</a></li>
        <li><a href="#run">Run</a></li>
        <li><a href="#configuration">Configuration</a></li>
        <li><a href="#tests">Tests</a></li>
    </ul>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About the Project

A local Django chat app that answers questions from files you place in a local
knowledge-base folder. Source files are converted to Markdown with Microsoft's
MarkItDown first, then the app indexes only the generated Markdown files. The
app uses Ollama for local chat and embedding models, so it does not need a paid
LLM API after installation.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running follow these simple steps.

## Requirements

- Python 3.11 or newer
- Ollama running locally

Install Ollama from <https://ollama.com/download>, then pull the default models:

```sh
ollama pull llama3.2
ollama pull nomic-embed-text
```

## Setup

Clone the repo

```sh
 git clone git@github.com:dilancroos/django_chat.git
 cd django_chat
```

Create and activate a virtual environment:

```sh
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```sh
pip install -r requirements.txt
```

Create an environment file:

```sh
cp envtemp .env
```

Run the database migrations and create a user:

```sh
python manage.py migrate
python manage.py makemigrations
```

again

```sh
python manage.py migrate
```

```sh
python manage.py createsuperuser
```

## Knowledge Base

Put source files in `knowledge_base/`. The app converts them into Markdown in
`knowledge_markdown/`, then indexes only those generated `.md` files.

Supported first-version source file types are:

- PDF
- Word
- PowerPoint
- XLS and XLSX
- CSV
- Markdown
- TXT
- HTML
- JSON and XML
- ZIP

The app checks this folder when you send a chat message. If files changed, it
converts the files into Markdown, then rebuilds the local index in
`rag_storage/` before answering.

You can rebuild the index manually:

```sh
python manage.py rebuild_rag_index
```

To skip rebuilding when the stored manifest is current:

```sh
python manage.py rebuild_rag_index --skip-unchanged
```

## Run

Start Ollama, then start Django:

```sh
python manage.py runserver
```

Open <http://127.0.0.1:8000>, sign in, and ask questions about the files in
`knowledge_base/`. Do not edit `knowledge_markdown/` manually; it is generated
from the source folder.

The app automatically creates the `ai-chat` chat group and `botty` bot user the
first time a chat message is sent.

## Configuration

These settings can be changed in `.env`:

```sh
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_CHAT_MODEL=llama3.2
OLLAMA_EMBED_MODEL=nomic-embed-text
RAG_SOURCE_DIR=knowledge_base
RAG_MARKDOWN_DIR=knowledge_markdown
RAG_STORAGE_DIR=rag_storage
```

## Tests

```sh
python manage.py test
```

<!-- CONTACT -->

## Contact

Dilan Croos - antondilan.crooswarnakulasuriya@cri-paris.org.com

Project Link: [https://github.com/dilancroos/django_chat](https://github.com/dilancroos/django_chat)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

- Django chat template by [Andreas Jud](https://www.youtube.com/@ajudmeister)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/dilancroos/django_chat.svg?style=for-the-badge
[contributors-url]: https://github.com/dilancroos/django_chat/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/dilancroos/django_chat.svg?style=for-the-badge
[forks-url]: https://github.com/dilancroos/django_chat/network/members
[stars-shield]: https://img.shields.io/github/stars/dilancroos/django_chat.svg?style=for-the-badge
[stars-url]: https://github.com/dilancroos/django_chat/stargazers
[issues-shield]: https://img.shields.io/github/issues/dilancroos/django_chat.svg?style=for-the-badge
[issues-url]: https://github.com/dilancroos/django_chat/issues
[license-shield]: https://img.shields.io/github/license/dilancroos/django_chat.svg?style=for-the-badge
[license-url]: https://github.com/dilancroos/django_chat/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url1]: https://linkedin.com/in/antondilancrooswarnakulasuriya
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com
