# AI image brief

The brief file is the prompt. The user pastes the whole file into Gemini, ChatGPT or another image model, so it must stand alone.

## Rules

- **Self-contained.** No local paths, source file names, repo paths, work IDs, ticket links, private URLs, or phrases like "see the spec", "from the plan", "as in the PR". The model sees only this text.
- **Nothing around it.** No markdown heading, source note, code fence or instructions to the user inside the file.
- **Quote every visible string** exactly as in the content sheet; each string appears once in the image.
- **Describe objects, not ideas.** "A small app window with three colored dots titled ..." beats "show the app".
- **Reading order.** Title, then zones top to bottom and left to right, then footer.
- **Ask for the end product.** Say the image should look ready to publish; that sets the level of polish.
- **Few words.** About 40 strings. Long sentences come out garbled; short isolated labels survive.
- **Same structure on both sides** for before / after, and say so.

## Template

```text
Create a 16:9 landscape <infographic | before/after illustration> for <a pull request description | a feature overview | a session recap>. It should explain <the topic in plain words> <mostly through pictures, with very little text | with short labeled cards>. The result should look like a clean editorial tech illustration, ready to publish.

STYLE: clean flat vector illustration with soft shading, friendly rounded shapes, thin outlines, gentle drop shadows. <Background: very light gray-white (#F8FAFC) | left half warm beige (#F7F4EF), right half cool light gray-blue (#F1F5F9), separated by a thin dashed line with a small white circle holding a right arrow>. <Role colors in words: blue for ..., teal for ..., amber for ..., red for problems, green for the fix>. Geometric sans-serif (Inter-like), dark navy text, slate gray descriptions; monospace for file names and code. Large, readable, few words.

TITLE (<position>, <size/weight>): "<title>"
SUBTITLE: "<subtitle>"

<ZONE NAME>, <position>:
  - <object description> with "<exact string>" ...
  - <arrow from X to Y, color, label "<exact string>">

<repeat per zone>

FOOTER (<position>, small gray): "<takeaway or facts>"

RULES: Spell each quoted label exactly as given and show it only one time. Add no other words, labels, numbers or logos. <Both halves use the same layout so they compare at a glance.> No photorealism, no 3D, no mascots<, no people other than ...>. Nothing overlapping or clipped.
```

## Model notes

- Ask for 16:9 in the chat as well; some apps ignore it in the prompt.
- Gemini image models (Nano Banana family) and ChatGPT images render dense text well; smaller models garble more, so cut strings first.
- Fixing text: ask "Change only the text "<wrong>" to "<right>"; keep everything else identical." Regenerate when the layout itself is wrong.
- After generation, compare every label with the content sheet. Watch for duplicated labels, invented words and swapped values.
