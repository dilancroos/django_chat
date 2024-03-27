[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![LinkedIn][linkedin-shield]][linkedin-url1]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h2 align="center">Django Chat with LLAMA</h2>
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
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About the Project



<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

Python 3.11.6^

- install pip

  ```sh
    $ python3 -m pip install pip
  ```

### Installation

1. Clone the repo

   ```sh
    $ git clone git@github.com:dilancroos/django_chat.git
   ```

2. Change to the working directory

   ```sh
    $ cd django_chat
   ```

- Check <a href="#usage">Usage</a> to create a virtual environment

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

- Create a virtual environment .venv

  ```sh
    $ python3 -m venv .venv
  ```

- Enter the virtual environment .venv

  ```sh
    $ source .venv/bin/activate
  ```

- Install PIP packages

  ```sh
    $ pip install -r requirements.txt
  ```

- Rename envtemp to .env
<br/>

- Add your Llama Api key to .env file
    - If you dont have one visit [llama-api.com](https://console.llama-api.com/account/api-token) to creat an API key
<br>

- Run Server

  ```sh
    $ python manage.py runserver
  ```

- Chat

    [https://127.0.0.1:8000](https://127.0.0.1:8000)
    <br>

- Credentials <br>
    User: admin@email.com <br>
    Password: 1zaq2xsw3cde
<br>
- Create user "botty" by,

    - logging in to https://127.0.0.1:8000/admin > Users > ADD USER +

    - Add an email address

    - Select ```Staff status``` & ```Superuser status``` > save

    - Profiles > botty > Choose File --> select file on ./media/avatars/botty.png

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

Dilan Croos - antondilan.crooswarnakulasuriya@cri-paris.org.com

Project Link: [https://github.com/dilancroos/django_chat](https://github.com/dilancroos/django_chat)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

-

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
