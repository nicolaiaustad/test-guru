# PR Quiz - User Guide

## Installation

### 1. Install GitHub App

1. Navigate to https://github.com/apps/nicolaiaustad-guru-test
2. Click **Install**
3. Select the repositories where you want to enable PR Quiz
4. Click **Install & Authorize**

### 2. Install Chrome Extension

1. Download and unzip the `pr_quiz_extension.zip` file
2. Open Chrome and navigate to `chrome://extensions`
3. Enable **Developer mode** (toggle in the top-right corner)
4. Click **Load unpacked**
5. Select the unzipped `pr_quiz_extension` folder

## Usage

### Taking a Quiz

1. Open any Pull Request in a repository where PR Quiz is enabled
2. The quiz UI will appear automatically on the right side of the PR page
3. Hover over the quiz panel to view questions
4. Answer all questions and click **Submit**
5. Click the verification button to update the PR check status with your score

### Troubleshooting

**Quiz doesn't appear?**
- Refresh the page (F5 or Cmd+R)
- Verify the GitHub App is installed for this repository
- Check that the extension is enabled at `chrome://extensions` with no errors in the log

**Extension errors?**
- Click the extension icon in the Chrome toolbar
- Right-click the extension and select **Inspect popup** to view console errors
- Confirm you are on a Pull Request page, not Issues or other GitHub pages

## Support

If issues persist, contact your administrator with:
- Browser console errors (screenshot from DevTools)
- PR URL where the issue occurred
- Extension version (found at `chrome://extensions`)
