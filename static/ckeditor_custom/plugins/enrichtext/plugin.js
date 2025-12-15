(function() {
    const pluginName = 'enrichtext';
    const defaultPrompts = [
        {
            key: 'clarity',
            title: 'Improve clarity',
            instruction: 'Improve clarity, correctness, and tone. Keep meaning.',
        },
    ];

    function normalizePrompts(rawPrompts) {
        if (!Array.isArray(rawPrompts) || !rawPrompts.length) {
            return defaultPrompts;
        }
        return rawPrompts
            .map((item, idx) => {
                const instruction = item && (item.instruction || item.prompt || item.text);
                if (!instruction) return null;
                const title = item.title || item.name || item.label || item.key || `Prompt ${idx + 1}`;
                const key = item.key || item.id || title || `prompt-${idx + 1}`;
                return {
                    key: String(key),
                    title: String(title),
                    instruction: String(instruction),
                };
            })
            .filter(Boolean);
    }

    CKEDITOR.plugins.add(pluginName, {
        icons: pluginName,
        init: function(editor) {
            if (!editor) {
                console.warn('[enrichtext] Editor instance not found');
                return;
            }
            const prompts = normalizePrompts(editor.config.enrichTextPrompts);

            const getCsrfToken = () => {
                const match = document.cookie.match(/csrftoken=([^;]+)/);
                return match ? decodeURIComponent(match[1]) : '';
            };

            const executePrompt = async (instruction, title) => {
                const sel = editor.getSelection();
                const selectedText = sel && sel.getSelectedText();
                if (!selectedText || !selectedText.trim()) {
                    alert('Select some text first.');
                    return;
                }

                const body = { text: selectedText, instruction };

                try {
                    const resp = await fetch('/api/ai/enrich/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCsrfToken(),
                        },
                        body: JSON.stringify(body),
                    });
                    const data = await resp.json();
                    if (!resp.ok || data.error) {
                        throw new Error(data.error || 'Enhancement failed');
                    }
                    const enhanced = data.enhanced_text || selectedText;
                    editor.insertText(enhanced);
                } catch (err) {
                    const label = title ? ` (${title})` : '';
                    alert('AI enhance error' + label + ': ' + err.message);
                }
            };

            editor.ui.addRichCombo('EnrichText', {
                label: 'AI Enhance',
                title: 'AI Enhance',
                toolbar: 'insert',
                className: 'cke_button_enrichtext',
                panel: {
                    css: [CKEDITOR.skin.getPath('editor')],
                    multiSelect: false
                },
                init: function() {
                    prompts.forEach(prompt => {
                        this.add(prompt.key, prompt.title, prompt.instruction);
                    });
                },
                onClick: function(value) {
                    const prompt = prompts.find(item => item.key === value);
                    if (!prompt) {
                        alert('Prompt not found.');
                        return;
                    }
                    executePrompt(prompt.instruction, prompt.title);
                }
            });

            console.log(
                '[enrichtext] plugin loaded for editor',
                editor.name || '(inline)',
                'with prompts:',
                prompts.map(p => p.key)
            );
        }
    });
})();
