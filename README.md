# Xiaohongshu Draft Skill

An agent skill for preparing Xiaohongshu image-and-text notes and saving them as drafts through the official Creator Service Platform.

The skill helps an agent carry user-approved copy and images into the signed-in creator UI, check the composition, save without publishing, and verify the draft. It does not automate login, bypass platform risk controls, or publish posts.

## Install

Install the skill from this repository with the [Skills CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add yuxbao/xiaohongshu-draft-skill --skill xiaohongshu-draft
```

The skill can become discoverable on [skills.sh](https://skills.sh/) after the public repository is indexed.

## Use

Ask your agent to create a Xiaohongshu post as a draft and provide or identify:

- the final title and body;
- any tags or topics;
- the image files and their intended order;
- the authenticated Xiaohongshu Creator Service Platform session.

The agent should confirm the active account, upload the selected images in order, check the title/body/images in the editor, use the platform's draft-save flow, and verify the saved note in Drafts. A draft request does not authorize publication.

For offline handoff or backup, the repository includes a standard-library Python helper to package a Markdown draft and selected image files into a ZIP. This local bundle is not an uploaded or saved Xiaohongshu draft.

## Contents

- `skills/xiaohongshu-draft/SKILL.md` — the installable skill entry point.
- `skills/xiaohongshu-draft/references/creator-workflow.md` — UI workflow and failure handling.
- `skills/xiaohongshu-draft/scripts/package_draft.py` — create an offline draft bundle.
- `tests/test_package_draft.py` — tests for the packaging helper.

## Validate and test

```bash
python3 skills/xiaohongshu-draft/scripts/package_draft.py --help
python3 -m unittest discover -s tests -v
```

The packaging helper uses only Python's standard library. UI behavior can vary by account, region, platform updates, and browser; verify the live editor and Drafts state each time.

## License

MIT. See [LICENSE](LICENSE).

## 中文使用说明

这是一个供具备浏览器操作能力的 AI 助手使用的工作流 skill。它指导助手确认当前账号、按顺序上传图片、准确填写中文文案、保存草稿并核验结果。它本身不是浏览器驱动，也不提供小红书私有接口。

调用示例：

```text
使用 $xiaohongshu-draft，把我提供的标题、正文和图片创建为小红书图文草稿。图片按文件名数字顺序排列，保存后到草稿箱核验，不要发布。
```

需要支持文件上传和 Unicode 粘贴或填写的浏览器工具，以及用户能够完成的正常登录流程。网页草稿是否同步到手机端，以平台当前提示为准。

离线打包示例（Python 3.9 或更新版本，无第三方依赖）：

```bash
python3 skills/xiaohongshu-draft/scripts/package_draft.py --copy /path/to/draft.md --images /path/to/selected-images --output /path/to/new-bundle.zip
```

只把明确选定的图片放入输入目录；脚本按文件名数字顺序打包 PNG、JPG、JPEG、WebP，忽略子目录及符号链接，不检查图片解码完整性，也不上传任何内容。输出已存在时会报错，避免覆盖文件。ZIP 内包含原文、图片和顺序清单，不保存输入文件的绝对路径。

## Validation status

The helper and skill structure are tested separately from account interaction. A previous browser session confirmed image upload and a save-and-leave control, but text input failed before a saved draft could be verified. End-to-end draft persistence is therefore **not yet verified**. Verify the current editor, exact text, image order, and saved draft on each run.

This repository contains generic instructions and synthetic test data only. It does not include account cookies, private chat exports, personal screenshots, or user-specific draft content.

## Directory listing

The [skills.sh documentation](https://skills.sh/docs) explains that installs through the Skills CLI contribute anonymous install telemetry to the directory. GitHub publication alone does not prove that a listing has been indexed. Directory availability and ranking remain controlled by skills.sh.
