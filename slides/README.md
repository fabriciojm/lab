# Markdown Slides in Terminal

- Testing slides package from Maas Lalani https://github.com/maaslalani/slides
- Note: code execution is broken in the slides snap package. Use an alternative for installation.
- Vim: Add this to silently map `<space> s` to saving the file and showing slides:
```bash
nnoremap <leader>s :w<bar>execute "silent !slides %:p"<bar>redraw!<CR>
```
