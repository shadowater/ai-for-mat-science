# Preparation Class 2: Files, Markdown, and Research Sources

This class builds on the first preparation class. You will work with a small, fictional surface experiment. You do not need to write a program or analyze a curve. Allow about 2–3 hours, in short sessions if you prefer. If you already know a step, check it quickly and move on.

## What you will try

1. Find a file and tell its name, extension, location, and likely contents.
2. Copy this folder, then edit a short Markdown note with a local link, an image, and a formula.
3. Compare a PDF with selectable text and an image-only PDF; record the source of a real paper.

The files in [`materials/`](materials/) are small examples made for this class. Read the linked documents here and try the actions on **your copy** of the folder. The only online items are optional reading and original source pages. No account, programming environment, or submission is required for this class.

## 1. Find the file you mean

A **file** is a saved item, such as a note, picture, or PDF. Its **name** helps you recognize it. An **extension** is the part after the final dot: `.md` often means Markdown text, `.pdf` a document in PDF format, and `.svg` a picture described by text. An extension is a clue, not a conversion tool: renaming `picture.svg` to `picture.pdf` does not make a PDF.

A **folder** holds files and other folders. A **path** tells you where an item is. The path `materials/figure.svg` starts from this guide's folder, so it is a **relative path**. A path starting from a computer's root or drive, such as `C:\Users\...` or `/Users/...`, is an **absolute path**. Relative paths make a folder easier to move as a whole.

Open the whole `预习课二` folder in VS Code (File → Open Folder), as in preparation class 1. In its file list, find [`figure.svg`](materials/figure.svg), [`sample.csv`](materials/sample.csv), and [`sample.json`](materials/sample.json). **CSV** is text arranged into rows and columns; **JSON** is text arranged as named pieces of information. You only need to recognize these as file types here. Their scientific use comes later.

**Try it:** Copy the whole `预习课二` folder to a new location and open the copy. Click the [`figure.svg` link](materials/figure.svg) from this guide in the copy. It should still find the figure. If a link fails, check that `materials` moved with `README.md` and `README.zh.md`. Keep the original folder as your reference.

## 2. Make a readable research note

**Markdown** is plain text with small marks that a viewer can turn into headings, lists, links, and images. You saw a heading and a link in class 1. A **source file** is the text you edit; a **preview** shows how a viewer displays it. Both refer to the same saved note.

Open [`materials/note.en.md`](materials/note.en.md) in your copied folder. Save another copy as `my-note.md` **inside `materials`**. Change its sample name, add one list item, and make sure its link to `figure.svg` works. To show an image inside a note, use `![short description](figure.svg)`. The description tells a reader what the picture shows if the picture is unavailable. To point to a file without embedding it, use `[figure](figure.svg)`.

LaTeX is a way to describe the structure and equations of a document using text commands. Some Markdown viewers can also display formulas written with LaTeX-style symbols. In the note, change the inline formula `$A=\pi r^2$` to `$d=2r$`. The dollar signs mark a formula in this viewer; `\pi` means π, and `^2` means “squared.” Keep the `$` signs. You can put a longer formula on its own lines between `$$` marks. In VS Code, use the Markdown preview (Windows/Linux: **Ctrl+Shift+V**; macOS: **Shift+Command+V**) to compare the source and display. If another viewer shows the dollar signs as plain text, check its math support; your source file is still valid Markdown text. The [VS Code Markdown guide](https://code.visualstudio.com/docs/languages/markdown) describes its preview and math display.

In a LaTeX paper source, commands such as `\section{Methods}`, `\includegraphics{figure.png}`, and `\cite{paper-key}` have different jobs: a heading, an image, and a reference. The backslash starts a command; braces hold its input. You only need to recognize this pattern. You do not need to create or compile a LaTeX paper now.

**Optional look ahead:** [Overleaf](https://www.overleaf.com/) is a browser editor for LaTeX projects. A journal may publish its own [article template](https://www.overleaf.com/latex/templates/tagged/academic-journal), which is a ready-made starting layout. You may look for the template of a journal in your field; use the journal's own author instructions to check which template it accepts. No account or finished paper is needed.

## 3. Check what a PDF contains and where a paper came from

**PDF** describes a document's pages. Some PDFs contain text that you can select and copy. Others contain only a picture of each page, for example after scanning paper. **OCR** means optical character recognition: software tries to turn letters in a picture into text. OCR can make a scan searchable, but its output can contain mistakes. A PDF viewer may run OCR automatically, so an apparently selectable scan is not always proof that the original file had a text layer. [Adobe's explanation](https://helpx.adobe.com/ae_en/acrobat/desktop/create-documents/scan-documents-to-pdfs/recognize-text.html) shows this distinction.

Open the two **fictional course examples**, [`text-example.pdf`](materials/text-example.pdf) and [`image-only-example.pdf`](materials/image-only-example.pdf), in a PDF viewer. Try selecting the words “SAMPLE M-02” in each. The text example contains selectable letters; the image-only example contains pixels. If your viewer selects words in both, it may have applied OCR. You do not have to run OCR yourself. Tell a classmate which file you would try first when asking software to quote an exact sentence, and why you would still check the original page.

A paper's **DOI** is a persistent identifier for that work. Its **metadata** is descriptive information such as title, authors, and publication year. A DOI or a search result points you toward a source; it is not the paper's full text and does not guarantee access to its PDF. The [DOI Foundation](https://www.doi.org/the-identifier/what-is-a-doi/) explains the identifier, while the [Crossref metadata guide](https://www.crossref.org/documentation/retrieve-metadata/rest-api/) shows how registered records can be looked up. You do not need to call an API here.

Read the local [paper record](materials/paper-record.en.md), then open its link to the publisher's page if you have internet access. In `my-note.md`, add the paper's title, first author, year, and DOI as a link. Use the publisher page to check one of these details when online. The paper is about contact-angle measurements, which will return as a course example later. You do not need to download or summarize its full text.

## Check yourself

- Can you still open the figure link after moving the **whole folder**?
- Does your edited note show a heading, a list, a local image, and `$d=2r$` in the VS Code preview?
- Can you explain the difference between the two PDFs, and can you find the paper's DOI and publisher page?

If a step fails, keep the file name and the exact error or behavior. You can use the search and help method from preparation class 1. These checks are for your own learning; there is no required hand-in.

## Sources and credit

The notes, figure, small data files, and two PDFs in `materials/` were made for this class; the PDF pages contain fictional sample text. External explanations and the real paper are linked to their original pages: [VS Code Markdown](https://code.visualstudio.com/docs/languages/markdown), [Adobe on OCR](https://helpx.adobe.com/ae_en/acrobat/desktop/create-documents/scan-documents-to-pdfs/recognize-text.html), [DOI Foundation](https://www.doi.org/the-identifier/what-is-a-doi/), [Crossref](https://www.crossref.org/documentation/retrieve-metadata/rest-api/), and the publisher page in the [paper record](materials/paper-record.en.md). No third-party article text or images are included in this folder.
