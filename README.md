<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/XanaDublaKublaConch/sshcheck">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">SSHCheck</h3>

  <p align="center">
    A small utility for checking ssh hosts against a YAML Key Exchange security policy
    <br />
    <a href="https://github.com/XanaDublaKublaConch/sshcheck"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/XanaDublaKublaConch/sshcheck">View Demo</a>
    ·
    <a href="https://github.com/XanaDublaKublaConch/sshcheck/issues">Report Bug</a>
    ·
    <a href="https://github.com/XanaDublaKublaConch/sshcheck/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![](/home/johnny/PycharmProjects/sshcheck/images/product-snapshot.png)](https://example.com)


<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Python][Python.org]][Python-url]
* [![Typer][Typer.tiangolo.com]][Typer-url] Typer

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To set up sshcheck, you will need to clone the repo and install locally with pip because I haven't botherd with pypi yet.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/XanaDublaKublaConch/sshcheck.git
   ```
2. Create a venv in the cloned folder
   ```sh
   # windows
   cd sshcheck
   py -3.10-64 -m venv venv
   venv\scripts\activate
   pip install .
   
   # Linux
   cd sshcheck
   python3 -m venv venv
   . venv/scripts/activate
   pip install .
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

To use the utility, you can run it from the *activated venv* with the `sshcheck` command using the syntax:

`sshcheck <ip or hostname> --port <port>`

The --port option is not required and defaults to the standard port 22.

  ```shell
  sshcheck 192.168.1.1
  sshcheck localhost --port 2222
  ```

SSHCheck uses the `rich` python library for pretty console display.

There are additional flags you can use to output svg, png, or pdf results (currently uses the fully-qualified hostname 
as the filename):

  ```shell
  sshcheck myssh-server.home.local --svg-export
  sshcheck myssh-server.home.local --png-export
  sshcheck myssh-server.home.local --pdf-export
  # combined
  sshcheck myssh-server.home.local --svg-export --png-export --pdf-export
  ```

SVG/PDF output is built into `rich`, but PNG output requires the `cairosvg` library.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Take a policy as input?
- [ ] Custom exceptions
- [ ] FastAPI front-end
    - [ ] Bulk host input? Not sure if I'm comfortable with this.

See the [open issues](https://github.com/XanaDublaKublaConch/sshcheck/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

XanaDublaKublaConch - Use github issue tracker

Project Link: [https://github.com/XanaDublaKublaConch/sshcheck](https://github.com/XanaDublaKublaConch/sshcheck)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Me](https://github.com/XanaDublaKublaConch) - I barely did anything. This was all built on:
* [Paramiko](https://www.paramiko.org/) - The gold standard for python ssh
* [Typer](https://typer.tiangolo.com/) - Typer is :sparkles: awesome :sparkles:
* [Rich](https://github.com/Textualize/rich) - Cross-platform beautiful output


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/XanaDublaKublaConch/sshcheck.svg?style=for-the-badge
[contributors-url]: https://github.com/XanaDublaKublaConch/sshcheck/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/XanaDublaKublaConch/sshcheck.svg?style=for-the-badge
[forks-url]: https://github.com/XanaDublaKublaConch/sshcheck/network/members
[stars-shield]: https://img.shields.io/github/stars/XanaDublaKublaConch/sshcheck.svg?style=for-the-badge
[stars-url]: https://github.com/XanaDublaKublaConch/sshcheck/stargazers
[issues-shield]: https://img.shields.io/github/issues/XanaDublaKublaConch/sshcheck.svg?style=for-the-badge
[issues-url]: https://github.com/XanaDublaKublaConch/sshcheck/issues
[license-shield]: https://img.shields.io/github/license/XanaDublaKublaConch/sshcheck.svg?style=for-the-badge
[license-url]: https://github.com/XanaDublaKublaConch/sshcheck/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
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
[Python.org]: https://img.shields.io/badge/python-0769AD?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[Typer.tiangolo.com]: https://typer.tiangolo.com/img/icon-white.svg
[Typer-url]: https://typer.tiangolo.com/