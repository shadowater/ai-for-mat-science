# Preparation Class 1: Learn to Solve Problems with Search and Meet Your Computer

**Computers are wonderful, but computers can also be quite stupid.** They can do many things, but you need to tell them what you want in a language they understand. In this preparation class, we will first learn to solve problems with search, then look at what roughly happens inside a computer when you open a program. Relax: you can start without any computing background.

The readings under `materials/` are in this folder and can be opened locally. You will still need a browser to watch videos and download software.

## What you will do

1. Watch two SI100+ videos: one about solving problems with search and one about computer basics.
2. Read the related local material, including two chapters from *The Computer Class You Missed* (《你缺失的那门计算机课》).
3. Install Visual Studio Code (VS Code), open **this whole folder**, and view this document as Markdown. It might open a new world for you.

If you already know a topic, you can skip the corresponding section.

## 1. Start with a question and learn to search

Watch **“How to Solve Problems with Search” (如何用搜索解决问题)** in the [SI100+ Bilibili video collection](https://www.bilibili.com/video/BV12L8r6MEn9/). You can compare it with the local [SI100+ 2024 search slides](materials/si100plus-2024/search/Lecture_x_Search.md), or view the [slides on GitHub](https://github.com/teafrogsf/SI100Plus/blob/58ee452e61b462cc70127e8bcc851bb2e022a0b3/Lecture_x_Search/Lecture_x_Search.md) in your browser.

Then read the local [“What to Do When Something Goes Wrong”](materials/missing-web/how-to-find-solutions.md), a copy of [the chapter on the 《你缺计课》 website](https://www.criwits.top/missing/how-to-find-solutions.html). Its examples mostly use Windows, but the method for solving problems with search also works on other systems.

Imagine that a file will not open. Saying “My computer is broken” gives a helper very little to work with. A more useful description says **what you wanted to do, what you did, and what actually happened**. If an error message appears, keep its exact words. To search, start with short keywords such as the program name and the error text. If the results are about a different program or version, adjust the keywords and try again.

When you have a question, you can use a search engine, ask another person, or ask AI. An AI chat tool lets you type a question as if you were having a conversation, then ask follow-up questions. Whichever option you choose, explain **what you wanted to do, what you did, and what actually happened**; this helps you solve the problem. Here are some entry points; you only need to try one:

| Region | AI chat tool | Website |
|---|---|---|
| China | DeepSeek | [Open DeepSeek](https://chat.deepseek.com/) |
| China | Kimi | [Open Kimi](https://www.kimi.com/) |
| Outside China | ChatGPT | [Open ChatGPT](https://chatgpt.com/) |
| Outside China | Claude | [Open Claude](https://claude.ai/) |
| Outside China | Gemini | [Open Gemini](https://gemini.google.com/) |

Search results and AI answers are leads, not proof. Look for the original source, check whether it fits your situation, and test a suggestion before you rely on it. You can ask AI to explain an unfamiliar term, but check important claims against a source or a small experiment.

**Try one question for practice:** “Why does a computer need both RAM and storage?” “If a file will not open, how should I describe the problem so that a search engine, a classmate, or AI can help me?” or “Besides search engines and asking other people, which AI chat tools could I use?” First try to find an answer yourself; then explain in your own words how you checked it.

## 2. Meet the computer behind the screen

Watch **“Computer Basics” (计算机基本知识)** in the same [SI100+ video collection](https://www.bilibili.com/video/BV12L8r6MEn9/). If you want to review, open the local [SI100+ 2024 computer basics slides](materials/si100plus-2024/basics/Lecture_i_Basic_Knowledge.md), or view the [slides on GitHub](https://github.com/teafrogsf/SI100Plus/blob/58ee452e61b462cc70127e8bcc851bb2e022a0b3/Lecture_i_Basic_Knowledge/Lecture_i_Basic_Knowledge.md) in your browser. Then read the local [“Meet Your Computer”](materials/missing-web/computer-and-its-components.md), which corresponds to [the chapter on the 《你缺计课》 website](https://www.criwits.top/missing/computer-and-its-components.html). Focus first on the CPU, memory, storage, software, and operating systems. You can leave product names and model numbers for later.

Here is a simple first picture:

| Term | First meaning | Example |
|---|---|---|
| **Hardware** | Physical parts you could touch | A CPU chip or a storage drive |
| **Software** | Instructions and data that make the hardware do a job | A browser or VS Code |
| **CPU** | The part that carries out many of a program's instructions | Calculating a value |
| **Memory (RAM)** | Working space used while programs run | Holding the document you are editing right now |
| **Storage** | Where files remain when programs close or power goes off | The saved copy of this guide |
| **Operating system** | Software that helps programs use hardware and manages files and running programs | Windows, macOS, or Linux |

When you double-click a program icon, your mouse provides an **input**. The operating system finds the program's files in storage and starts it. The computer places the needed instructions and data in memory; the CPU carries out instructions, and the screen shows an **output**. This picture leaves out many details, but it helps explain an important difference: **a file saved on storage is not the same as a program currently running in memory**.

If anything in this section is unclear, try using the methods from the search section to find an answer. We also encourage you to explore other chapters from SI100+ and 《你缺计课》 on your own.

## 3. Hands-on task: open this folder in VS Code

VS Code is an **editor**: it helps you open and change files. Later in the course, we will learn how to use an editor with a Python environment. For now, opening and reading Markdown is enough.

1. Download VS Code for your operating system from the [official download page](https://code.visualstudio.com/download) and install it. If it is already installed, use your existing copy.
2. Open VS Code and choose **File → Open Folder**. Select the entire `预习课一` folder. The file list on the left should show `README.md`, `README.zh.md`, and `materials`.
3. Click `README.md` in that file list. You are now reading the plain text of a **Markdown** file. Markdown adds simple structure to plain text: `#` marks a heading, `-` starts a list item, and `[label](link)` makes a link. If you are interested, you can learn more from the [Markdown basic syntax guide](https://www.markdownguide.org/basic-syntax/).
4. Open the preview with **Ctrl+Shift+V** on Windows/Linux or **Shift+Command+V** on macOS. Compare the plain text with the formatted view. Click a **local reading link** above; it should open another file from this folder in VS Code. Online links will open a browser.
5. Find one heading, one list, and one link in both views. If you want to try more, copy this guide, edit the copy, and see how its preview changes.

VS Code has a built-in Markdown preview. If you get stuck, use the methods you just learned to find an answer. The [official VS Code Markdown guide](https://code.visualstudio.com/docs/languages/markdown) shows the preview commands.

## Sources and credit

The videos and 2024 slides are by the [SI100+ team](https://github.com/teafrogsf/SI100Plus). The two 《你缺计课》 chapters are by Hans Wan and Windy Deng; see their [website](https://www.criwits.top/missing/) and the [source and license note](materials/missing-web/SOURCE.md). Thank you to both teams for sharing these learning materials.
