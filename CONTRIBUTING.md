# 🌐 Contributing to PerfectGrid

Thank you for your interest in contributing to PerfectGrid! Whether you're fixing a bug, improving the interface, adding a feature, or helping with compatibility across platforms, contributions are welcome.

*You **don't**  need to be an expert to contribute. Bug reports, suggestions, documentation improvements, and code contributions are all appreciated.*

## Getting Started

PerfectGrid is a Python desktop application built with PyQt.

### Requirements

- Python 3.10 or newer
- Git
- FFmpeg and FFprobe available on your system (depending on the development workflow

### 🛠️ Set Up a Development Environment

<details>
<summary><i><b>Instructions</b></i></summary>
</br>

Clone the repository:

```bash
git clone https://github.com
cd PerfectGrid
```

Create and activate a virtual environment:

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

Install the project dependencies:

```bash
python -m pip install -r requirements.txt
```
<a name="run-from-source"></a>
Run PerfectGrid from source:

```bash
PYTHONPATH=src python -m perfect_grid.app
```

On Windows PowerShell, use:

```powershell
\$env:PYTHONPATH = "src"
python -m perfect_grid.app
```

</details>

## ⚠️ Before Submitting

A few things to keep in mind when contributing:

- **Keep changes focused.** Try to avoid tons of unrelated changes in the same pull request.

- **Preserve existing architecture and behavior.** If you're changing something that already works, explain why. Consider how it affects other workflows and platforms.

- **Think cross-platform.** PerfectGrid currently supports macOS, Windows, and Linux. A change that works on one system may behave differently on another. This is why testing is vital. Just because it compiles doesn't mean its functional.

- **Avoid unnecessary dependencies.** If something can be handled with the existing tools and libraries, there's *probably* no need to introduce another dependency.

- **Keep the UI consistent.** Changes to the UI should fit into the existing application rather than introduce a completely different visual style.

Before opening a pull request, run the following checks:

```bash
python -m py_compile src/perfect_grid/app.py src/perfect_grid/engine.py
```

If your changes affect video importing, frame extraction, refining, or exporting, please test the relevant workflow with a sample video where possible.

## 📌 Opening a Pull Request

1. Fork the repository.
2. Create a *branch* for your changes.
3. Make your changes and [test them](#run-from-source) locally.
4. Commit your work with a clear description of what changed.
5. Then open a pull request against the `main` branch.

In your pull request, please include:

- A brief explanation of what you changed and why.
- Any relevant screenshots for UI changes.
- Steps to reproduce the issue if you're fixing a bug.
- The operating systems you've tested on.
- Any known limitations or things that still need attention.


> Organized, *focused* pull requests are easier to review.


## 🪲 Reporting Bugs

Bug reports are just as valuable (if not more) as code contributions. When reporting an issue, please include as much of the following information as possible:

- **Operating system:** macOS, Windows, or Linux (include the version, it will be in the bottom right of the controls panel). *Please note, releases before v0.2.3 do not contain dynamic versioning*
- **PerfectGrid version:** Include the release version or commit if running from source.
- **What happened:** Describe the unexpected behavior.
- **What's expected:** Explain what you thought should happen instead.
- **Steps to reproduce:** Include the action(s) that led to the issue.

- **Video details:** Include the file extension and codec if known.
- **Workflow affected:** Preview, refine, export, batch processing, or another part of the application.
- **Additional information:** Include terminal output, screenshots, or other relevant details.

For video-related issues, screenshots and sample information can be especially helpful.

**Don't upload private video files or other personal material unless you're comfortable sharing them publicly.** If a sample file is necessary to reproduce an issue, consider using a free, non-sensitive example, e.g.

1. [download.blender.org - Big Buck Bunny](https://download.blender.org/demo/movies/BBB/)

2. [samplelib.com - Sample MP4 video files](https://samplelib.com/sample-mp4.html)
3. [cde.ca.gov - Video Sample](https://www3.cde.ca.gov/download/rod/videosample1.html)


## Feature Requests and Suggestions

Have an idea for something you'd like to see in PerfectGrid? Open an issue and describe:

- What you'd like to be able to do.
- Why this could be useful, or beneficial.
- How you imagine it working, if you have an idea.

Discussion and feedback are welcome, ***even if you aren't sure how a feature should be implemented.***

## ❤️ A Final Note

PerfectGrid is an evolving solo project as of November 2026, and there's *always* room to improve that. Contributions, feedback, and thoughtful suggestions all help make it better.

Thank you!! You can also reach me by email at [contact@usbx.live](mailto:contact@usbx.live)