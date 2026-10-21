# Preparation Class 2: Files, Markdown, and Research Sources

This class builds on the first preparation class. You will work with a small, fictional surface experiment. You do not need to write a program or analyze a curve. Allow about 2–3 hours, in short sessions if you prefer. If you already know a step, check it quickly and move on.

## What you will try

1. Find a file and tell its name, extension, location, and likely contents.
2. Copy this folder, then edit a short Markdown note with a local link, an image, and a formula.
3. Compare a PDF with selectable text and an image-only PDF; record the source of a real paper.

The [`materials/`](materials/) folder contains a local excerpt from an existing computer course, its pictures, and small examples made for this class. Read the linked material and try the actions on **your copy** of the folder. Original source pages and optional references are online. No account, programming environment, or submission is required for this class.

## 1. Find the file you mean

If you received a ZIP file, extract the whole archive before opening the course folder. A ZIP is one file that packages other files and folders. Use [Microsoft’s unzip instructions](https://support.microsoft.com/en-us/windows/experience/storage-filemanagement/zip-and-unzip-files) or [Apple’s unzip instructions](https://support.apple.com/guide/mac-help/zip-and-unzip-files-and-folders-on-mac-mchlp2528/mac) if needed. In the extracted folder, find `README.md`, `README.zh.md`, and `materials`.

A **file** is a saved item, such as a note, picture, or PDF. Its **name** helps you recognize it. An **extension** is the part after the final dot: `.md` often means Markdown text, `.pdf` a document in PDF format, and `.svg` a picture described by text. An extension is a clue, not a conversion tool: renaming `picture.svg` to `picture.pdf` does not make a PDF.

Show the full filename in your file browser: use [Microsoft’s extension instructions](https://support.microsoft.com/en-us/windows/experience/storage-filemanagement/common-file-name-extensions-in-windows) or [Apple’s extension instructions](https://support.apple.com/en-hk/guide/mac-help/mchlp2304/mac). The local reading below uses Windows screenshots; Mac users can use Apple’s steps for this action.

A **folder** holds files and other folders. A **path** tells you where an item is. The path `materials/figure.svg` starts from this guide's folder, so it is a **relative path**. A path starting from a computer's root or drive, such as `C:\Users\...` or `/Users/...`, is an **absolute path**. Relative paths make a folder easier to move as a whole.

Read the local illustrated excerpt [“File Names and Types” and “Folders, Paths and Directories”](materials/missing-web/file-and-file-management.md) (Chinese), taken from Hans Wan and Windy Deng's *The Computer Class You Missed*. The [complete chapter on the authors' site](https://www.criwits.top/missing/file-and-file-management.html) includes further topics. The [SI100+ 2024 computer basics slides](https://github.com/teafrogsf/SI100Plus/blob/58ee452e61b462cc70127e8bcc851bb2e022a0b3/Lecture_i_Basic_Knowledge/Lecture_i_Basic_Knowledge.md) from class 1 give a short recap of file extensions. In the local excerpt, find the picture of a folder tree, then locate its `Tree.png` file in the `file-and-file-management` subfolder. If you do not read Chinese, use the English definitions above and the folder-tree picture. Use the reading to identify a file name and a path on your own computer; you do not need to memorize the chapter.

Open the whole `预习课二` folder in VS Code (File → Open Folder), as in preparation class 1. In its file list, find [`figure.svg`](materials/figure.svg), [`sample.csv`](materials/sample.csv), and [`sample.json`](materials/sample.json). **CSV** is text arranged into rows and columns; **JSON** is text arranged as named pieces of information. You only need to recognize these as file types here. Their scientific use comes later.

**Try it:** Copy the whole `预习课二` folder to a new location and open the copy. Click the [`figure.svg` link](materials/figure.svg) from this guide in the copy. It should still find the figure. If a link fails, check that `materials` moved with `README.md` and `README.zh.md`. Keep the original folder as your reference.

## 2. Make a readable research note

**Markdown** is plain text with small marks that a viewer can turn into headings, lists, links, and images. You saw a heading and a link in class 1. A **source file** is the text you edit; a **preview** shows how a viewer displays it. Both refer to the same saved note.

Open the local [Markdown Guide cheat sheet](materials/markdown-guide/markdown-cheat-sheet.md), provided by Matt Cone and the Markdown Guide contributors, in both source and preview. Read **Heading, Ordered/Unordered List, Link, Image, Code, and Fenced Code Block**; use the [original illustrated syntax guide](https://www.markdownguide.org/basic-syntax/) when you need more detail. The remaining sections are optional, and some extended forms do not render in every viewer. Use our formula reference for math, rather than the cheat sheet’s `H~2~O` or `X^2^` forms. The local sample note below also links back to the original reading so you can see how a source is recorded in a Markdown file.

Open [`materials/note.en.md`](materials/note.en.md) in your copied folder. Save another copy as `my-note.md` **inside `materials`**. Change the heading after `#`, change its sample name, add one list item, and make sure its link to `figure.svg` works. To show an image inside a note, use `![short description](figure.svg)`. The description tells a reader what the picture shows if the picture is unavailable. To point to a file without embedding it, use `[figure](figure.svg)`.

A **code block** displays several lines literally, which is useful for keeping an error message or a writing example. Find “Fenced Code Block” in the cheat sheet, and add a block containing `sample: M-02` to your note. Its opening and closing marks are three backticks, not quotation marks. Save with **Ctrl+S** (Windows/Linux) or **Command+S** (macOS), close the note, and reopen it to check that your edits were saved. Use the ordinary keyboard characters shown in the examples: full-width characters such as `＃` and `＄` are different from `#` and `$`.

LaTeX is a way to describe the structure and equations of a document using text commands. Some Markdown viewers can also display formulas written with LaTeX-style symbols. In the note, change the inline formula `$A=\pi r^2$` to `$d=2r$`. The dollar signs mark a formula in this viewer; `\pi` means π, and `^2` means “squared.” Keep the `$` signs. You can put a longer formula on its own lines between `$$` marks. In VS Code, use the Markdown preview (Windows/Linux: **Ctrl+Shift+V**; macOS: **Shift+Command+V**) to compare the source and display. If another viewer shows the dollar signs as plain text, check its math support; your source file is still valid Markdown text. The [VS Code Markdown guide](https://code.visualstudio.com/docs/languages/markdown) describes its preview and math display.

The local [formula quick reference](materials/math-in-markdown.en.md) shows inline and separate-line formulas, powers, subscripts, Greek letters, fractions, roots, and units. Try its two short actions in your copied note; keep the table for later lookup. [GitHub's math guide](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions) describes how the same style is displayed in this repository.

In a LaTeX paper source, commands such as `\section{Methods}`, `\includegraphics{figure.png}`, and `\cite{paper-key}` have different jobs: a heading, an image, and a reference. The backslash starts a command; braces hold its input. You only need to recognize this pattern. These document commands belong in a `.tex` paper source; they do not turn a Markdown heading, image, or citation into a formatted one. You do not need to create or compile a LaTeX paper now.

**Optional look ahead:** [Overleaf](https://www.overleaf.com/) is a browser editor for LaTeX projects. A journal may publish its own [article template](https://www.overleaf.com/latex/templates/tagged/academic-journal), which is a ready-made starting layout. You may look for the template of a journal in your field; use the journal's own author instructions to check which template it accepts. For a concrete source-to-PDF example, read only “What is LaTeX?” and “Writing your first piece of LaTeX” in [Overleaf’s introductory tutorial](https://www.overleaf.com/learn/latex/Learn_LaTeX_in_30_minutes). Compare the short source with the shown result. No account or finished paper is needed.

## 3. Check what a PDF contains and where a paper came from

**PDF** describes a document's pages. Some PDFs contain text that you can select and copy. Others contain only a picture of each page, for example after scanning paper. **OCR** means optical character recognition: software tries to turn letters in a picture into text. OCR can make a scan searchable, but its output can contain mistakes. A PDF viewer may run OCR automatically, so an apparently selectable scan is not always proof that the original file had a text layer. [Adobe's explanation](https://helpx.adobe.com/ae_en/acrobat/desktop/create-documents/scan-documents-to-pdfs/recognize-text.html) shows this distinction.

Open the two **fictional course examples**, [`text-example.pdf`](materials/text-example.pdf) and [`image-only-example.pdf`](materials/image-only-example.pdf), in a PDF viewer. Try selecting the words “SAMPLE M-02” in each. The text example contains selectable letters; the image-only example contains pixels. If your viewer selects words in both, it may have applied OCR. You do not have to run OCR yourself. Tell a classmate which file you would try first when asking software to quote an exact sentence, and why you would still check the original page.

A paper's **DOI** is a persistent identifier for that work. Its **metadata** is descriptive information such as title, authors, and publication year. A DOI or a search result points you toward a source; it is not the paper's full text and does not guarantee access to its PDF. The [DOI Foundation](https://www.doi.org/the-identifier/what-is-a-doi/) explains the identifier, while the [Crossref Metadata Search](https://search.crossref.org/) lets you search for a paper by title in a browser. Its [search help](https://search.crossref.org/help/works) explains the available searches. If useful, paste the example paper’s title there and compare the result with the publisher page. Programmatic retrieval belongs in the later literature practice.

Read the local [paper record](materials/paper-record.en.md), then open its link to the publisher's page if you have internet access. In `my-note.md`, add the paper's title, first author, year, and DOI as a link. Use the publisher page to check one of these details when online. The paper is about contact-angle measurements, which will return as a course example later. You do not need to download or summarize its full text.

## Check yourself

- Can you still open the figure link after moving the **whole folder**?
- Does your edited note show your changed heading, a list, a local image, a code block, `$d=2r$`, and your separate-line formula in the VS Code preview?
- Can you explain the difference between the two PDFs, and can you find the paper's DOI and publisher page?

If a step fails, keep the file name and the exact error or behavior. You can use the search and help method from preparation class 1. These checks are for your own learning; there is no required hand-in.

## Sources and credit

The local excerpt and its eight images come from [*The Computer Class You Missed* by Hans Wan and Windy Deng](materials/missing-web/SOURCE.md), with source, version, license, and changes documented beside it. The local [Markdown Guide cheat sheet](materials/markdown-guide/SOURCE.md) is reused under CC BY-SA 4.0, with a Chinese translation and an image-link adjustment. The sample notes, formula sheet, figure, small data files, and two PDFs were made for this class; the PDF pages contain fictional sample text. Further explanations are linked to their original pages: [SI100+ 2024 slides](https://github.com/teafrogsf/SI100Plus/blob/58ee452e61b462cc70127e8bcc851bb2e022a0b3/Lecture_i_Basic_Knowledge/Lecture_i_Basic_Knowledge.md), [Markdown Guide](https://www.markdownguide.org/basic-syntax/), [VS Code Markdown](https://code.visualstudio.com/docs/languages/markdown), [GitHub math](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions), [Adobe on OCR](https://helpx.adobe.com/ae_en/acrobat/desktop/create-documents/scan-documents-to-pdfs/recognize-text.html), [DOI Foundation](https://www.doi.org/the-identifier/what-is-a-doi/), [Crossref](https://search.crossref.org/), and the publisher page in the [paper record](materials/paper-record.en.md). No third-party research paper text or images are included here.
