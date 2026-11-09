# Connect this starter to GitHub

The GitHub connector available in the current workspace can inspect and modify existing repositories, but it does not expose a create-repository action. Create the empty remote once through GitHub, then push this local repository.

## 1. Create an empty private repository

Open https://github.com/new and use:

- Owner: `czyboi`
- Repository name: `system-design-academy`
- Visibility: **Private**
- Do not initialize with a README, .gitignore, or license (this starter already contains files).

## 2. Push this local repository

From the extracted `system-design-academy` folder:

```bash
git remote add origin https://github.com/czyboi/system-design-academy.git
git push -u origin main
```

Authenticate using GitHub CLI or your normal Git credential manager. Do not put a personal access token in this repository or in chat.

## 3. Connect ChatGPT to the new repository

After the repository exists and the GitHub connection has access, select/authorize `czyboi/system-design-academy`. Then use Codex/Work against this repository. Keep the repository private while the curriculum, attribution, and third-party asset review are in progress.
