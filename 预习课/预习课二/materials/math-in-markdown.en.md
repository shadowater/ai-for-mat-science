# Formula quick reference for Markdown

This sheet is an original course example. Use it with the [class 2 guide](../README.md) and your copied `my-note.md`. You only need to try **one inline formula and one separate-line formula**. The other forms are here when you need them later.

## See the source and the result

In VS Code, open a `.md` file and its Markdown preview. A formula **inside a sentence** goes between single dollar signs: the source `$d=2r$` displays as $d=2r$.

For a formula **on its own line**, place double dollar signs on lines by themselves. Copy these three lines into `my-note.md`:

```text
$$
A=\pi r^2
$$
```

The code block above shows the characters to type; formulas **inside** a code block are shown as text. In the preview of your note, the three copied lines display as

$$
A=\pi r^2
$$

VS Code's Markdown preview and GitHub Markdown support math display. Other Markdown viewers may show the dollar signs literally. Use the [VS Code guide](https://code.visualstudio.com/docs/languages/markdown) and [GitHub math guide](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions) if a preview looks different.

## A small set of useful symbols

| What you want | Type in Markdown | Meaning in a research note |
|---|---|---|
| Power | `$r^2$` or `$r^{10}$` | `^` raises the following symbol or braced group. |
| Subscript | `$m_0$` or `$m_{initial}$` | `_` lowers the following symbol or braced group. |
| Greek letter | `$\theta$`, `$\pi$`, `$\Delta m$` | An angle, π, or a change in mass. |
| Fraction | `$\frac{\Delta m}{m_0}$` | First braces give the numerator; second braces give the denominator. |
| Square root | `$\sqrt{x}$` | A square root. |
| Multiplication | `$a\times b$` | A multiplication sign. |
| Units | `$r=5\,\mu\mathrm{m}$` | `\,` adds a small space; `\mu` means micro; `\mathrm{m}` makes the unit m upright. |

Use the original references when you need more than these examples: [Overleaf on powers and subscripts](https://www.overleaf.com/learn/latex/Subscripts_and_superscripts), [Greek letters and symbols](https://www.overleaf.com/learn/latex/List_of_Greek_letters_and_math_symbols), [fractions](https://www.overleaf.com/learn/latex/Fractions_and_Binomials), and [spacing in math mode](https://www.overleaf.com/learn/latex/Spacing_in_math_mode). These are lookup pages; there is no need to read them all now.

For example, a simple mass-change expression can be written on its own lines as:

```text
$$
\frac{\Delta m}{m_0}\times 100\%
$$
```

Here `\%` produces a percent sign inside a formula. This is a **notation example**, not a request to analyze experimental data. You do not need to memorize the commands: copy an example, change one piece, and check the preview.

## Try and check

1. In your copied `my-note.md`, keep the inline formula `$d=2r$` from the guide.
2. Add the three-line area formula above. Change `r^2` to `r_0^2` and compare the source with the preview.
3. If you only see raw dollar signs, confirm that you opened the Markdown **preview**, then check the viewer's math support. Keep the source file; you do not need to install LaTeX.

For more symbols, consult [Overleaf's mathematical expressions guide](https://www.overleaf.com/learn/latex/Mathematical_expressions). The Markdown delimiters and preview behavior are documented by [VS Code](https://code.visualstudio.com/docs/languages/markdown) and [GitHub](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions). The examples and explanations here were written for this course; they are not copied from those guides.
