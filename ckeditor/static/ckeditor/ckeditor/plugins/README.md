<p align="center">
    <a href="https://textarea.ai/"><img src="https://textarea.ai/img/favicons/logo-90.png" alt="Textarea.AI" width="90" /></a>
</p>

<h1 align="center" style="margin-top:-20px">Textarea.AI</h1>

<p align="center">
    <strong>ChatGPT plugin for CKEditor 4 for fast copyrighting and writing texts with AI. </strong>
</p>

<p align="center">
    <a href="https://textarea.ai/">Home page</a> ∙ <a href="https://textarea.ai/doc/install-chat-gpt-ckeditor-4-plugin/">Install</a> ∙ <a href="https://codepen.io/textarea-ai/pen/mdQEOJE">Try Online</a>
</p>

[textareaai.webm](https://github.com/edsdk/textareaai-ckeditor/assets/47594816/db99630d-bb92-406e-9662-54edf83c13b1)

## Intro

This is a **ChatGPT plugin for CKEditor 4**. It can help to generate texts with AI and publish it on your website.

If you have already installed and use [N1ED](https://n1ed.com) plugin, please do not install this one: ChatGPT is included into N1ED. Use this Textarea.AI ChatGPT add-on when you need just a GPT features only.

### Main features:

- Seamless integration with CKEditor 4
- Easy installation as CKEditor plugin
- All the power of GPT-4 in your CKEditor
- Press a toolbar button or Ctrl+Enter everywhere to generate a text! With selection or not, it is very smart.

## Installation

[Download ChatGPT plugin](https://textarea.ai/download/chat-gpt-ckeditor.zip)

Copy `chat-gpt` directory into `ckeditor/plugins/`.
You will have such file path as result: `ckeditor/plugins/chat-gpt/plugin.js`.

### If you use `config.js`
Add these line into your "config.js" file to activate the plugin and new buttons:
```js
config.extraPlugins = "chat-gpt";
config.apiKey = "TXAIDFLT"; // Default key. Get own: https://textarea.ai/dashboard
config.toolbar = [
    { name: 'standard', items: ['TextareaAI', 'TextareaAILess', 'TextareaAIMore', '-', 'Bold', 'Italic', '-', 'Link', 'Unlink', '-', '-', 'FontSize', 'Format', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'] },
];
```

### If you use initialization script
When you pass parameters to CKEditor 4 manually as function argument, do the same but inside config structure:
```js
CKEDITOR.replace(
  "#editor",
  {
     extraPlugins: "chat-gpt",
     apiKey: "TXAIDFLT", // Default key. Get own: https://textarea.ai/dashboard
     toolbar: [
        { name: 'standard', items: ['TextareaAI', 'TextareaAILess', 'TextareaAIMore', '-', 'Bold', 'Italic', '-', 'Link', 'Unlink', '-', '-', 'FontSize', 'Format', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'] },
     ],
  }
);
```

## Configuration

Please check that you switched the plugin to use your API key, you can get it here: [https://textarea.ai/dashboard](Dashboard).

## Support

Please do not hesitate to ask any questions regarding installation or using sending a letter to [support e-mail](support@helpdesk.edsdk.com).
